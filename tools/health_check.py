#!/usr/bin/env python3
"""
health_check.py — Logseq graph health checker for ~/ws/ai/pages/

Checks:
  1. No [[triple___lowbar]] references inside page content —
     page links must use [[Slash/Namespaces]].
  2. Every file whose name contains ___ has an explicit title:: property
     whose value uses / (so Logseq shows the right name in the UI).
  3. Every [[Page Reference]] resolves to a known page (by title or alias).
  4. No duplicate title:: values across the graph.

Exit code: 0 if all checks pass, 1 otherwise.

Usage:
  python3 tools/health_check.py [pages-dir]
  python3 tools/health_check.py            # defaults to pages/ relative to script
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field

_PROP_RE   = re.compile(r"^([a-zA-Z_-][a-zA-Z0-9_-]*)::[ \t]*(.*?)[ \t]*$")
_PAGEREF_RE = re.compile(r"\[\[(.+?)\]\]")
_TITLE_RE  = re.compile(r"^title::[ \t]+(.*?)[ \t]*$", re.MULTILINE)
_ALIAS_RE  = re.compile(r"^alias::[ \t]+(.*?)[ \t]*$", re.MULTILINE)


@dataclass
class Issue:
    level: str        # "ERROR" | "WARN"
    file:  str
    line:  int | None
    msg:   str

    def __str__(self) -> str:
        loc = f":{self.line}" if self.line else ""
        return f"  [{self.level}] {self.file}{loc}: {self.msg}"


@dataclass
class PageInfo:
    filename: str          # stem (no .md)
    title:    str          # explicit title:: or derived from filename
    aliases:  list[str] = field(default_factory=list)
    has_explicit_title: bool = False


def _filename_to_title(stem: str) -> str:
    """Derive Logseq page title from filename stem (triple-lowbar → slash)."""
    return stem.replace("___", "/")


def _collect_pages(pages_dir: Path) -> dict[str, PageInfo]:
    """Build a map of all known page titles → PageInfo."""
    pages: dict[str, PageInfo] = {}
    for md in sorted(pages_dir.glob("*.md")):
        text  = md.read_text(encoding="utf-8")
        stem  = md.stem

        title_m = _TITLE_RE.search(text)
        if title_m:
            title = title_m.group(1).strip()
            has_explicit = True
        else:
            title = _filename_to_title(stem)
            has_explicit = False

        alias_m = _ALIAS_RE.search(text)
        aliases: list[str] = []
        if alias_m:
            aliases = [a.strip() for a in alias_m.group(1).split(",") if a.strip()]

        info = PageInfo(
            filename=stem,
            title=title,
            aliases=aliases,
            has_explicit_title=has_explicit,
        )
        pages[title.lower()] = info
        for a in aliases:
            pages[a.lower()] = info

    return pages


def check(pages_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    known = _collect_pages(pages_dir)

    # ── Check 4: duplicate titles ──────────────────────────────────────────
    seen_titles: dict[str, str] = {}
    for md in sorted(pages_dir.glob("*.md")):
        text    = md.read_text(encoding="utf-8")
        title_m = _TITLE_RE.search(text)
        title   = title_m.group(1).strip() if title_m else _filename_to_title(md.stem)
        key     = title.lower()
        if key in seen_titles:
            issues.append(Issue("ERROR", md.name, None,
                f"Duplicate title '{title}' (also in {seen_titles[key]})"))
        else:
            seen_titles[key] = md.name

    # ── Per-file checks ────────────────────────────────────────────────────
    for md in sorted(pages_dir.glob("*.md")):
        text  = md.read_text(encoding="utf-8")
        lines = text.splitlines()
        stem  = md.stem
        fname = md.name

        # ── Check 2: namespaced file must have explicit title:: ────────────
        if "___" in stem:
            title_m = _TITLE_RE.search(text)
            if not title_m:
                expected = _filename_to_title(stem)
                issues.append(Issue("ERROR", fname, None,
                    f"Missing title:: — Logseq will show filename with ___. "
                    f"Add: title:: {expected}"))
            else:
                actual = title_m.group(1).strip()
                expected = _filename_to_title(stem)
                if "___" in actual:
                    issues.append(Issue("ERROR", fname, None,
                        f"title:: value contains ___ (should use /). "
                        f"Found: '{actual}'"))
                if actual.lower() != expected.lower():
                    issues.append(Issue("WARN", fname, None,
                        f"title:: '{actual}' does not match filename-derived "
                        f"title '{expected}'"))

        # ── Check 1 & 3: scan every [[reference]] ─────────────────────────
        for lineno, line in enumerate(lines, start=1):
            for m in _PAGEREF_RE.finditer(line):
                ref = m.group(1).strip()

                # Check 1: triple-lowbar inside a reference
                if "___" in ref:
                    expected_ref = ref.replace("___", "/")
                    issues.append(Issue("ERROR", fname, lineno,
                        f"[[{ref}]] uses ___ — should be [[{expected_ref}]]"))

                # Check 3: unresolved reference (after slash-normalisation)
                normalised = ref.replace("___", "/")
                if normalised.lower() not in known:
                    # Ignore self-references and template placeholders
                    if not normalised.startswith("[") and "..." not in normalised:
                        issues.append(Issue("WARN", fname, lineno,
                            f"Unresolved reference: [[{normalised}]]"))

    return issues


def main() -> None:
    if len(sys.argv) > 1:
        pages_dir = Path(sys.argv[1])
    else:
        pages_dir = Path(__file__).parent.parent / "pages"

    if not pages_dir.is_dir():
        print(f"ERROR: pages directory not found: {pages_dir}", file=sys.stderr)
        sys.exit(1)

    issues = check(pages_dir)

    errors = [i for i in issues if i.level == "ERROR"]
    warns  = [i for i in issues if i.level == "WARN"]

    if not issues:
        print(f"✓ All checks passed ({len(list(pages_dir.glob('*.md')))} pages)")
        sys.exit(0)

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for i in errors:
            print(str(i))

    if warns:
        print(f"\nWARNINGS ({len(warns)}):")
        for i in warns:
            print(str(i))

    print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
