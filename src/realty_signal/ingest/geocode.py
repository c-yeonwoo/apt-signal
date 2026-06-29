"""지오코딩 캐시 — 단지명/주소 → 좌표. SQLite 영속 캐시 + OSM Nominatim.

Nominatim 정책상 1req/s·식별 UA 필수. 캐시 우선, 미스만 호출(요청당 상한).
좌표가 누적되는 키-값 저장이라 JSON 대신 SQLite 사용.
"""

from __future__ import annotations

import sqlite3
import time
import urllib.parse
import urllib.request
from pathlib import Path

DB = Path("data/cache/geocode.db")
_URL = "https://nominatim.openstreetmap.org/search"
_UA = "realty-signal-map/1.0 (personal home-buying study tool)"
_last = [0.0]  # 마지막 호출 시각(1req/s 준수)


def _conn() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS geo(q TEXT PRIMARY KEY, lat REAL, lng REAL, ts INTEGER)")
    return c


def _query_osm(q: str) -> tuple[float, float] | None:
    dt = time.time() - _last[0]
    if dt < 1.1:
        time.sleep(1.1 - dt)
    _last[0] = time.time()
    url = _URL + "?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1, "countrycodes": "kr"})
    try:
        import json
        data = json.loads(urllib.request.urlopen(  # noqa: S310
            urllib.request.Request(url, headers={"User-Agent": _UA}), timeout=15).read())
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None


def lookup_cached(queries: list[str]) -> dict[str, list]:
    """캐시에 있는 좌표만 즉시 반환 {q: [lat,lng]} (호출 없음)."""
    if not queries:
        return {}
    c = _conn()
    qs = list({q for q in queries if q})
    out = {}
    for i in range(0, len(qs), 400):
        chunk = qs[i:i + 400]
        ph = ",".join("?" * len(chunk))
        for q, lat, lng in c.execute(
                f"SELECT q,lat,lng FROM geo WHERE q IN ({ph}) AND lat IS NOT NULL", chunk):
            out[q] = [lat, lng]
    c.close()
    return out


def geocode_batch(queries: list[str], max_miss: int = 20) -> dict[str, list]:
    """캐시 우선 + 미스를 최대 max_miss건 OSM 조회(1req/s)하여 캐시·반환."""
    c = _conn()
    cached, miss = {}, []
    for q in dict.fromkeys(q for q in queries if q):
        row = c.execute("SELECT lat,lng FROM geo WHERE q=?", (q,)).fetchone()
        if row is None:
            miss.append(q)
        elif row[0] is not None:
            cached[q] = [row[0], row[1]]
    for q in miss[:max_miss]:
        r = _query_osm(q)
        c.execute("INSERT OR REPLACE INTO geo(q,lat,lng,ts) VALUES(?,?,?,?)",
                  (q, r[0] if r else None, r[1] if r else None, int(time.time())))
        if r:
            cached[q] = [r[0], r[1]]
    c.commit()
    c.close()
    return {"coords": cached, "remaining": max(0, len(miss) - max_miss)}
