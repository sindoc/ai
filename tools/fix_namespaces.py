#!/usr/bin/env python3
"""
fix_namespaces.py — Fix ___ vs / namespace issues across all pages.

Applies two transforms to every .md file in pages/:
  1. Replace [[Foo___Bar]] with [[Foo/Bar]] in all page references.
  2. Prepend title:: <derived-from-filename> to files with ___ in their name
     that lack an explicit title:: property.

Run health_check.py afterwards to verify zero errors remain.

Usage:
  python3 tools/fix_namespaces.py [pages-dir] [--dry-run]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

_PROP_RE  = re.compile(r"^([a-zA-Z_-][a-zA-Z0-9_-]*)::[ \t]*(.*?)[ \t]*$")
_TITLE_RE = re.compile(r"^title::[ \t]+(.*?)[ \t]*$", re.MULTILINE)

# Match [[...]] references — non-greedy, no nesting
_REF_RE   = re.compile(r"\[\[(.+?)\]\]")


def _fix_refs(text: str) -> str:
    """Replace ___ with / inside every [[...]] reference."""
    def _sub(m: re.Match) -> str:
        inner = m.group(1)
        if "___" in inner:
            inner = inner.replace("___", "/")
        return f"[[{inner}]]"
    return _REF_RE.sub(_sub, text)


def _filename_to_title(stem: str) -> str:
    return stem.replace("___", "/")


def _ensure_title(text: str, stem: str) -> tuple[str, bool]:
    """
    If the file has ___ in its name and lacks title::, prepend it.
    Returns (new_text, changed).
    """
    if "___" not in stem:
        return text, False
    if _TITLE_RE.search(text):
        return text, False
    title = _filename_to_title(stem)
    return f"title:: {title}\n{text}", True


def fix_file(md: Path, dry_run: bool = False) -> tuple[int, int]:
    """
    Fix a single file. Returns (ref_fixes, title_fixes).
    """
    original = md.read_text(encoding="utf-8")

    # Fix 1: references
    after_refs = _fix_refs(original)
    ref_fixes = 0 if after_refs == original else original.count("___")

    # Fix 2: missing title::
    after_title, title_added = _ensure_title(after_refs, md.stem)
    title_fixes = 1 if title_added else 0

    if after_title != original:
        if not dry_run:
            md.write_text(after_title, encoding="utf-8")

    return ref_fixes, title_fixes


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        pages_dir = Path(args[0])
    else:
        pages_dir = Path(__file__).parent.parent / "pages"

    if not pages_dir.is_dir():
        print(f"ERROR: pages dir not found: {pages_dir}", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print("DRY RUN — no files will be modified\n")

    total_refs = total_titles = total_files = 0
    for md in sorted(pages_dir.glob("*.md")):
        ref_n, title_n = fix_file(md, dry_run=dry_run)
        if ref_n or title_n:
            total_files  += 1
            total_refs   += ref_n
            total_titles += title_n
            tag = "(dry)" if dry_run else "fixed"
            parts = []
            if ref_n:
                parts.append(f"{ref_n} ref(s)")
            if title_n:
                parts.append("added title::")
            print(f"  {tag} {md.name}: {', '.join(parts)}")

    verb = "Would fix" if dry_run else "Fixed"
    print(f"\n{verb} {total_files} file(s): "
          f"{total_refs} bad ref(s), {total_titles} missing title(s)")


if __name__ == "__main__":
    main()
