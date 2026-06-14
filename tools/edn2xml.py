"""
edn2xml — Page/Block IR → SilkPage/DocBook Website XML.

Produces a <webpage> element compatible with the Lutino SilkPage theme XSL.
Inline Logseq Markdown (page refs, tags, bold, italic, code) is parsed and
converted to DocBook/custom inline elements.
"""
from __future__ import annotations
import re
import sys
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom
from schema import Block, Page

# Namespace for Logseq-specific elements (page-ref, tag, block)
LS_NS = "urn:logseq:block"

# ---------------------------------------------------------------------------
# Inline content parser
# ---------------------------------------------------------------------------

def _parse_inline(text: str, parent: ET.Element) -> None:
    """
    Parse Logseq inline Markdown content and append child elements/text to parent.

    Handles: [[page ref]], #tag, **bold**, *italic*, `code`, [text](url), and
    plain text.  Order of patterns matters — longer/more specific first.
    """
    patterns = [
        # [[Page Reference]]
        ("page_ref",  re.compile(r"\[\[(.+?)\]\]")),
        # External link [text](url)
        ("ext_link",  re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")),
        # Bold **text** or __text__
        ("bold",      re.compile(r"\*\*(.+?)\*\*|__(.+?)__")),
        # Italic *text* or _text_ (after bold check)
        ("italic",    re.compile(r"\*([^*]+?)\*|_([^_]+?)_")),
        # Inline code `text`
        ("code",      re.compile(r"`([^`]+?)`")),
        # Tag #word
        ("tag",       re.compile(r"#([\w/-]+)")),
        # Block reference ((uuid))
        ("block_ref", re.compile(r"\(\(([0-9a-f-]{36})\)\)")),
    ]

    pos = 0
    while pos < len(text):
        # Find the earliest match across all patterns
        best_match = None
        best_start = len(text)
        best_kind = None
        for kind, pat in patterns:
            m = pat.search(text, pos)
            if m and m.start() < best_start:
                best_match = m
                best_start = m.start()
                best_kind = kind

        if best_match is None:
            # No more patterns — append remaining text
            _append_text(parent, text[pos:])
            break

        # Text before the match
        if best_start > pos:
            _append_text(parent, text[pos:best_start])

        m = best_match
        if best_kind == "page_ref":
            page_name = m.group(1)
            el = ET.SubElement(parent, "link")
            el.set("linkend", _id_of(page_name))
            el.text = page_name
        elif best_kind == "ext_link":
            el = ET.SubElement(parent, "ulink")
            el.set("url", m.group(2))
            el.text = m.group(1)
        elif best_kind == "bold":
            el = ET.SubElement(parent, "emphasis")
            el.set("role", "bold")
            el.text = m.group(1) or m.group(2)
        elif best_kind == "italic":
            el = ET.SubElement(parent, "emphasis")
            el.text = m.group(1) or m.group(2)
        elif best_kind == "code":
            el = ET.SubElement(parent, "literal")
            el.text = m.group(1)
        elif best_kind == "tag":
            el = ET.SubElement(parent, "phrase")
            el.set("role", "tag")
            el.text = m.group(1)
        elif best_kind == "block_ref":
            el = ET.SubElement(parent, "phrase")
            el.set("role", "block-ref")
            el.set("data-id", m.group(1))
            el.text = "((" + m.group(1)[:8] + "…))"

        pos = m.end()


def _append_text(el: ET.Element, text: str) -> None:
    """Append text to element, handling existing tail text properly."""
    if len(el) == 0:
        el.text = (el.text or "") + text
    else:
        last = el[-1]
        last.tail = (last.tail or "") + text


def _id_of(page_name: str) -> str:
    """Convert a page name to an XML id (used in linkend attributes)."""
    s = page_name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "page"


# ---------------------------------------------------------------------------
# Heading detection in block content
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")


def _is_heading(content: str) -> tuple[bool, int, str]:
    m = _HEADING_RE.match(content.strip())
    if m:
        return True, len(m.group(1)), m.group(2)
    return False, 0, content


def _is_code_fence(content: str) -> tuple[bool, str, str]:
    """Detect ```lang\\ncontent\\n``` style code blocks."""
    m = re.match(r"^```(\w*)\n(.*?)\n?```$", content, re.DOTALL)
    if m:
        return True, m.group(1), m.group(2)
    return False, "", content


# ---------------------------------------------------------------------------
# Block → XML
# ---------------------------------------------------------------------------

def _block_to_xml(block: Block, parent: ET.Element) -> None:
    """Render a Block and its children under parent."""
    content = block.content.strip()
    if not content and not block.children:
        return

    is_head, level, head_text = _is_heading(content)
    is_code, lang, code_text = _is_code_fence(content)

    if is_code:
        pre = ET.SubElement(parent, "programlisting")
        if lang:
            pre.set("language", lang)
        pre.text = code_text
        return

    if is_head:
        tag = f"h{level}"
        el = ET.SubElement(parent, tag)
        el.text = head_text
    elif content:
        para = ET.SubElement(parent, "para")
        _parse_inline(content, para)

    if block.children:
        lst = ET.SubElement(parent, "itemizedlist")
        for child in block.children:
            item = ET.SubElement(lst, "listitem")
            _block_to_xml(child, item)


# ---------------------------------------------------------------------------
# Page → XML
# ---------------------------------------------------------------------------

def page_to_xml(page: Page) -> ET.Element:
    """Convert a Page to a SilkPage <webpage> ElementTree element."""
    root = ET.Element("webpage")
    root.set("id", page.xml_id)

    # <head>
    head = ET.SubElement(root, "head")
    title_el = ET.SubElement(head, "title")
    title_el.text = page.title

    abbrev = ET.SubElement(head, "titleabbrev")
    abbrev.text = page.title

    # Page properties as <meta> elements
    for key, val in page.properties.items():
        if key in ("__id__",):
            continue
        meta = ET.SubElement(head, "meta")
        meta.set("name", key)
        if isinstance(val, list):
            meta.set("content", ", ".join(str(v) for v in val))
        elif val is None:
            meta.set("content", "")
        else:
            meta.set("content", str(val))

    # <section> wrapping all blocks
    section = ET.SubElement(root, "section")
    for block in page.blocks:
        _block_to_xml(block, section)

    return root


def page_to_xml_string(page: Page, pretty: bool = True) -> str:
    """Return the XML string for a Page."""
    el = page_to_xml(page)
    raw = ET.tostring(el, encoding="unicode", xml_declaration=False)
    if pretty:
        dom = minidom.parseString(
            '<?xml version="1.0" encoding="UTF-8"?>' + raw
        )
        return dom.toprettyxml(indent="  ", encoding=None)
    return raw


DOCTYPE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!DOCTYPE webpage PUBLIC\n'
    '  "-//Norman Walsh//DTD Website V2.6.0//EN"\n'
    '  "http://docbook.sourceforge.net/release/website/2.6.0/schema/dtd/website.dtd">\n'
)


def page_to_docbook_string(page: Page) -> str:
    """Return a full DocBook Website XML document string."""
    el = page_to_xml(page)
    raw = ET.tostring(el, encoding="unicode")
    dom = minidom.parseString("<root>" + raw + "</root>")
    inner = dom.documentElement.firstChild
    pretty = inner.toprettyxml(indent="  ")
    # Remove the <?xml?> processing instruction minidom inserts
    lines = [l for l in pretty.split("\n") if not l.startswith("<?xml")]
    return DOCTYPE + "\n".join(lines)


if __name__ == "__main__":
    import sys
    from md2edn import parse_file
    if len(sys.argv) < 2:
        print("Usage: edn2xml.py <file.md>")
        sys.exit(1)
    page = parse_file(sys.argv[1])
    print(page_to_docbook_string(page))
