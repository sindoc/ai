"""
md2edn — Logseq Markdown → intermediate Page/Block representation.

Handles:
  - Page-level properties (key:: value lines before the first bullet)
  - Outliner blocks (- bullet indented with spaces, 2 spaces per level)
  - Block-level properties (key:: value lines as block children)
  - Block IDs (id:: <uuid>)
  - Collapsed/background-color/other Logseq block properties
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from schema import Block, Page

# Matches a property line: "key:: value" or "key::" (empty value)
_PROP_RE = re.compile(r"^([a-zA-Z_-][a-zA-Z0-9_-]*)::[ \t]*(.*?)[ \t]*$")

# Matches a Logseq bullet: optional whitespace (spaces or tabs) + "- " + content
# Logseq uses either 2 spaces or 1 tab per indent level.
_BULLET_RE = re.compile(r"^([ \t]*)- (.*)")


def _indent_level(ws: str) -> int:
    """
    Normalise mixed tab/space indentation to a single integer level.
    Logseq uses either 2-space or 1-tab per level — we normalise both to
    a count of 'indent units' (each unit = 2 spaces or 1 tab).
    We convert the raw whitespace string by expanding tabs to 2 spaces.
    """
    expanded = ws.replace("\t", "  ")
    return len(expanded)


def _parse_prop_value(raw: str) -> object:
    """Convert a raw property value string to a Python object."""
    v = raw.strip()
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    # Comma-separated multi-value (e.g. alias:: foo, bar)
    if "," in v:
        parts = [p.strip() for p in v.split(",")]
        if all(p for p in parts):
            return parts
    return v or None


def _collect_page_props(lines: list[str]) -> tuple[dict, int]:
    """
    Collect page-level properties from the top of the file.
    Returns (properties dict, index of first non-property line).
    """
    props: dict = {}
    i = 0
    for i, line in enumerate(lines):
        line = line.rstrip("\n")
        # Skip blank separator lines that appear after the property block
        if not line.strip():
            continue
        m = _PROP_RE.match(line)
        if m:
            key, val = m.group(1), m.group(2)
            props[key] = _parse_prop_value(val)
        elif line.startswith("- ") or line.startswith("  "):
            break
        else:
            # A "---" YAML-style fence — skip
            if line.strip() == "---":
                continue
    else:
        i += 1  # all lines were properties
    return props, i


def _extract_block_props(lines_of_block: list[str]) -> tuple[dict, list[str]]:
    """
    Given the child lines of a block, separate block-level property lines
    from actual content child lines.
    Returns (props dict, remaining content lines).
    """
    props: dict = {}
    remaining: list[str] = []
    for line in lines_of_block:
        m = _PROP_RE.match(line.strip())
        if m and not (line.strip().startswith("- ") or line.strip().startswith("  -")):
            key, val = m.group(1), m.group(2)
            if key == "id":
                props["__id__"] = val
            else:
                props[key] = _parse_prop_value(val)
        else:
            remaining.append(line)
    return props, remaining


def _parse_blocks(lines: list[str], base_indent: int = 0) -> list[Block]:
    """
    Recursively parse a list of lines into a tree of Blocks.
    base_indent: the expected indent level for top-level bullets in this call.
    """
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        m = _BULLET_RE.match(line)
        if not m:
            i += 1
            continue

        indent = _indent_level(m.group(1))
        if indent < base_indent:
            break  # belongs to a parent caller
        if indent > base_indent:
            i += 1
            continue  # orphaned deeper line — skip

        content_raw = m.group(2)
        # Collect all following lines that are more indented (children)
        child_lines: list[str] = []
        j = i + 1
        while j < len(lines):
            next_line = lines[j].rstrip("\n")
            if not next_line.strip():
                child_lines.append(next_line)
                j += 1
                continue
            next_m = _BULLET_RE.match(next_line)
            if next_m:
                next_indent = _indent_level(next_m.group(1))
                if next_indent <= indent:
                    break
            # deeper content (block prop or nested bullet)
            child_lines.append(next_line)
            j += 1

        # Separate block-level properties from child bullets
        def _is_prop_only(l: str) -> bool:
            s = l.strip()
            return bool(s and not _BULLET_RE.match(l) and _PROP_RE.match(s))

        prop_lines = [l for l in child_lines if _is_prop_only(l)]
        bullet_child_lines = [l for l in child_lines if not _is_prop_only(l)]

        block_props: dict = {}
        block_id: str | None = None
        for pl in prop_lines:
            pm = _PROP_RE.match(pl.strip())
            if pm:
                k, v = pm.group(1), pm.group(2)
                if k == "id":
                    block_id = v
                else:
                    block_props[k] = _parse_prop_value(v)

        children = _parse_blocks(bullet_child_lines, base_indent=indent + 2)
        blocks.append(Block(
            content=content_raw,
            properties=block_props,
            children=children,
            block_id=block_id,
        ))
        i = j

    return blocks


def parse_file(path: str | Path) -> Page:
    """Parse a Logseq Markdown file into a Page."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return parse_string(text, filename=path.stem)


def parse_string(text: str, filename: str | None = None) -> Page:
    """Parse Logseq Markdown text into a Page."""
    lines = text.splitlines(keepends=False)
    # Strip any leading blank lines
    while lines and not lines[0].strip():
        lines.pop(0)

    props, content_start = _collect_page_props(lines)

    # Derive title: prefer explicit title:: property, then filename
    title: str = str(props.pop("title", filename or "Untitled"))
    # Normalise alias to a list
    if "alias" in props and isinstance(props["alias"], str):
        props["alias"] = [a.strip() for a in props["alias"].split(",")]

    blocks = _parse_blocks(lines[content_start:], base_indent=0)

    return Page(title=title, properties=props, blocks=blocks, filename=filename)


def page_to_edn_string(page: Page) -> str:
    """Serialise a Page to EDN (Clojure/Datomic-style string)."""
    return _dict_to_edn(page.to_dict())


def _dict_to_edn(obj, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(obj, dict):
        pairs = []
        for k, v in obj.items():
            key_str = f":{k}"
            pairs.append(f"{pad}  {key_str} {_dict_to_edn(v, indent + 1)}")
        return "{\n" + "\n".join(pairs) + f"\n{pad}}}"
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = [_dict_to_edn(i, indent) for i in obj]
        return "[" + " ".join(items) + "]"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if obj is None:
        return "nil"
    if isinstance(obj, (int, float)):
        return str(obj)
    # String: EDN uses double-quoted strings
    escaped = str(obj).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: md2edn.py <file.md> [--json | --edn]")
        sys.exit(1)
    mode = "--edn" if "--edn" not in sys.argv else "--edn"
    mode = "--json" if "--json" in sys.argv else mode
    page = parse_file(sys.argv[1])
    if mode == "--json":
        print(json.dumps(page.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(page_to_edn_string(page))
