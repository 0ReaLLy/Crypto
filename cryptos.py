import ccxt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# contacting with binance
exchange = ccxt.binance()

# kriptolar
symbols = ['ETH/USDT', 'BTC/USDT', 'SOL/USDT']  # ETH, BTC ve SOL

# Verileri kaydet
data = {symbol: {'prices': [], 'times': []} for symbol in symbols}

# Renk
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 

# canlı
def update(frame):
    now = datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    #fiyatları yazdır
    for i, symbol in enumerate(symbols):
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        data[symbol]['prices'].append(current_price)
        data[symbol]['times'].append(formatted_time)

        #grafiğin göze hoş görünürlüğü
        axs[i].clear()
        axs[i].plot(data[symbol]['times'], data[symbol]['prices'], label=symbol, color=colors[i], linewidth=2)

        # görünüş 2.0
        axs[i].legend(loc="upper left", fontsize=10, frameon=False)
        axs[i].set_title(f"{symbol} Fiyatı (Canlı)", fontsize=14, fontweight='bold', color=colors[i])
        axs[i].set_xlabel("Zaman", fontsize=12)
        axs[i].set_ylabel("Fiyat (USDT)", fontsize=12)
        axs[i].tick_params(axis='x', rotation=45, labelsize=10) # x, y değerlerinin belirlenmesi (2 boyutlu bir uzayda grafik oluşturmak)
        axs[i].tick_params(axis='y', labelsize=10)
        axs[i].grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

    plt.tight_layout()

# Tek bir ekran içinde 3 tabloyu yerleştirecek şekilde ayar
# grafik oluşturma
fig, axs = plt.subplots(3, 1, figsize=(12, 10))  # 3 satır, 1 sütun
axs = axs if len(symbols) > 1 else [axs]  # 3 tane crypto parayı birleştirmemize yarar, ayrıca 3 farklı crypto verilerine ulaşmamıza olanak sağlar
# ">" işareti ile tek tek listelemekle uğraşmıyoruz

# Renk ayarı (wallpaper)
fig.patch.set_facecolor('#A9A9A9')  # Açık siyah (gri tonları) arkplan

# Yazı tipi ayarları
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})  # Yazı tipi ve boyutunu ayarlama

# Animasyonu başlat
ani = FuncAnimation(fig, update, interval=2000, cache_frame_data=False) #süreleri belirleme interval=1000: 1sn

# grafiği ekrana yansıt
plt.show() 
