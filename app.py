from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

user_sessions = {}

# মার্কেটের তালিকা
MARKETS = {
    "crypto": {"name": "BTC/USDT", "price_range": (65000, 70000)},
    "forex": {"name": "EUR/USD", "price_range": (1.05, 1.15)}
}

@app.route('/')
def home():
    return '007Koba Backend Running!'

@app.route('/api/connect', methods=['POST'])
def connect():
    data = request.json
    email = data.get('email')
    market = data.get('market', 'crypto')  # crypto বা forex
    
    user_sessions[email] = {
        "balance": 10000,
        "connected": True,
        "market": market
    }
    
    return jsonify({
        "success": True,
        "message": f"Connected to {market.upper()} market",
        "balance": 10000
    })

@app.route('/api/balance', methods=['POST'])
def get_balance():
    data = request.json
    email = data.get('email')
    
    if email not in user_sessions:
        return jsonify({"success": False, "error": "Connect first"})
    
    return jsonify({
        "success": True,
        "balance": user_sessions[email]["balance"]
    })

@app.route('/api/real-signal', methods=['GET'])
def real_signal():
    market_type = request.args.get('market', 'crypto')
    
    if market_type == "forex":
        signal = "CALL" if random.random() > 0.5 else "PUT"
        confidence = random.randint(70, 92)
        price = round(random.uniform(1.05, 1.15), 5)
        asset = "EUR/USD"
    else:
        signal = "CALL" if random.random() > 0.5 else "PUT"
        confidence = random.randint(65, 95)
        price = random.randint(65000, 70000)
        asset = "BTC/USDT"
    
    return jsonify({
        "success": True,
        "signal": signal,
        "confidence": confidence,
        "current_price": price,
        "asset": asset,
        "market": market_type,
        "timestamp": datetime.now().isoformat()
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
