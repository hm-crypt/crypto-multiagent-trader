from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

# ダミーデータベース（実際は RasPi の取引DB）
trades_log = []
current_positions = {
    "BTC": {"quantity": 2.5, "avg_price": 42000},
    "ETH": {"quantity": 15.0, "avg_price": 2200}
}

@app.route('/market_data', methods=['GET'])
def get_market_data():
    """市場データを返す（MacBook Pro が呼び出す）"""
    symbol = request.args.get('symbol', 'BTCUSDT')
    
    # ダミーデータ
    market_data = {
        "symbol": symbol,
        "current_price": 45230.50 if symbol == "BTC" else 2850.25,
        "rsi": 55.2,
        "bollinger_upper": 46100,
        "bollinger_lower": 44200,
        "bollinger_middle": 45150,
        "volatility_ratio": 0.95,
        "volume_24h": 28500000,
        "fundamentals_score": 78,
        "correlation_with_portfolio": 0.52,
        "order_book": {
            "bid": [
                {"price": 45220, "volume": 2.5},
                {"price": 45210, "volume": 1.8},
            ],
            "ask": [
                {"price": 45240, "volume": 3.0},
                {"price": 45250, "volume": 2.2},
            ]
        }
    }
    return jsonify(market_data)

@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    """MacBook Pro からの全員一致判定を受けて、実取引を実行"""
    data = request.json
    decision = data.get('decision')
    
    # Step 1: 全員一致確認
    if decision != "OK":
        return jsonify({
            "status": "rejected",
            "reason": "マルチエージェント全員一致に達しませんでした"
        }), 400
    
    # Step 2: ダミー取引実行
    trade_id = f"TRD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    order_id = f"O_{datetime.now().strftime('%Y%m%d%H%M%S')}67890"
    
    trade_record = {
        "trade_id": trade_id,
        "order_id": order_id,
        "symbol": data.get('symbol'),
        "position_size": data.get('position_size'),
        "timestamp": datetime.now().isoformat(),
        "status": "executed",
        "conference_log": data.get('conference_log')
    }
    trades_log.append(trade_record)
    
    return jsonify({
        "status": "success",
        "trade_id": trade_id,
        "order_id": order_id,
        "message": f"取引実行完了: {trade_id}"
    })

@app.route('/trade_history', methods=['GET'])
def get_trade_history():
    """取引履歴を返す"""
    return jsonify(trades_log)

@app.route('/positions', methods=['GET'])
def get_positions():
    """現在のポジションを返す"""
    return jsonify(current_positions)

@app.route('/health', methods=['GET'])
def health():
    """ヘルスチェック"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    print("🚀 RasPi Trade Engine API サーバー起動")
    print("   http://localhost:5000")
    print("   GET  /market_data?symbol=BTC")
    print("   POST /execute_trade")
    print("   GET  /trade_history")
    print("   GET  /positions")
    app.run(host='127.0.0.1', port=5000, debug=True)
