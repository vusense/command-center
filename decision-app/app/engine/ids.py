"""ID generation: YYYY-MM-DD-short-slug."""

import re
from datetime import date


def slugify(text: str, max_len: int = 40) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s[:max_len] or "item"


def new_id(title: str, prefix: str = "") -> str:
    d = date.today().isoformat()
    slug = slugify(title)
    if prefix:
        return f"{prefix}-{d}-{slug}"
    return f"{d}-{slug}"
