from __future__ import annotations

from functools import lru_cache
from pathlib import Path

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

@lru_cache(maxsize=1)
def _find_skill_dir() -> Path | None:
    path = _repo_root() / "ipsw_service" / "ipsw-skill" / "ipsw"
    return path if (path / "SKILL.md").exists() else None

def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit].rstrip() + "\n\n[TRUNCATED]"

def get_ipsw_skill_source() -> str:
    d = _find_skill_dir()
    return str(d) if d else ""

@lru_cache(maxsize=1)
def load_ipsw_skill_context(max_chars: int = 14000) -> str:
    skill_dir = _find_skill_dir()
    if not skill_dir:
        return ""

    sections: list[str] = []

    skill_budget = min(7000, max_chars // 2)
    ref_budget_total = max(2000, max_chars - skill_budget)

    # main skill file
    try:
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        sections.append("# IPSW Skill Instructions\n" + _truncate(skill_text, skill_budget))
    except Exception:
        pass

    # reference files
    ref_dir = skill_dir / "references"
    if ref_dir.exists():
        preferred = [
            "download.md", "dyld.md", "kernel.md",
            "macho.md", "class-dump.md", "entitlements.md", "sandbox.md",
        ]

        ordered = [ref_dir / n for n in preferred if (ref_dir / n).exists()]
        ordered += sorted(
            (p for p in ref_dir.glob("*.md") if p.name not in preferred),
            key=lambda p: p.name,
        )

        per_ref = max(500, ref_budget_total // max(len(ordered), 1))

        for path in ordered:
            try:
                text = path.read_text(encoding="utf-8")
                sections.append(f"# Reference: {path.name}\n{_truncate(text, per_ref)}")
            except Exception:
                continue

    if not sections:
        return ""

    return _truncate("\n\n".join(sections), max_chars)