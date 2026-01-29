import asyncio
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Literal

@dataclass
class TradeSignal:
    """取引シグナル"""
    symbol: str
    action: str
    position_size: float
    expected_return: float
    varp: float
    rsi: float
    bollin_position: float
    volatility_ratio: float
    correlation: float
    fundamentals_score: float

@dataclass
class AgentDecision:
    """エージェントの判定結果"""
    agent_name: str
    emoji: str
    timestamp_ms: float
    decision: Literal["OK", "NG", "条件付き"]
    reason: str
    conditions: Dict = None

class Agent:
    """基底エージェントクラス"""
    def __init__(self, name: str, emoji: str):
        self.name = name
        self.emoji = emoji
    
    async def judge(self, signal: TradeSignal) -> AgentDecision:
        raise NotImplementedError

class MaedaToshiie(Agent):
    """前田利家: テクニカル分析者"""
    def __init__(self):
        super().__init__("前田利家", "📊")
    
    async def judge(self, signal: TradeSignal) -> AgentDecision:
        await asyncio.sleep(0.1)
        
        reasons = []
        decision = "OK"
        
        if signal.rsi < 20 or signal.rsi > 80:
            decision = "NG"
            reasons.append(f"RSI={signal.rsi:.1f}（過熱/過売）")
        else:
            reasons.append(f"RSI={signal.rsi:.1f}OK")
        
        if abs(signal.bollin_position) > 1.2:
            decision = "NG"
            reasons.append(f"ボリンジャーバンド外({signal.bollin_position:.2f})")
        else:
            reasons.append(f"ボリンジャーバンド内OK")
        
        if signal.volatility_ratio > 1.5:
            decision = "NG"
            reasons.append(f"ボラティリティ過高({signal.volatility_ratio:.2f}x)")
        else:
            reasons.append(f"ボラティリティ許容範囲内")
        
        reason_text = " / ".join(reasons)
        return AgentDecision(
            agent_name=self.name,
            emoji=self.emoji,
            timestamp_ms=time.time(),
            decision=decision,
            reason=reason_text
        )

class OdaNobunaga(Agent):
    """織田信長: リターン期待値評価者"""
    def __init__(self):
        super().__init__("織田信長", "🎯")
    
    async def judge(self, signal: TradeSignal) -> AgentDecision:
        await asyncio.sleep(0.1)
        
        reasons = []
        decision = "OK"
        
        if signal.expected_return < 5:
            decision = "NG"
            reasons.append(f"期待リターン{signal.expected_return:.1f}%（つまらん）")
        elif signal.expected_return < 15:
            decision = "条件付き"
            reasons.append(f"期待リターン{signal.expected_return:.1f}%（微妙）")
        else:
            reasons.append(f"期待リターン{signal.expected_return:.1f}%（良好）")
        
        if signal.position_size > 50:
            decision = "NG"
            reasons.append(f"ポジション{signal.position_size:.1f}%（賭けすぎ）")
        else:
            reasons.append(f"ポジション{signal.position_size:.1f}%OK")
        
        sharpe = signal.expected_return / max(signal.varp, 0.1)
        if sharpe < 0.5:
            decision = "NG"
            reasons.append(f"シャープレシオ{sharpe:.2f}（リスク高）")
        else:
            reasons.append(f"シャープレシオ{sharpe:.2f}OK")
        
        reason_text = " / ".join(reasons)
        return AgentDecision(
            agent_name=self.name,
            emoji=self.emoji,
            timestamp_ms=time.time(),
            decision=decision,
            reason=reason_text
        )

class AkechiMitsuhide(Agent):
    """明智光秀: リスク評価者"""
    def __init__(self):
        super().__init__("明智光秀", "🛡️")
    
    async def judge(self, signal: TradeSignal) -> AgentDecision:
        await asyncio.sleep(0.15)
        
        reasons = []
        decision = "OK"
        
        if signal.varp > 10:
            decision = "NG"
            reasons.append(f"VaR={signal.varp:.1f}%（危険）")
        elif signal.varp > 6:
            decision = "条件付き"
            reasons.append(f"VaR={signal.varp:.1f}%（要注意）")
        else:
            reasons.append(f"VaR={signal.varp:.1f}%OK")
        
        max_dd = signal.varp * 2.5
        if max_dd > 25:
            decision = "NG"
            reasons.append(f"最大DD推定{max_dd:.1f}%（致命的）")
        elif max_dd > 15:
            if decision != "NG":
                decision = "条件付き"
            reasons.append(f"最大DD推定{max_dd:.1f}%（限界）")
        else:
            reasons.append(f"最大DD推定{max_dd:.1f}%OK")
        
        if signal.fundamentals_score < 40:
            decision = "NG"
            reasons.append(f"ファンダ{signal.fundamentals_score:.0f}点（危険）")
        elif signal.fundamentals_score < 70:
            if decision != "NG":
                decision = "条件付き"
            reasons.append(f"ファンダ{signal.fundamentals_score:.0f}点（要警戒）")
        else:
            reasons.append(f"ファンダ{signal.fundamentals_score:.0f}点OK")
        
        reason_text = " / ".join(reasons)
        return AgentDecision(
            agent_name=self.name,
            emoji=self.emoji,
            timestamp_ms=time.time(),
            decision=decision,
            reason=reason_text
        )

class ShibataMasanie(Agent):
    """柴田勝家: ポジション監視者"""
    def __init__(self):
        super().__init__("柴田勝家", "🔒")
    
    async def judge(self, signal: TradeSignal) -> AgentDecision:
        await asyncio.sleep(0.08)
        
        reasons = []
        decision = "OK"
        
        concentration = signal.position_size
        if concentration > 120:
            decision = "NG"
            reasons.append(f"ポジション集中度{concentration:.0f}%（過度）")
        elif concentration > 100:
            decision = "条件付き"
            reasons.append(f"ポジション集中度{concentration:.0f}%（ぎりぎり）")
        else:
            reasons.append(f"ポジション集中度{concentration:.0f}%OK")
        
        if signal.correlation > 0.9:
            decision = "NG"
            reasons.append(f"相関{signal.correlation:.2f}（同向リスク）")
        elif signal.correlation > 0.7:
            if decision != "NG":
                decision = "条件付き"
            reasons.append(f"相関{signal.correlation:.2f}（要監視）")
        else:
            reasons.append(f"相関{signal.correlation:.2f}OK")
        
        rr_ratio = signal.expected_return / max(signal.varp, 0.1)
        if rr_ratio < 2.0:
            if decision != "NG":
                decision = "条件付き"
            reasons.append(f"RR比{rr_ratio:.2f}（要確認）")
        else:
            reasons.append(f"RR比{rr_ratio:.2f}OK")
        
        reason_text = " / ".join(reasons)
        return AgentDecision(
            agent_name=self.name,
            emoji=self.emoji,
            timestamp_ms=time.time(),
            decision=decision,
            reason=reason_text
        )

class ToyotomiHideyoshi(Agent):
    """豊臣秀吉: 総合判定者"""
    def __init__(self):
        super().__init__("豊臣秀吉", "⚖️")
    
    async def judge(self, signal: TradeSignal, 
                   other_decisions: List[AgentDecision]) -> AgentDecision:
        await asyncio.sleep(0.2)
        
        ng_count = sum(1 for d in other_decisions if d.decision == "NG")
        conditional_count = sum(1 for d in other_decisions if d.decision == "条件付き")
        
        if ng_count > 0:
            reason = f"誰か1人（{ng_count}人）がNGを出した。全員一致が不可能"
            return AgentDecision(
                agent_name=self.name,
                emoji=self.emoji,
                timestamp_ms=time.time(),
                decision="NG",
                reason=reason
            )
        
        if conditional_count == 0:
            reason = "全員OK。実行する"
            return AgentDecision(
                agent_name=self.name,
                emoji=self.emoji,
                timestamp_ms=time.time(),
                decision="OK",
                reason=reason
            )
        
        reason = f"条件統合中...({conditional_count}人が条件付き) → 修正案で対応可能と判断 → 実行"
        return AgentDecision(
            agent_name=self.name,
            emoji=self.emoji,
            timestamp_ms=time.time(),
            decision="OK",
            reason=reason
        )
