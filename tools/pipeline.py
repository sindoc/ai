#!/usr/bin/env python3
"""
pipeline.py — Logseq ↔ SilkPage bidirectional conversion CLI

Commands:
  md2xml   <input.md>  [output.xml]   Logseq Markdown → SilkPage DocBook XML
  xml2md   <input.xml> [output.md]    SilkPage XML → Logseq Markdown
  md2json  <input.md>  [output.json]  Logseq Markdown → JSON IR (debug)
  md2edn   <input.md>                 Logseq Markdown → EDN (stdout)
  batch    <pages-dir> <out-dir> xml  Convert all .md files in pages/ to XML

Examples:
  python pipeline.py md2xml pages/AI\\ Life.md out/ai-life.xml
  python pipeline.py xml2md out/ai-life.xml pages/AI\\ Life.md
  python pipeline.py batch pages/ out/xml/ xml
"""
from __future__ import annotations
import sys
import json
import argparse
from pathlib import Path

# Allow running from any location
sys.path.insert(0, str(Path(__file__).parent))

from md2edn  import parse_file as md_parse, page_to_edn_string
from edn2xml import page_to_docbook_string
from xml2edn import parse_xml_file
from edn2md  import page_to_md
from schema  import Page


def cmd_md2xml(args: argparse.Namespace) -> None:
    page = md_parse(args.input)
    xml_str = page_to_docbook_string(page)
    if args.output:
        Path(args.output).write_text(xml_str, encoding="utf-8")
        print(f"Written: {args.output}")
    else:
        print(xml_str)


def cmd_xml2md(args: argparse.Namespace) -> None:
    page = parse_xml_file(args.input)
    md_str = page_to_md(page)
    if args.output:
        Path(args.output).write_text(md_str, encoding="utf-8")
        print(f"Written: {args.output}")
    else:
        print(md_str, end="")


def cmd_md2json(args: argparse.Namespace) -> None:
    page = md_parse(args.input)
    out = json.dumps(page.to_dict(), indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Written: {args.output}")
    else:
        print(out)


def cmd_md2edn(args: argparse.Namespace) -> None:
    page = md_parse(args.input)
    print(page_to_edn_string(page))


def cmd_batch(args: argparse.Namespace) -> None:
    src = Path(args.input)
    dst = Path(args.output)
    dst.mkdir(parents=True, exist_ok=True)
    fmt = getattr(args, "format", "xml")

    md_files = list(src.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {src}", file=sys.stderr)
        sys.exit(1)

    ok, err = 0, 0
    for md_path in sorted(md_files):
        try:
            page = md_parse(md_path)
            if fmt == "xml":
                out_path = dst / (md_path.stem + ".xml")
                out_path.write_text(page_to_docbook_string(page), encoding="utf-8")
            elif fmt == "json":
                out_path = dst / (md_path.stem + ".json")
                out_path.write_text(
                    json.dumps(page.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
            ok += 1
        except Exception as exc:
            print(f"ERROR {md_path.name}: {exc}", file=sys.stderr)
            err += 1

    print(f"Converted {ok} files to {dst}/ ({err} errors)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Logseq ↔ SilkPage conversion pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # md2xml
    p = sub.add_parser("md2xml", help="Logseq Markdown → SilkPage DocBook XML")
    p.add_argument("input",  help="Input .md file")
    p.add_argument("output", nargs="?", help="Output .xml file (stdout if omitted)")

    # xml2md
    p = sub.add_parser("xml2md", help="SilkPage XML → Logseq Markdown")
    p.add_argument("input",  help="Input .xml file")
    p.add_argument("output", nargs="?", help="Output .md file (stdout if omitted)")

    # md2json
    p = sub.add_parser("md2json", help="Logseq Markdown → JSON IR")
    p.add_argument("input",  help="Input .md file")
    p.add_argument("output", nargs="?", help="Output .json file (stdout if omitted)")

    # md2edn
    p = sub.add_parser("md2edn", help="Logseq Markdown → EDN (stdout)")
    p.add_argument("input", help="Input .md file")

    # batch
    p = sub.add_parser("batch", help="Convert all .md files in a directory")
    p.add_argument("input",  help="Source pages/ directory")
    p.add_argument("output", help="Destination directory")
    p.add_argument("format", nargs="?", choices=["xml", "json"], default="xml")

    args = parser.parse_args()
    dispatch = {
        "md2xml":  cmd_md2xml,
        "xml2md":  cmd_xml2md,
        "md2json": cmd_md2json,
        "md2edn":  cmd_md2edn,
        "batch":   cmd_batch,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
