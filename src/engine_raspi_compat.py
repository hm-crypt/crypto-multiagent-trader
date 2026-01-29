from datetime import datetime
from typing import Any, Dict, List
from src.agents_raspi_compat import Opinion, MaedaToshiie, OdaNobunaga, AkechiMitsuhide, ShibataMasanie, ToyotomiHideyoshi

class OpinionBasedEngine:
    def __init__(self):
        self.agents = [MaedaToshiie(), OdaNobunaga(), AkechiMitsuhide(), ShibataMasanie()]
        self.moderator = ToyotomiHideyoshi()
        self.start_time = datetime.now()
    
    def format_log(self, message: str) -> str:
        elapsed = (datetime.now() - self.start_time).total_seconds()
        minutes = int(elapsed) // 60
        seconds = int(elapsed) % 60
        ms = int((elapsed % 1) * 1000)
        return f"[{minutes:02d}:{seconds:02d}.{ms:03d}] {message}"
    
    def execute(self, ctx: Dict[str, Any]) -> Opinion:
        print("\\n" + "="*70)
        symbol = ctx.get("symbol", "BTC")
        print(self.format_log(f"🎯 シグナル: {symbol}"))
        print("="*70)
        
        opinions = []
        for agent in self.agents:
            opinion = agent.evaluate(ctx)
            opinions.append(opinion)
            emoji = "✅" if opinion.action == "BUY" else "❌" if opinion.action == "SELL" else "🟡" if opinion.action == "HOLD" else "🚫"
            print(self.format_log(f"  {opinion.agent}: {emoji} {opinion.action} (信頼度 {opinion.confidence:.2f}) - {opinion.reason}"))
        
        final = self.moderator.decide(ctx, opinions)
        emoji = "✅" if final.action == "BUY" else "❌" if final.action == "SELL" else "🟡"
        print(self.format_log(f"  {final.agent}: {emoji} {final.action} (信頼度 {final.confidence:.2f}) - {final.reason}"))
        print("="*70)
        return final
