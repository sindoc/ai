#!/usr/bin/env python3
"""
Wikipedia context fetcher for the ai/ knowledge graph.

Fetches article summaries from the Wikipedia REST API for a given concept
and, optionally, for its parent namespace pages and known child pages in
the graph.

Usage:
  python3 tools/wikipedia_fetch.py "AI as an Assistant"
  python3 tools/wikipedia_fetch.py "AI Governance" --with-children
  python3 tools/wikipedia_fetch.py "Intelligent agent" --raw
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
PAGES_DIR = Path(__file__).parent.parent / "pages"


def fetch_summary(query: str) -> dict | None:
    """Fetch Wikipedia summary for *query*. Returns None on 404/error."""
    encoded = urllib.parse.quote(query.replace(" ", "_"), safe="")
    url = WIKI_API.format(encoded)
    req = urllib.request.Request(url, headers={"User-Agent": "ai-knowledge-graph/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    except Exception as exc:
        print(f"[wikipedia_fetch] ERROR fetching '{query}': {exc}", file=sys.stderr)
        return None


def _known_page_titles() -> set[str]:
    """Return set of page titles from the graph (derived from filenames + title:: props)."""
    titles: set[str] = set()
    if not PAGES_DIR.exists():
        return titles
    for path in PAGES_DIR.glob("*.md"):
        # derive title from filename (triple-lowbar → /)
        stem = path.stem.replace("___", "/")
        titles.add(stem)
        # also read explicit title:: property
        try:
            first_line = path.read_text(encoding="utf-8").split("\n")[0]
            if first_line.startswith("title::"):
                titles.add(first_line[len("title::"):].strip())
        except OSError:
            pass
    return titles


def _parent_namespaces(page_title: str) -> list[str]:
    """Return all ancestor namespace segments for a page title."""
    parts = page_title.split("/")
    parents = []
    for i in range(1, len(parts)):
        parents.append("/".join(parts[:i]))
    return parents


def _child_pages(page_title: str, known: set[str]) -> list[str]:
    """Return known graph pages that are direct children of *page_title*."""
    prefix = page_title + "/"
    return [t for t in known if t.startswith(prefix) and "/" not in t[len(prefix):]]


def fetch_for_page(page_title: str, with_children: bool = False) -> dict:
    """
    Fetch Wikipedia context for *page_title* plus its namespace ancestors
    and (optionally) its direct child pages in the graph.

    Returns a dict keyed by lookup label → summary dict (or None).
    """
    known = _known_page_titles()
    results: dict[str, dict | None] = {}

    # the page itself
    results[page_title] = fetch_summary(page_title)

    # parent namespaces
    for parent in _parent_namespaces(page_title):
        if parent not in results:
            results[parent] = fetch_summary(parent)

    # child pages (optional)
    if with_children:
        for child in _child_pages(page_title, known):
            if child not in results:
                results[child] = fetch_summary(child)

    return results


def format_logseq_block(summary: dict) -> str:
    """Format a Wikipedia summary dict as a Logseq-ready block."""
    title = summary.get("title", "")
    extract = summary.get("extract", "").strip()
    url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
    lines = [f"- **{title}** (Wikipedia)"]
    if extract:
        first_sentence = extract.split(". ")[0].rstrip(".") + "."
        lines.append(f"\t- {first_sentence}")
    if url:
        lines.append(f"\t- Source: [{url}]({url})")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Wikipedia context for a graph page")
    parser.add_argument("query", help="Page title or concept to look up")
    parser.add_argument("--with-children", action="store_true",
                        help="Also fetch child namespace pages from the graph")
    parser.add_argument("--raw", action="store_true",
                        help="Output raw JSON instead of Logseq block format")
    args = parser.parse_args()

    results = fetch_for_page(args.query, with_children=args.with_children)

    for label, summary in results.items():
        if summary is None:
            print(f"# {label}\n(no Wikipedia article found)\n")
        elif args.raw:
            print(f"# {label}")
            print(json.dumps(summary, indent=2, ensure_ascii=False))
            print()
        else:
            print(f"# {label}")
            print(format_logseq_block(summary))
            print()


if __name__ == "__main__":
    main()
