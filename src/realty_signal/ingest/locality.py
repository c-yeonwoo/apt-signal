"""저평가 지역 분석 — 입지(접근성·학군·주거환경) 대비 가격의 헤도닉 잔차.

데이터 소스:
  - 가격(시군구 평단가): 국토부 실거래가 API (PUBLIC_DATA_KEY)        [키]
  - 업무지구 접근성: ODsay 대중교통 소요시간 (ODSAY_KEY)              [키]
  - 학군(학원 밀도): 소상공인 상가정보 API (PUBLIC_DATA_KEY)          [키]
  - 주거환경(공원·하천·마트): OSM Overpass                            [키 불필요]

핵심 엔진 score_undervaluation 은 데이터 소스와 무관하게 순수 함수로 분리해
키 없이도 검증·동작한다. (수집기는 키 활성화 후 연결)
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

# 주요 업무지구 좌표 (lat, lng)
HUBS = {"강남": (37.4979, 127.0276), "광화문": (37.5759, 126.9769), "여의도": (37.5215, 126.9249)}

# 입지점수 가중치 (조정 가능)
WEIGHTS = {"accessibility": 0.5, "school": 0.25, "env": 0.25}

_UA = "realty-signal/1.0"


# ---------- 주거환경: OSM Overpass (키 불필요) ----------
def osm_environment(lat: float, lng: float, radius: int = 2000) -> dict:
    """반경 내 공원·물(하천/호수)·대형마트 개수."""
    q = f"""[out:json][timeout:25];
    ( way["leisure"="park"](around:{radius},{lat},{lng});
      way["natural"="water"](around:{radius},{lat},{lng});
      node["shop"="supermarket"](around:{radius},{lat},{lng});
      way["shop"="mall"](around:{radius},{lat},{lng}); );
    out tags;"""
    url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:  # noqa: S310
        els = json.load(r).get("elements", [])
    parks = sum(1 for e in els if e.get("tags", {}).get("leisure") == "park")
    water = sum(1 for e in els if e.get("tags", {}).get("natural") == "water")
    marts = sum(1 for e in els if e.get("tags", {}).get("shop") in ("supermarket", "mall"))
    return {"공원": parks, "물": water, "대형마트": marts}


# ---------- 저평가 엔진 (순수 함수, 키 불필요) ----------
def _minmax(vals: list[float]) -> list[float]:
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0 for _ in vals]
    return [(v - lo) / (hi - lo) * 100 for v in vals]


def _linfit(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """단순선형회귀 y=a+bx (최소제곱). numpy 없이."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx if sxx else 0.0
    return my - b * mx, b


def score_undervaluation(rows: list[dict]) -> list[dict]:
    """rows: [{region, price(평단가), accessibility, school, env}] (원점수, 클수록 좋음).

    입지점수 = 가중합(정규화), 적정가 = 입지점수 회귀 예측, 저평가도 = (적정가-실제가)/적정가.
    저평가도 높은 순 정렬.
    """
    rows = [r for r in rows if r.get("price")]
    if len(rows) < 3:
        return rows
    acc = _minmax([r["accessibility"] for r in rows])
    sch = _minmax([r["school"] for r in rows])
    env = _minmax([r["env"] for r in rows])
    for i, r in enumerate(rows):
        r["입지점수"] = round(
            acc[i] * WEIGHTS["accessibility"] + sch[i] * WEIGHTS["school"] + env[i] * WEIGHTS["env"], 1)

    xs = [r["입지점수"] for r in rows]
    ys = [r["price"] for r in rows]
    a, b = _linfit(xs, ys)
    for r in rows:
        fair = a + b * r["입지점수"]
        r["적정가"] = round(fair)
        r["저평가도"] = round((fair - r["price"]) / fair * 100, 1) if fair > 0 else 0.0
    rows.sort(key=lambda r: r["저평가도"], reverse=True)
    return rows
