import pandas as pd

from realty_signal.ingest.kb_weekly import _clean_region, _normalize_dates
from realty_signal.signals.engine import (
    SignalConfig,
    _buyer_state,
    _jeonse_state,
    _momentum,
    _overall,
)


def test_clean_region():
    assert _clean_region("전국 Total") == "전국"
    assert _clean_region("6개광역시 6 Large Cities") == "6개광역시"
    assert _clean_region("강남 Southern Seoul") == "강남"


def test_normalize_dates_carries_year_and_rollover():
    from datetime import datetime

    raw = [datetime(2008, 4, 14), "4.21", "4.28", "5.5", "12.29", "1.5"]
    out = _normalize_dates(raw)
    assert out[0] == pd.Timestamp(2008, 4, 14)
    assert out[1] == pd.Timestamp(2008, 4, 21)
    assert out[3] == pd.Timestamp(2008, 5, 5)
    # 12 → 1 로 줄면 연도 증가
    assert out[4] == pd.Timestamp(2008, 12, 29)
    assert out[5] == pd.Timestamp(2009, 1, 5)


def test_jeonse_state_bands():
    c = SignalConfig()
    assert _jeonse_state(90, c) == "공급우위"
    assert _jeonse_state(130, c) == "보통"
    assert _jeonse_state(160, c) == "타이트"
    assert _jeonse_state(180, c) == "전세난"
    assert _jeonse_state(195, c) == "매매전이"


def test_buyer_state_bands():
    c = SignalConfig()
    assert _buyer_state(30, c) == "매수위축"
    assert _buyer_state(50, c) == "매도우위"
    assert _buyer_state(70, c) == "매수우위"
    assert _buyer_state(90, c) == "매수강세"


def test_momentum_labels():
    c = SignalConfig(momentum_weeks=4, momentum_up=0.05, momentum_down=-0.05)
    up = pd.Series([0.1, 0.2, 0.15, 0.3])
    down = pd.Series([-0.1, -0.2, -0.15, -0.3])
    flat = pd.Series([0.0, 0.01, -0.01, 0.0])
    assert _momentum(up, c)[1] == "상승"
    assert _momentum(down, c)[1] == "하락"
    assert _momentum(flat, c)[1] == "보합"


def test_overall_strong_buy():
    c = SignalConfig()
    sig, _ = _overall("전세난", "매수우위", "상승", c)
    assert sig == "STRONG_BUY"
    sig, _ = _overall("공급우위", "매수위축", "하락", c)
    assert sig == "SELL_RISK"
