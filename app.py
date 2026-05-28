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
    
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

user_sessions = {}

@app.route('/')
def home():
    return '007Koba Backend Running!'

@app.route('/api/connect', methods=['POST'])
def connect():
    data = request.json
    email = data.get('email')
    user_sessions[email] = {"balance": 10000, "connected": True}
    return jsonify({"success": True, "balance": 10000})

@app.route('/api/real-signal', methods=['GET'])
def real_signal():
    signal = "CALL" if random.random() > 0.5 else "PUT"
    confidence = random.randint(65, 95)
    btc_price = random.randint(65000, 70000)
    return jsonify({
        "success": True,
        "signal": signal,
        "confidence": confidence,
        "current_price": btc_price,
        "asset": "BTC/USDT"
    })

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    email = data.get('email')
    signal = data.get('signal')
    amount = data.get('amount', 10)
    
    if email not in user_sessions:
        return jsonify({"success": False, "error": "Connect first"})
    
    is_win = random.random() < 0.7
    profit = amount * 0.85 if is_win else -amount
    user_sessions[email]["balance"] += profit
    
    return jsonify({
        "success": True,
        "result": "WIN" if is_win else "LOSS",
        "profit": round(profit, 2),
        "new_balance": round(user_sessions[email]["balance"], 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
