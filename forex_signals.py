import urllib.request
import urllib.parse
import json
import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
SYMBOLS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/CHF", "USD/CAD", "NZD/USD"]
API_URL = "https://api.twelvedata.com/rsi"
API_KEY = os.getenv("API_KEY")

def get_rsi(symbol):
    params = {
        "symbol": symbol.replace("/", ""),
        "interval": "5min",
        "time_period": 14,
        "apikey": API_KEY
    }
    query = urllib.parse.urlencode(params)
    url = f"{API_URL}?{query}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return float(data["values"][0]["rsi"])
    except:
        return None

def send_signal(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload)
    try:
        urllib.request.urlopen(req)
    except:
        pass

def generate_signals():
    now = datetime.datetime.now().strftime("%H:%M")
    for symbol in SYMBOLS:
        rsi_val = get_rsi(symbol)
        if rsi_val is None:
            continue
        direction = None
        if rsi_val > 70:
            direction = "SELL"
        elif rsi_val < 30:
            direction = "BUY"
        if direction:
            msg = f"📊 Сигнал: {symbol} — {direction}\n⏰ Время: {now}\n📈 RSI: {round(rsi_val, 2)}"
            send_signal(msg)

generate_signals()

