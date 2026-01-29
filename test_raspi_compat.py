from src.engine_raspi_compat import OpinionBasedEngine

engine = OpinionBasedEngine()

print("\\n\\n🔴 テストケース1: BTC 買い")
engine.execute({"symbol": "BTC", "rsi": 55, "expected_return": 18, "varp": 3.2, "position_size": 25})

print("\\n\\n🟠 テストケース2: ETH リスク")
engine.execute({"symbol": "ETH", "rsi": 75, "expected_return": 12, "varp": 9.5, "position_size": 45})

print("\\n\\n🔴 テストケース3: ALT 全員反対")
engine.execute({"symbol": "ALT", "rsi": 85, "expected_return": 3, "varp": 12, "position_size": 50})

print("\\n✅ テスト完了！")
