from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import random
import aiohttp
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ইউজার ডাটা স্টোর
user_sessions = {}

# ExpertOption API এর ডেমো ক্লায়েন্ট (আসল API এর জন্য সঠিক এন্ডপয়েন্ট)
class ExpertOptionClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.balance = 10000
        self.connected = False
    
    async def connect(self):
        # সিমুলেটেড সংযোগ
        self.connected = True
        return True
    
    async def get_balance(self):
        return self.balance
    
    async def place_trade(self, signal, amount):
        # রিয়েল মার্কেট সিমুলেশন (70% সঠিক)
        win = random.random() < 0.7
        profit = amount * 0.85 if win else -amount
        self.balance += profit
        return {"result": "WIN" if win else "LOSS", "profit": profit, "new_balance": self.balance}

# রিয়েল মার্কেট ডাটা পাওয়ার জন্য Binance API
async def get_real_price(symbol="BTCUSDT"):
    """Binance থেকে রিয়েল টাইম প্রাইস নেয়"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}") as response:
                data = await response.json()
                return float(data['price'])
    except:
        return None

async def get_historical_prices(symbol="BTCUSDT", limit=5):
    """গত ৫ মিনিটের প্রাইস ডাটা নেয় (ট্রেন্ড বের করার জন্য)"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}") as response:
                data = await response.json()
                prices = [float(candle[4]) for candle in data]  # closing prices
                return prices
    except:
        return None

def calculate_signal_from_prices(prices):
    """প্রাইস ডাটা থেকে সিগন্যাল বের করে"""
    if not prices or len(prices) < 2:
        return "CALL", 50
    
    # ট্রেন্ড বিশ্লেষণ
    price_change = (prices[-1] - prices[0]) / prices[0] * 100
    
    if price_change > 0.2:
        return "CALL", 85  # ঊর্ধ্বমুখী প্রবণতা
    elif price_change < -0.2:
        return "PUT", 85   # নিম্নমুখী প্রবণতা
    else:
        # RSI সিমুলেশন (সরলীকৃত)
        rsi = random.randint(40, 60)
        if rsi > 55:
            return "CALL", 65
        elif rsi < 45:
            return "PUT", 65
        else:
            return "CALL" if random.random() > 0.5 else "PUT", 60

@app.route('/')
def home():
    return '007Koba Backend Running!'

@app.route('/api/connect', methods=['POST'])
async def connect():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    client = ExpertOptionClient(email, password)
    connected = await client.connect()
    
    if connected:
        user_sessions[email] = client
        return jsonify({
            "success": True, 
            "message": "Connected to ExpertOption",
            "balance": client.balance
        })
    else:
        return jsonify({"success": False, "error": "Connection failed"})

@app.route('/api/balance', methods=['POST'])
async def get_balance():
    data = request.json
    email = data.get('email')
    client = user_sessions.get(email)
    
    if not client:
        return jsonify({"success": False, "error": "Connect first"})
    
    balance = await client.get_balance()
    return jsonify({"success": True, "balance": balance})

@app.route('/api/real-signal', methods=['GET'])
async def get_real_signal():
    """রিয়েল মার্কেট ডাটা থেকে সিগন্যাল জেনারেট করে"""
    
    # Binance থেকে রিয়েল প্রাইস নাও
    current_price = await get_real_price("BTCUSDT")
    historical_prices = await get_historical_prices("BTCUSDT", 5)
    
    if current_price and historical_prices:
        signal, confidence = calculate_signal_from_prices(historical_prices)
        return jsonify({
            "success": True,
            "signal": signal,
            "confidence": confidence,
            "current_price": current_price,
            "asset": "BTC/USDT",
            "timestamp": datetime.now().isoformat()
        })
    else:
        # API ব্যর্থ হলে সিমুলেটেড সিগন্যাল
        signal = "CALL" if random.random() > 0.5 else "PUT"
        return jsonify({
            "success": True,
            "signal": signal,
            "confidence": random.randint(60, 85),
            "current_price": None,
            "asset": "BTC/USDT (Simulated)",
            "timestamp": datetime.now().isoformat()
        })

@app.route('/api/trade', methods=['POST'])
async def trade():
    data = request.json
    email = data.get('email')
    signal = data.get('signal')
    amount = data.get('amount', 10)
    
    client = user_sessions.get(email)
    if not client:
        return jsonify({"success": False, "error": "Connect first"})
    
    result = await client.place_trade(signal, amount)
    return jsonify({
        "success": True,
        "result": result["result"],
        "profit": result["profit"],
        "new_balance": result["new_balance"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
