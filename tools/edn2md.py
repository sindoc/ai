"""
edn2md — Page/Block IR → Logseq Markdown.

Converts the intermediate representation back to Logseq-compatible Markdown,
preserving the outliner structure, page properties, and block properties.
"""
from __future__ import annotations
import sys
from pathlib import Path
from schema import Block, Page


def _prop_value_str(val) -> str:
    """Serialize a property value back to a Logseq property string."""
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    if isinstance(val, bool):
        return "true" if val else "false"
    if val is None:
        return ""
    return str(val)


def _block_to_md(block: Block, indent: int = 0) -> list[str]:
    """Render a Block (and its children) to Logseq Markdown lines."""
    prefix = "  " * indent + "- "
    lines: list[str] = []

    content = block.content or ""
    lines.append(prefix + content)

    # Block-level properties (id:: and others) appear as indented property lines
    if block.block_id:
        lines.append("  " * indent + "  id:: " + block.block_id)
    for key, val in (block.properties or {}).items():
        if key == "__id__":
            continue
        lines.append("  " * indent + f"  {key}:: {_prop_value_str(val)}")

    # Children
    for child in block.children:
        lines.extend(_block_to_md(child, indent=indent + 1))

    return lines


def page_to_md(page: Page) -> str:
    """Convert a Page to a Logseq Markdown string."""
    lines: list[str] = []

    # Page-level properties (title is always first if set explicitly)
    title_in_props = page.properties.get("title")
    if not title_in_props or str(title_in_props) != page.title:
        lines.append(f"title:: {page.title}")

    for key, val in page.properties.items():
        if key in ("title",):
            continue
        lines.append(f"{key}:: {_prop_value_str(val)}")

    # Blank separator line between properties and content
    if lines:
        lines.append("")

    # Blocks
    for block in page.blocks:
        lines.extend(_block_to_md(block, indent=0))

    return "\n".join(lines) + "\n"


def write_file(page: Page, path: str | Path) -> None:
    """Write a Page to a Logseq Markdown file."""
    path = Path(path)
    path.write_text(page_to_md(page), encoding="utf-8")


if __name__ == "__main__":
    import json
    if len(sys.argv) < 2:
        print("Usage: edn2md.py <ir.json>   # reads JSON IR, writes Logseq Markdown")
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text())
    page = Page.from_dict(data)
    print(page_to_md(page), end="")
