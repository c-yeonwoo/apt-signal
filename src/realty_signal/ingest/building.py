"""건축물대장 — 용적률·건폐율·사용승인일(연식)·세대수·층수 (건축HUB, data.go.kr 키).

국토부 실거래 응답의 sggCd/umdCd/bonbun/bubun(모두 4자리 zero-pad)으로 곧장 조회.
지오코딩·법정동코드 변환 불필요. 아파트는 지번에 여러 동(棟)이 잡히므로 단지 단위로 집계한다.

  - 동별 표제부(getBrTitleInfo)    → 세대수(합)·사용승인일(최이른)·최고층
  - 총괄표제부(getBrRecapTitleInfo) → 단지 용적률·건폐율 (동별 표제부엔 0으로만 기재됨)
"""

from __future__ import annotations

import urllib.request
import xml.etree.ElementTree as ET

_BASE = "https://apis.data.go.kr/1613000/BldRgstHubService"
_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
_HDR = {"User-Agent": _UA, "Accept": "*/*"}  # 건축HUB는 Accept 없으면 200+빈body


def _items(ep: str, sgg: str, umd: str, bonbun: str, bubun: str, key: str) -> list:
    url = (f"{_BASE}/{ep}?serviceKey={key}&sigunguCd={sgg}&bjdongCd={umd}"
           f"&platGbCd=0&bun={bonbun}&ji={bubun}&numOfRows=100&pageNo=1")
    try:
        root = ET.fromstring(urllib.request.urlopen(  # noqa: S310
            urllib.request.Request(url, headers=_HDR), timeout=30).read())
        return list(root.iter("item"))
    except Exception:
        return []


def _f(it, tag: str) -> float:
    try:
        return float(it.findtext(tag) or 0)
    except ValueError:
        return 0.0


def fetch_building(sgg: str, umd: str, bonbun: str, bubun: str, key: str) -> dict | None:
    """지번 → 단지 단위 {용적률, 건폐율, 사용승인일, 세대수, 최고층}. 데이터 없으면 None."""
    # 동별 표제부: 세대수·연식·층
    useaps, hhlds, flrs = [], [], []
    for it in _items("getBrTitleInfo", sgg, umd, bonbun, bubun, key):
        if "총괄" in (it.findtext("regstrKindCdNm") or ""):
            continue
        ua = (it.findtext("useAprDay") or "").strip()
        if ua.isdigit() and len(ua) == 8:
            useaps.append(ua)
        purps = (it.findtext("mainPurpsCdNm") or "") + (it.findtext("etcPurps") or "")
        hh = int(_f(it, "hhldCnt"))
        if hh > 0 and ("공동주택" in purps or "주거" in purps):
            hhlds.append(hh)
        fl = int(_f(it, "grndFlrCnt"))
        if fl > 0:
            flrs.append(fl)

    # 총괄표제부: 단지 용적률·건폐율 (+세대수 fallback)
    vlrat = bcrat = None
    recap_hhld = 0
    for it in _items("getBrRecapTitleInfo", sgg, umd, bonbun, bubun, key):
        vl, bc = _f(it, "vlRat"), _f(it, "bcRat")
        if vl > 0:
            vlrat = round(vl, 1)
        if bc > 0:
            bcrat = round(bc, 1)
        recap_hhld = max(recap_hhld, int(_f(it, "hhldCnt")))

    세대수 = sum(hhlds) if hhlds else (recap_hhld or None)
    if not (useaps or 세대수 or vlrat):
        return None
    return {
        "용적률": vlrat,                              # % (구축은 미기재→None)
        "건폐율": bcrat,                              # %
        "사용승인일": min(useaps) if useaps else None,  # YYYYMMDD
        "세대수": 세대수,
        "최고층": max(flrs) if flrs else None,
    }
