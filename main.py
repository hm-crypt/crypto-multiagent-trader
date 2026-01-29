#!/usr/bin/env python3

import asyncio
import sys
from src.agents import TradeSignal
from src.engine import MultiAgentEngine

async def run_tests():
    """複数シナリオを実行"""
    engine = MultiAgentEngine()
    
    # テストケース1: 全員OK
    print("\\n\\n🔴 テストケース1: スムーズに全員一致")
    signal1 = TradeSignal(
        symbol="BTC",
        action="buy",
        position_size=25,
        expected_return=18,
        varp=3.2,
        rsi=55,
        bollin_position=0.3,
        volatility_ratio=0.9,
        correlation=0.5,
        fundamentals_score=78
    )
    await engine.execute(signal1)
    
    # テストケース2: 条件付きで修正
    print("\\n\\n🟠 テストケース2: 条件付きで修正・実行")
    signal2 = TradeSignal(
        symbol="ETH",
        action="buy",
        position_size=45,
        expected_return=12,
        varp=8.5,
        rsi=52,
        bollin_position=0.2,
        volatility_ratio=1.1,
        correlation=0.65,
        fundamentals_score=65
    )
    await engine.execute(signal2)
    
    # テストケース3: NGで却下
    print("\\n\\n🔴 テストケース3: リスク高すぎで却下")
    signal3 = TradeSignal(
        symbol="新規ALT",
        action="buy",
        position_size=50,
        expected_return=25,
        varp=12,
        rsi=85,
        bollin_position=-1.3,
        volatility_ratio=2.1,
        correlation=0.92,
        fundamentals_score=35
    )
    await engine.execute(signal3)
    
    # ログを保存
    engine.save_logs("logs/conference_log.json")

if __name__ == "__main__":
    print("🎭 5人の戦国武将 マルチエージェント実行エンジン")
    print("=" * 70)
    asyncio.run(run_tests())
    print("✅ テスト完了！")
