"""Run the software-architecture audit command."""

from __future__ import annotations

import architecture_audit as _architecture_audit
from architecture_audit import main

__all__ = _architecture_audit.__all__


def __getattr__(name: str):
    return getattr(_architecture_audit, name)


if __name__ == "__main__":
    raise SystemExit(main())
