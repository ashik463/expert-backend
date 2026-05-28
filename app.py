from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import random
import json

app = Flask(__name__)
CORS(app)

# ডেমো মোডে ডাটা স্টোর
user_sessions = {}

@app.route('/')
def home():
    return '007Koba Backend Running!'

@app.route('/api/connect', methods=['POST'])
def connect():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # ডেমো সংযোগ (সিমুলেশন)
    user_sessions[email] = {"connected": True, "balance": 10000}
    
    return jsonify({
        "success": True, 
        "message": "Connected to ExpertOption Demo",
        "balance": 10000
    })

@app.route('/api/balance', methods=['POST'])
def balance():
    data = request.json
    email = data.get('email')
    
    if email not in user_sessions:
        return jsonify({"success": False, "error": "Connect first"})
    
    return jsonify({
        "success": True,
        "balance": user_sessions[email].get("balance", 10000)
    })

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    email = data.get('email')
    signal = data.get('signal')  # CALL or PUT
    amount = data.get('amount', 10)
    
    if email not in user_sessions:
        return jsonify({"success": False, "error": "Connect first"})
    
    # সিমুলেটেড ট্রেড ফলাফল (70% সঠিক)
    win = random.random() < 0.7
    profit = amount * 0.85 if win else -amount
    
    if win:
        user_sessions[email]["balance"] += profit
    else:
        user_sessions[email]["balance"] += profit  # profit negative
    
    return jsonify({
        "success": True,
        "result": "WIN" if win else "LOSS",
        "profit": profit,
        "new_balance": user_sessions[email]["balance"]
    })

@app.route('/api/signal', methods=['GET'])
def signal():
    # রিয়েল মার্কেট সিমুলেশন
    signals = ["CALL", "PUT"]
    selected = random.choice(signals)
    return jsonify({
        "success": True,
        "signal": selected,
        "confidence": round(random.uniform(65, 95), 1),
        "asset": "EUR/USD"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
