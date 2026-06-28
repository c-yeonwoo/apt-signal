from realty_signal.ingest.locality import score_undervaluation


def test_undervaluation_ranks_cheap_for_locality():
    # 입지 좋은데 싼 B가 저평가 1위여야
    rows = [
        {"region": "A", "price": 10000, "accessibility": 90, "school": 90, "env": 90},  # 입지최고·비쌈
        {"region": "B", "price": 6000,  "accessibility": 85, "school": 85, "env": 85},  # 입지높은데 쌈 → 저평가
        {"region": "C", "price": 6000,  "accessibility": 20, "school": 20, "env": 20},  # 입지낮음·적정
        {"region": "D", "price": 9000,  "accessibility": 50, "school": 50, "env": 50},  # 입지중간·비쌈→고평가
    ]
    out = score_undervaluation(rows)
    assert out[0]["region"] == "B"
    assert out[0]["저평가도"] > 0
    # 입지점수는 0~100
    assert all(0 <= r["입지점수"] <= 100 for r in out)
