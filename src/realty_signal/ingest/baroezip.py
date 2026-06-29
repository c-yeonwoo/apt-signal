"""개인용 급매 레이더 — baroezip 공개 spatialmarket API (인증/서명 없음).

⚠️ 개인용·로컬 확인 전용. 데이터 원천은 네이버 부동산 매물(complex_no=네이버 단지번호)이며
baroezip이 집계·노출한다. 재배포/상업이용 금지(부정경쟁방지법·각 사 ToS). 저빈도로만 호출.

각 매물: 호가(deal_amount) + 그 평형 중위시세(median_deal_amount) + is_urgent(급매).
급매 갭 = (호가 − 중위시세)/중위시세. 음수가 클수록 시세 대비 싸다.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

_URL = "https://baroezip.com/api/apartment/spatialmarket"
_HDR = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json"}


def fetch_market(lat1: float, lng1: float, lat2: float, lng2: float) -> list[dict]:
    """bbox 내 매물 목록(개별 호가). 단지별 market_data를 평탄화."""
    q = urllib.parse.urlencode({"latitude_1": lat1, "longitude_1": lng1,
                                "latitude_2": lat2, "longitude_2": lng2})
    try:
        raw = urllib.request.urlopen(  # noqa: S310
            urllib.request.Request(f"{_URL}?{q}", headers=_HDR), timeout=25).read()
        data = json.loads(raw).get("data", [])
    except Exception:
        return []

    out = []
    for grp in data:
        al = grp.get("apt_list", {})
        for m in grp.get("market_data", []):
            호가 = m.get("deal_amount")
            중위 = m.get("median_deal_amount")
            if not 호가:
                continue
            gap = round((호가 - 중위) / 중위 * 100, 1) if 중위 else None
            out.append({
                "단지명": m.get("complex_name") or al.get("complex_name"),
                "complex_no": m.get("complex_no") or al.get("complex_no"),  # 네이버 단지번호
                "평형": m.get("pyeong_name"),
                "전용면적": m.get("exclusive_use_area"),
                "층": m.get("floor"),
                "방향": m.get("direction"),
                "거래": m.get("trade_type"),                 # trade=매매
                "호가": 호가,
                "중위시세": 중위,
                "급매갭": gap,                                # % (음수=시세 이하)
                "급매": bool(m.get("is_urgent")),
                "세대수": al.get("total_household_count"),
                "연식": (al.get("use_approve_ymd") or "")[:4] or None,
                "lat": al.get("latitude"),
                "lng": al.get("longitude"),
                "naver_id": m.get("original"),               # 네이버 매물 id
            })
    return out


def bbox_around(lat: float, lng: float, dlat: float = 0.05, dlng: float = 0.06) -> tuple:
    """중심좌표 → (lat1,lng1,lat2,lng2). 시군구 1개를 대략 덮는 박스."""
    return (lat - dlat, lng - dlng, lat + dlat, lng + dlng)
