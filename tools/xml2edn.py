"""
xml2edn — SilkPage/DocBook Website XML → Page/Block IR.

Parses a <webpage> element back into the intermediate Page/Block structure
so it can be round-tripped to Logseq Markdown via edn2md.py.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from schema import Block, Page

# DocBook namespace (optional — SilkPage files are often no-namespace)
_DB_NS = "http://docbook.org/ns/docbook"
_META_NS = {"db": _DB_NS}


def _tag(el: ET.Element) -> str:
    """Return local tag name, stripping namespace if present."""
    tag = el.tag
    if tag.startswith("{"):
        tag = tag.split("}", 1)[1]
    return tag


def _text_of(el: ET.Element) -> str:
    """
    Collect all text content recursively.
    Collapse internal whitespace that minidom pretty-printing inserts around
    inline elements so the round-trip produces clean Logseq Markdown.
    """
    parts: list[str] = []
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(_inline_el_to_md(child))
        if child.tail:
            parts.append(child.tail)
    raw = "".join(parts)
    import re as _re
    # Collapse newline+indent runs (minidom pretty-print) to single space
    collapsed = _re.sub(r"[ \t]*\n[ \t]*", " ", raw)
    # Remove space before punctuation that can't be preceded by a space in Markdown
    collapsed = _re.sub(r" ([.,;:!?)\]])", r"\1", collapsed)
    collapsed = _re.sub(r"  +", " ", collapsed)
    return collapsed.strip()


def _inline_el_to_md(el: ET.Element) -> str:
    """Convert a DocBook inline element back to Logseq Markdown."""
    tag = _tag(el)
    inner = _text_of(el)

    if tag == "link":
        linkend = el.get("linkend", "")
        # Convert XML id back to page name (best-effort: replace hyphens with spaces)
        page_name = inner or linkend.replace("-", " ").title()
        return f"[[{page_name}]]"

    if tag == "ulink":
        url = el.get("url", "")
        return f"[{inner}]({url})"

    if tag == "emphasis":
        role = el.get("role", "")
        if role in ("bold", "strong"):
            return f"**{inner}**"
        return f"*{inner}*"

    if tag in ("literal", "code"):
        return f"`{inner}`"

    if tag == "phrase":
        role = el.get("role", "")
        if role == "tag":
            return f"#{inner}"
        if role == "block-ref":
            uid = el.get("data-id", "")
            return f"(({uid}))"
        return inner

    if tag == "programlisting":
        lang = el.get("language", "")
        return f"```{lang}\n{(el.text or '').rstrip()}\n```"

    return inner


def _para_to_md(el: ET.Element) -> str:
    return _text_of(el)


def _element_to_blocks(el: ET.Element) -> list[Block]:
    """
    Recursively convert DocBook XML elements to Block objects.

    Strategy:
    - <para> → a leaf Block with inline content converted to Markdown
    - <itemizedlist> → recurse into <listitem> children
    - <listitem> → one Block; its <para> is the content, nested lists become children
    - <h1>–<h6> → a Block whose content is "## Heading text"
    - <programlisting> → a Block whose content is a fenced code block
    - <blockquote> → a Block whose content starts with "> "
    - <section> → recurse (transparent wrapper)
    """
    tag = _tag(el)
    blocks: list[Block] = []

    if tag == "section":
        for child in el:
            blocks.extend(_element_to_blocks(child))
        return blocks

    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(tag[1])
        content = "#" * level + " " + _text_of(el)
        return [Block(content=content)]

    if tag == "para":
        return [Block(content=_para_to_md(el))]

    if tag == "programlisting":
        lang = el.get("language", "")
        code = (el.text or "").rstrip()
        return [Block(content=f"```{lang}\n{code}\n```")]

    if tag == "blockquote":
        inner_blocks = []
        for child in el:
            inner_blocks.extend(_element_to_blocks(child))
        combined = "\n".join(b.content for b in inner_blocks)
        return [Block(content="> " + combined)]

    if tag == "itemizedlist":
        for item in el:
            if _tag(item) == "listitem":
                blocks.extend(_listitem_to_blocks(item))
        return blocks

    if tag == "orderedlist":
        for item in el:
            if _tag(item) == "listitem":
                blocks.extend(_listitem_to_blocks(item))
        return blocks

    # Fallback: collect text
    text = _text_of(el).strip()
    if text:
        blocks.append(Block(content=text))
    return blocks


def _listitem_to_blocks(item: ET.Element) -> list[Block]:
    """Convert a <listitem> to one Block (with possible nested children)."""
    content_parts: list[str] = []
    children: list[Block] = []

    for child in item:
        tag = _tag(child)
        if tag == "para":
            content_parts.append(_para_to_md(child))
        elif tag in ("itemizedlist", "orderedlist"):
            children.extend(_element_to_blocks(child))
        elif tag == "programlisting":
            lang = child.get("language", "")
            code = (child.text or "").rstrip()
            children.append(Block(content=f"```{lang}\n{code}\n```"))
        else:
            sub = _element_to_blocks(child)
            if sub:
                # First sub-block becomes part of content
                content_parts.append(sub[0].content)
                children.extend(sub[1:])

    content = " ".join(content_parts).strip()
    return [Block(content=content, children=children)]


def parse_xml_file(path: str | Path) -> Page:
    """Parse a SilkPage XML file back into a Page."""
    path = Path(path)
    tree = ET.parse(str(path))
    root = tree.getroot()
    return parse_xml_element(root, filename=path.stem)


def parse_xml_string(text: str, filename: str | None = None) -> Page:
    """Parse SilkPage XML string into a Page."""
    root = ET.fromstring(text)
    return parse_xml_element(root, filename=filename)


def parse_xml_element(root: ET.Element, filename: str | None = None) -> Page:
    """Convert a <webpage> ET.Element into a Page."""
    tag = _tag(root)
    if tag != "webpage":
        raise ValueError(f"Expected <webpage> root element, got <{tag}>")

    # Parse <head>
    title = filename or "Untitled"
    properties: dict = {}

    head = root.find("head")
    if head is not None:
        title_el = head.find("title")
        if title_el is not None and title_el.text:
            title = title_el.text.strip()
        for meta in head.findall("meta"):
            name = meta.get("name", "")
            content = meta.get("content", "")
            if name:
                properties[name] = content

    # Parse content (everything that's not <head> and not another <webpage>)
    blocks: list[Block] = []
    for child in root:
        if _tag(child) in ("head", "webpage"):
            continue
        blocks.extend(_element_to_blocks(child))

    return Page(title=title, properties=properties, blocks=blocks, filename=filename)


if __name__ == "__main__":
    import json
    if len(sys.argv) < 2:
        print("Usage: xml2edn.py <file.xml> [--json]")
        sys.exit(1)
    page = parse_xml_file(sys.argv[1])
    print(json.dumps(page.to_dict(), indent=2, ensure_ascii=False))
