from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class Opinion:
    agent: str
    action: str  # "BUY" | "SELL" | "HOLD" | "BLOCK"
    confidence: float
    reason: str
    meta: Dict[str, Any]

class Agent:
    name: str
    def evaluate(self, ctx: Dict[str, Any]) -> Opinion:
        raise NotImplementedError

class MaedaToshiie(Agent):
    name = "maeda_toshiie"
    def evaluate(self, ctx: Dict[str, Any]) -> Opinion:
        rsi = ctx.get("rsi", 50)
        action = "HOLD"
        confidence = 0.5
        if rsi > 80:
            action = "BLOCK"
            confidence = 0.95
        elif rsi < 20:
            action = "BLOCK"
            confidence = 0.95
        elif rsi > 60:
            action = "BUY"
            confidence = 0.7
        elif rsi < 40:
            action = "SELL"
            confidence = 0.7
        return Opinion(agent=self.name, action=action, confidence=confidence, reason=f"RSI={rsi:.1f}", meta={"rsi": rsi})

class OdaNobunaga(Agent):
    name = "oda_nobunaga"
    def evaluate(self, ctx: Dict[str, Any]) -> Opinion:
        expected_return = ctx.get("expected_return", 10)
        action = "HOLD"
        confidence = 0.5
        if expected_return < 5:
            action = "BLOCK"
            confidence = 0.85
        elif expected_return > 20:
            action = "BUY"
            confidence = 0.9
        elif expected_return > 10:
            action = "BUY"
            confidence = 0.7
        return Opinion(agent=self.name, action=action, confidence=confidence, reason=f"期待リターン{expected_return:.1f}%", meta={"expected_return": expected_return})
    
    def decide(self, ctx: Dict[str, Any], opinions: List[Opinion]) -> Opinion:
        blockers = [o for o in opinions if o.action == "BLOCK"]
        if blockers:
            return Opinion(agent=self.name, action="BLOCK", confidence=0.95, reason=f"反対意見あり", meta={})
        buy_count = sum(1 for o in opinions if o.action == "BUY")
        if buy_count >= 3:
            return Opinion(agent=self.name, action="BUY", confidence=0.8, reason=f"買い優勢({buy_count}人)", meta={"buy_count": buy_count})
        return Opinion(agent=self.name, action="HOLD", confidence=0.5, reason="優位性不足", meta={})

class AkechiMitsuhide(Agent):
    name = "akechi_mitsuhide"
    def evaluate(self, ctx: Dict[str, Any]) -> Opinion:
        varp = ctx.get("varp", 3.0)
        action = "HOLD"
        confidence = 0.5
        if varp > 10:
            action = "BLOCK"
            confidence = 0.95
        elif varp > 6:
            action = "SELL"
            confidence = 0.8
        else:
            action = "BUY"
            confidence = 0.7
        return Opinion(agent=self.name, action=action, confidence=confidence, reason=f"VaR={varp:.1f}%", meta={"varp": varp})

class ShibataMasanie(Agent):
    name = "shibata_katsuie"
    def evaluate(self, ctx: Dict[str, Any]) -> Opinion:
        concentration = ctx.get("position_size", 20)
        action = "HOLD"
        confidence = 0.5
        if concentration > 120:
            action = "BLOCK"
            confidence = 0.9
        elif concentration > 100:
            action = "SELL"
            confidence = 0.7
        return Opinion(agent=self.name, action=action, confidence=confidence, reason=f"集中度{concentration:.0f}%", meta={"concentration": concentration})

class ToyotomiHideyoshi(Agent):
    name = "toyotomi_hideyoshi"
    def evaluate(self, ctx: Dict[str, Any]) -> Opinion:
        return Opinion(agent=self.name, action="HOLD", confidence=0.5, reason="Not used", meta={})
    
    def decide(self, ctx: Dict[str, Any], opinions: List[Opinion]) -> Opinion:
        blockers = [o for o in opinions if o.action == "BLOCK"]
        if blockers:
            return Opinion(agent=self.name, action="BLOCK", confidence=0.95, reason=f"反対意見あり({len(blockers)}人)", meta={})
        buy_count = sum(1 for o in opinions if o.action == "BUY")
        if buy_count >= 3:
            return Opinion(agent=self.name, action="BUY", confidence=0.8, reason=f"全員一致({buy_count}人)", meta={"buy_count": buy_count})
        return Opinion(agent=self.name, action="HOLD", confidence=0.6, reason=f"全員一致なし(買:{buy_count})", meta={})
