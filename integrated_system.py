#!/usr/bin/env python3
"""
統合スクリプト: MacBook Pro ↔ RasPi 通信
1. RasPi から市場データを取得
2. マルチエージェント判定を実行
3. RasPi に判定結果を送信して取引実行
"""

import asyncio
import requests
import json
from datetime import datetime
from src.agents import TradeSignal
from src.engine import MultiAgentEngine

class IntegratedSystem:
    """MacBook Pro ↔ RasPi 統合システム"""
    
    def __init__(self, raspi_url="http://localhost:5000"):
        self.raspi_url = raspi_url
        self.engine = MultiAgentEngine()
    
    def fetch_market_data(self, symbol="BTCUSDT"):
        """RasPi から市場データを取得"""
        try:
            response = requests.get(
                f"{self.raspi_url}/market_data",
                params={"symbol": symbol},
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"❌ RasPi 接続エラー: {e}")
            return None
    
    def send_decision_to_raspi(self, decision, symbol, position_size, conference_log):
        """判定結果を RasPi に送信"""
        payload = {
            "decision": decision,
            "symbol": symbol,
            "position_size": position_size,
            "conference_log": conference_log,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                f"{self.raspi_url}/execute_trade",
                json=payload,
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"❌ RasPi 送信エラー: {e}")
            return None
    
    async def process_trading_signal(self, symbol="BTCUSDT", position_size=25, expected_return=18):
        """取引シグナルを処理（市場データ取得 → 判定 → 実行）"""
        
        print(f"\\n【開始】{symbol} の取引シグナル処理")
        print("=" * 70)
        
        # Step 1: RasPi から市場データ取得
        print(f"📥 RasPi から {symbol} の市場データを取得中...")
        market_data = self.fetch_market_data(symbol)
        
        if not market_data:
            print("❌ 市場データ取得失敗。中止します")
            return
        
        print(f"✅ 市場データ取得完了")
        print(f"   価格: , RSI: {market_data['rsi']:.1f}")
        
        # Step 2: TradeSignal に変換
        signal = TradeSignal(
            symbol=symbol,
            action="buy",
            position_size=position_size,
            expected_return=expected_return,
            varp=market_data.get('volatility_ratio', 3.0) * 3.2,
            rsi=market_data.get('rsi', 55),
            bollin_position=0.3,
            volatility_ratio=market_data.get('volatility_ratio', 0.95),
            correlation=market_data.get('correlation_with_portfolio', 0.5),
            fundamentals_score=market_data.get('fundamentals_score', 78)
        )
        
        # Step 3: マルチエージェント判定実行
        print(f"\\n⚖️  5人の武将による判定会議を実行中...")
        final_decision = await self.engine.execute(signal)
        
        # Step 4: RasPi に送信
        if final_decision.decision == "OK":
            print(f"\\n📤 RasPi に実行指示を送信中...")
            result = self.send_decision_to_raspi(
                final_decision.decision,
                symbol,
                position_size,
                self.engine.conference_logs[-1] if self.engine.conference_logs else {}
            )
            
            if result and result.get('status') == 'success':
                print(f"✅ 取引実行完了！")
                print(f"   Trade ID: {result.get('trade_id')}")
                print(f"   Order ID: {result.get('order_id')}")
            else:
                print(f"❌ RasPi での取引実行に失敗")
                print(f"   {result}")
        else:
            print(f"\\n❌ 全員一致に達しませんでした。取引見送り")
        
        print("=" * 70)

async def main():
    """メイン処理"""
    system = IntegratedSystem()
    
    # テストケース
    print("\\n🎭 MacBook Pro ↔ RasPi 統合テスト")
    
    # テスト1: BTC買い
    await system.process_trading_signal(
        symbol="BTC",
        position_size=25,
        expected_return=18
    )
    
    # テスト2: ETH買い（条件付き）
    await system.process_trading_signal(
        symbol="ETH",
        position_size=45,
        expected_return=12
    )

if __name__ == "__main__":
    asyncio.run(main())
