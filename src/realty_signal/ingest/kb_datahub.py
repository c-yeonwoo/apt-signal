"""KB 데이터허브 자동 수집 — data-api.kbland.kr 공개 JSON API 직접 호출.

엑셀 수동 다운로드를 대체한다. 표준 라이브러리(urllib)만 사용해
의존성 충돌/세그폴트 없이 동작하며, kb_weekly.load() 와 동일한
tidy long(date, region, metric, value) 형태를 반환한다.

수집 지표(전국 등 24개 광역 단위, 주간):
  매수우위지수(buyer_superiority), 매수세우위(buyer_demand),
  전세수급지수(jeonse_supply), 매매증감률(sale_change), 전세증감률(jeonse_change)
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

import pandas as pd

from realty_signal.ingest.kb_weekly import KBWeekly


def _parse_date(s: str) -> pd.Timestamp:
    """'YYYYMMDD' → Timestamp. pd.to_datetime(format=) 는 일부 파이썬 빌드에서
    스칼라 파싱 시 세그폴트가 나므로 슬라이싱으로 안전하게 구성한다."""
    s = str(s)
    return pd.Timestamp(year=int(s[:4]), month=int(s[4:6]), day=int(s[6:8]))

_BASE = "https://data-api.kbland.kr/bfmstat/weekMnthlyHuseTrnd/"
_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
_WEEKLY = "02"

# 시장동향(maktTrnd) 메뉴코드 → {응답 키: metric}
_TREND = {
    "01": {"매수우위지수": "buyer_superiority", "매수자많음": "buyer_demand"},
    "03": {"전세수급지수": "jeonse_supply"},
}
# 증감률(prcIndxInxrdcRt) 매매전세코드 → metric  (매물종별 01=아파트)
_CHANGE = {"01": "sale_change", "02": "jeonse_change"}


def _get(path: str, params: dict) -> dict:
    url = _BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (고정 https 도메인)
        body = json.load(r)
    db = body.get("dataBody", {})
    if str(db.get("resultCode")) != "11000":
        raise RuntimeError(f"KB API 오류({path}): resultCode={db.get('resultCode')}")
    return db["data"]


def fetch() -> KBWeekly:
    """KB 데이터허브에서 최신 주간 지표를 받아 KBWeekly 로 반환."""
    rows: list[tuple] = []

    for menu, key_map in _TREND.items():
        data = _get("maktTrnd", {"메뉴코드": menu, "월간주간구분코드": _WEEKLY})
        for rec in data["데이터리스트"]:
            region = rec["지역명"]
            for item in rec["dataList"]:
                date = _parse_date(item["기준날짜"])
                for src_key, metric in key_map.items():
                    v = item.get(src_key)
                    if v is not None:
                        rows.append((date, region, metric, float(v)))

    for code, metric in _CHANGE.items():
        data = _get(
            "prcIndxInxrdcRt",
            {"월간주간구분코드": _WEEKLY, "매물종별구분": "01", "매매전세코드": code},
        )
        dates = [_parse_date(s) for s in data["날짜리스트"]]
        for rec in data["데이터리스트"]:
            region = rec["지역명"]
            for i, v in enumerate(rec["dataList"]):
                if v is not None and i < len(dates):
                    rows.append((dates[i], region, metric, float(v)))

    long = pd.DataFrame(rows, columns=["date", "region", "metric", "value"])
    return KBWeekly(long=long)
