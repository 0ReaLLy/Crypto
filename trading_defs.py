from datetime import datetime

def safe_fetch_ticker(exchange):
    """Ticker fiyatlarını güvenli bir şekilde getir."""
    try:
        return exchange.fetch_ticker('ETH/USDT')
    except Exception as e:
        raise Exception(f"Hata: Fiyat alınamadı! {e}")

def buy_eth_usdt(exchange, budget, eth_balance, amount_usdt, update_status, update_labels):
    """USDT ile ETH alımı yap."""
    try:
        ticker = safe_fetch_ticker(exchange)
        price = ticker['last']
        if budget >= amount_usdt:
            eth_bought = amount_usdt / price
            eth_balance += eth_bought
            budget -= amount_usdt
            update_status(f"{datetime.now().strftime('%H:%M:%S')} - {amount_usdt:.2f} USDT ile ETH alındı.")
            update_labels()
        else:
            update_status("Yetersiz bütçe!")
    except Exception as e:
        update_status(f"Alım hatası: {e}")
    return budget, eth_balance


def sell_eth_usdt(exchange, budget, eth_balance, amount_usdt, update_status, update_labels):
    """USDT karşılığında ETH satışı yap."""
    ticker = safe_fetch_ticker(exchange)
    price = ticker['last']
    eth_to_sell = amount_usdt / price
    if eth_balance >= eth_to_sell:
        eth_balance -= eth_to_sell
        budget += amount_usdt
        update_status(f"{datetime.now().strftime('%H:%M:%S')} - {amount_usdt} USDT değerinde ETH satıldı.")
        update_labels()
    else:
        update_status("Yetersiz ETH bakiyesi!")
    return budget, eth_balance

def calculate_net_worth(exchange, budget, eth_balance):
    """Net serveti hesapla."""
    ticker = safe_fetch_ticker(exchange)
    current_price = ticker['last']
    return budget + eth_balance * current_price
