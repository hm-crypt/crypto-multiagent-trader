import asyncio
import json
from datetime import datetime
from typing import List
import time
from src.agents import (
    TradeSignal, AgentDecision, MaedaToshiie, OdaNobunaga,
    AkechiMitsuhide, ShibataMasanie, ToyotomiHideyoshi
)

class MultiAgentEngine:
    """複数エージェントの並列実行エンジン"""
    
    def __init__(self):
        self.agents = [
            MaedaToshiie(),
            OdaNobunaga(),
            AkechiMitsuhide(),
            ShibataMasanie()
        ]
        self.moderator = ToyotomiHideyoshi()
        self.start_time = datetime.now()
        self.conference_logs = []
    
    def format_log(self, elapsed_ms: float, message: str) -> str:
        """ログメッセージをフォーマット"""
        total_seconds = (datetime.now() - self.start_time).total_seconds()
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        milliseconds = int((total_seconds % 1) * 1000)
        
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        return f"[{time_str}] {message}"
    
    async def execute(self, signal: TradeSignal):
        """シグナルを処理"""
        start = time.time()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "signal": {
                "symbol": signal.symbol,
                "action": signal.action,
                "position_size": signal.position_size
            },
            "decisions": []
        }
        
        print("\\n" + "="*70)
        print(self.format_log(0, f"🎯 新規シグナル: {signal.symbol} {signal.action.upper()} (ポジション{signal.position_size:.0f}%)"))
        print("="*70)
        
        # 1. 各エージェントが並列で判定
        tasks = [agent.judge(signal) for agent in self.agents]
        decisions = await asyncio.gather(*tasks)
        
        # 2. 各判定をログ出力
        for decision in decisions:
            elapsed = (time.time() - start) * 1000
            symbol = "✅" if decision.decision == "OK" else "❌" if decision.decision == "NG" else "🟡"
            print(self.format_log(elapsed, 
                f"{decision.emoji} {decision.agent_name}: {symbol} {decision.decision} - {decision.reason}"))
            
            log_entry["decisions"].append({
                "agent": decision.agent_name,
                "decision": decision.decision,
                "reason": decision.reason
            })
        
        # 3. 豊臣秀吉が総合判定
        final_decision = await self.moderator.judge(signal, decisions)
        elapsed = (time.time() - start) * 1000
        symbol = "✅" if final_decision.decision == "OK" else "❌"
        print(self.format_log(elapsed, 
            f"{self.moderator.emoji} {self.moderator.name}: {symbol} {final_decision.decision}"))
        print(self.format_log(elapsed, 
            f"   └─ {final_decision.reason}"))
        
        # 4. 最終判定
        elapsed = (time.time() - start) * 1000
        if final_decision.decision == "OK":
            print(self.format_log(elapsed, 
                f"✅ 【最終判定】全員一致・実行\\n   タイムスタンプ: {datetime.now().isoformat()}"))
        else:
            print(self.format_log(elapsed, 
                f"❌ 【最終判定】却下\\n   見送り中..."))
        
        print("="*70 + "\\n")
        
        log_entry["final_decision"] = final_decision.decision
        log_entry["final_reason"] = final_decision.reason
        self.conference_logs.append(log_entry)
        
        return final_decision
    
    def save_logs(self, filename: str):
        """ログをファイルに保存"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conference_logs, f, indent=2, ensure_ascii=False)
        print(f"✅ ログを保存しました: {filename}")
