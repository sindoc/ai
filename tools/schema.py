"""
Shared schema types for the Logseq ↔ SilkPage conversion pipeline.

Intermediate representation (IR) is plain Python dicts — JSON-serialisable
and expressible as Clojure EDN.  The two root types are Page and Block.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Block:
    """A single Logseq outline block."""
    content: str                          # raw Markdown content of this block
    properties: dict[str, Any] = field(default_factory=dict)  # block-level props
    children: list[Block] = field(default_factory=list)
    block_id: str | None = None           # id:: <uuid> if present

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"content": self.content}
        if self.block_id:
            d["id"] = self.block_id
        if self.properties:
            d["properties"] = self.properties
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Block":
        return cls(
            content=d.get("content", ""),
            properties=d.get("properties", {}),
            children=[cls.from_dict(c) for c in d.get("children", [])],
            block_id=d.get("id"),
        )


@dataclass
class Page:
    """A single Logseq page."""
    title: str
    properties: dict[str, Any] = field(default_factory=dict)  # page-level props
    blocks: list[Block] = field(default_factory=list)
    filename: str | None = None           # original .md filename (no extension)

    def to_dict(self) -> dict:
        return {
            "type": "page",
            "title": self.title,
            "filename": self.filename or self._slug(),
            "properties": self.properties,
            "blocks": [b.to_dict() for b in self.blocks],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Page":
        return cls(
            title=d.get("title", ""),
            properties=d.get("properties", {}),
            blocks=[Block.from_dict(b) for b in d.get("blocks", [])],
            filename=d.get("filename"),
        )

    def _slug(self) -> str:
        """Filesystem-safe slug from title (triple-lowbar convention)."""
        return self.title.replace("/", "___").replace(" ", "_")

    @property
    def xml_id(self) -> str:
        """XML id attribute derived from title (letters, digits, hyphens only)."""
        import re
        s = self.title.lower()
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        return s or "page"
