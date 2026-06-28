"""파싱 결과 캐시 — 대용량 엑셀을 매번 파싱하지 않도록 parquet 로 보관.

build(xlsx) → data/cache/long.parquet  (tidy long)
load()      → KBWeekly  (캐시에서 즉시 로드)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from realty_signal.ingest import kb_datahub, kb_supply, kb_weekly
from realty_signal.ingest.kb_weekly import KBWeekly

CACHE_DIR = Path("data/cache")
CACHE_FILE = CACHE_DIR / "long.parquet"
SUPPLY_FILE = CACHE_DIR / "supply.parquet"


def _save(kb: KBWeekly, out: Path) -> KBWeekly:
    out.parent.mkdir(parents=True, exist_ok=True)
    kb.long.to_parquet(out, index=False)
    return kb


def build(xlsx_path: str | Path, out: Path = CACHE_FILE) -> KBWeekly:
    """엑셀을 파싱해 parquet 캐시로 저장하고 KBWeekly 반환."""
    return _save(kb_weekly.load(xlsx_path), out)


def fetch(out: Path = CACHE_FILE, with_supply: bool = True) -> KBWeekly:
    """KB 데이터허브에서 최신 지표(+입주물량)를 받아 캐시로 저장하고 반환."""
    kb = kb_datahub.fetch()
    _save(kb, out)
    if with_supply and kb.codes:
        supply = kb_supply.fetch_supply(kb.codes)
        SUPPLY_FILE.parent.mkdir(parents=True, exist_ok=True)
        supply.to_parquet(SUPPLY_FILE, index=False)
    return kb


def load(cache: Path = CACHE_FILE) -> KBWeekly:
    """캐시(parquet)에서 KBWeekly 로드. 없으면 안내."""
    if not cache.exists():
        raise FileNotFoundError(
            f"캐시 없음: {cache}. 먼저 `signal fetch` 또는 `signal build <xlsx>` 로 생성하세요."
        )
    return KBWeekly(long=pd.read_parquet(cache))


def load_supply(cache: Path = SUPPLY_FILE) -> pd.DataFrame:
    """입주물량 공급압력 캐시 로드 (없으면 빈 DataFrame)."""
    if not cache.exists():
        return pd.DataFrame(columns=["region", "future_units", "base_units", "supply_pressure"])
    return pd.read_parquet(cache)
