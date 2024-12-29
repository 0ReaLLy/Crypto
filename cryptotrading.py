import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import ccxt
import trading_defs as th

# Binance ile bağlantı
exchange = ccxt.binance()

# Başlangıç verileri
budget, eth_balance = 10000, 0
prices, times = [], []

# Dinamik etiketler için veriler
labels_data = {
    "Bütçe (USDT)": lambda: f"{budget:.2f}",
    "ETH Bakiyesi": lambda: f"{eth_balance:.6f}",
    "Net Servet (USDT)": lambda: f"{th.calculate_net_worth(exchange, budget, eth_balance):.2f}"
}

# GUI güncelleyiciler
def update_labels():
    """Etiketlerin güncellenmesi."""
    for label_text, label_widget in labels.items():
        label_widget.config(text=labels_data[label_text]())

def update_status(message):
    """Durum etiketini güncelle."""
    status_label.config(text=f"Durum: {message}")

# Alım-satım işlevi
def execute_trade(action):
    """Alım-satım işlemini gerçekleştir."""
    global budget, eth_balance
    try:
        amount = float(amount_entry.get())
        if amount > 0:
            if action == "buy":
                budget, eth_balance = th.buy_eth_usdt(exchange, budget, eth_balance, amount, update_status, update_labels)
            elif action == "sell":
                budget, eth_balance = th.sell_eth_usdt(exchange, budget, eth_balance, amount, update_status, update_labels)
        else:
            update_status("Lütfen pozitif bir miktar girin!")
    except ValueError:
        update_status("Geçersiz miktar! Lütfen sayısal bir değer girin.")

# Grafik güncelleme
def update_graph():
    """Grafiği güncelle."""
    global prices, times
    try:
        ticker = th.safe_fetch_ticker(exchange)
        current_price = ticker['last']
        now = datetime.now().strftime("%H:%M:%S")
        prices.append(current_price)
        times.append(now)
        if len(prices) > 300:
            prices.pop(0)
            times.pop(0)
        ax.clear()
        ax.plot(times, prices, label='ETH/USDT', color='blue')
        ax.set_title("ETH/USDT Fiyatı")
        ax.legend()
        canvas.draw()
        update_labels()
    except Exception as e:
        update_status(f"Hata: {e}")
    root.after(3000, update_graph)

# Tkinter başlangıç
root = tk.Tk()
root.title("ETH Trading Simülasyonu")

# Durum etiketi
status_label = ttk.Label(root, text="Durum: Uygulama başlatıldı.", font=("Helvetica", 12))
status_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

# Miktar girişi
ttk.Label(root, text="Miktar (USDT):", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
amount_entry = ttk.Entry(root, font=("Helvetica", 12))
amount_entry.grid(row=1, column=1, padx=10, pady=5)

# Dinamik etiketler
labels = {}
for i, (text, value_fn) in enumerate(labels_data.items(), start=2):
    ttk.Label(root, text=text, font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    labels[text] = ttk.Label(root, text=value_fn(), font=("Helvetica", 12), foreground="green" if "Bütçe" in text else "blue")
    labels[text].grid(row=i, column=1, padx=10, pady=5, sticky="w")

# Alım-satım butonları
buy_button_usdt = ttk.Button(root, text="BUY (USDT)", command=lambda: execute_trade("buy"))
buy_button_usdt.grid(row=len(labels_data) + 2, column=2, padx=10, pady=5)
sell_button_usdt = ttk.Button(root, text="SELL (USDT)", command=lambda: execute_trade("sell"))
sell_button_usdt.grid(row=len(labels_data) + 2, column=3, padx=10, pady=5)

# Grafik ayarları
fig = Figure(figsize=(10, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=len(labels_data) + 3, column=0, columnspan=4, padx=10, pady=10)

# Güncelleme başlat
update_labels()
root.after(3000, update_graph)
root.mainloop()
