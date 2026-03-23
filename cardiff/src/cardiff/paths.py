"""Shared filesystem path helpers for Cardiff."""

from __future__ import annotations

from pathlib import Path


def normalize_approved_asset_roots(
    approved_asset_roots: tuple[str | Path, ...] | None,
) -> tuple[Path, ...]:
    """Resolve approved asset roots into a canonical tuple of absolute paths."""

    return tuple(Path(root).resolve() for root in (approved_asset_roots or ()))
