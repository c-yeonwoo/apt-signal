"""아파트 입주물량 수집 — 매도/끝물 시그널의 핵심 입력.

KB land API(aptMovinCnt)로 지역별 연도별 입주 세대수(미래 예측 포함)를 받아
'공급압력 = 향후 입주물량 / 과거 평균'을 산출한다.

공급압력↑ → 입주 폭탄 → 매도/가격하락 압력 (원본 메모: "아파트 공급이 늘어날 때 하락").
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

import pandas as pd

_URL = "https://api.kbland.kr/land-extra/lots/v1/api/aptMovinCnt"
_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

FUTURE_YEARS = 3   # 향후 입주 윈도(예측 포함)
BASE_YEARS = 5     # 과거 평균 기준 윈도


def _get(beopjeong_code: str, 기간구분: str = "1") -> dict | None:
    params = {"기간구분": 기간구분, "법정동코드": str(beopjeong_code).ljust(10, "0")}
    url = _URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310
        body = json.load(r)
    data = body.get("dataBody", {}).get("data")
    return data


def _supply_pressure(chart: list[dict]) -> dict | None:
    """연도별 차트데이터 → 공급압력 지표."""
    pts = []
    for c in chart:
        try:
            year = int(str(c["일정"])[:4])
            units = c.get("합계", {}).get("세대수")
            if units is not None:
                pts.append((year, float(units)))
        except (ValueError, TypeError, KeyError):
            continue
    if len(pts) < FUTURE_YEARS + BASE_YEARS:
        return None
    pts.sort()
    max_y = pts[-1][0]
    fut = [u for y, u in pts if y > max_y - FUTURE_YEARS]
    base = [u for y, u in pts if max_y - FUTURE_YEARS - BASE_YEARS < y <= max_y - FUTURE_YEARS]
    if not fut or not base or sum(base) == 0:
        return None
    fut_avg = sum(fut) / len(fut)
    base_avg = sum(base) / len(base)
    return {
        "future_units": round(fut_avg),
        "base_units": round(base_avg),
        "supply_pressure": round(fut_avg / base_avg, 2),
        "future_to": max_y,
    }


def fetch_supply(codes: dict[str, str]) -> pd.DataFrame:
    """지역명→법정동코드 맵으로 입주물량 공급압력 테이블 산출.

    집계지역(코드에 영문 포함)·전국은 제외하고 10자리 법정동코드만 조회한다.
    """
    rows = []
    for region, code in codes.items():
        if not code or not code.isdigit() or code == "0000000000":
            continue
        try:
            data = _get(code)
        except Exception:
            continue
        if not data or "차트데이터" not in data:
            continue
        sp = _supply_pressure(data["차트데이터"])
        if sp:
            rows.append({"region": region, **sp})
    return pd.DataFrame(rows)
