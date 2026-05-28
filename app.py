from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ইউজার ডাটা স্টোর (সিমুলেটেড)
user_sessions = {}

@app.route('/')
def home():
    return '007Koba Backend Running!'

@app.route('/api/connect', methods=['POST'])
def connect():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # সব ইমেইল গ্রহণ করে (ডেমো মোড)
    user_sessions[email] = {
        "balance": 10000,
        "connected": True
    }
    
    return jsonify({
        "success": True,
        "message": "Connected to ExpertOption Demo",
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
    """সিমুলেটেড এআই সিগন্যাল (aiohttp ছাড়া)"""
    
    # রিয়েলিস্টিক সিগন্যাল জেনারেশন
    market_momentum = random.random()
    
    if market_momentum > 0.55:
        signal = "CALL"
        confidence = random.randint(75, 95)
    elif market_momentum < 0.45:
        signal = "PUT"
        confidence = random.randint(75, 95)
    else:
        signal = random.choice(["CALL", "PUT"])
        confidence = random.randint(60, 75)
    
    # সিমুলেটেড BTC প্রাইস
    btc_price = random.randint(65000, 70000)
    
    return jsonify({
        "success": True,
        "signal": signal,
        "confidence": confidence,
        "current_price": btc_price,
        "asset": "BTC/USDT",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    email = data.get('email')
    signal = data.get('signal')  # CALL or PUT
    amount = data.get('amount', 10)
    
    if email not in user_sessions:
        return jsonify({"success": False, "error": "Connect first"})
    
    # ট্রেড ফলাফল (সিগন্যালের সাথে সম্পর্কিত নয়, শুধু 70% সঠিক)
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
    app.run(host='0.0.0.0', port=5000)def real_signal():
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
