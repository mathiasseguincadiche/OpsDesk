#!/usr/bin/env python3
"""Conservative, offline checks for the public documentation and illustration assets.

This verifies files, not the rendering of GitHub or the operation of a Rocky VM.
No third-party dependencies, network requests, subprocesses or secrets are needed.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "docs/README.md",
    "docs/diagrams/README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "docs/CHARTE_GITHUB.md",
    "docs/templates/README-PROJET.md",
    "docs/templates/ARCHITECTURE-ADR.md",
    "docs/templates/RUNBOOK.md",
    "docs/templates/PREUVE.md",
    "docs/templates/RELEASE-NOTES.md",
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)")
MARKDOWN_IMAGE = re.compile(r"!\[([^\]\n]*)\]\(([^)\n]+)\)")
HTML_ASSET = re.compile(r'(?:src|srcset|href)="([^"]+)"')
REQUIRED = (
    "## Le projet en 30 secondes",
    "## Aperçu de l'application",
    "## Démarrage rapide",
    "## Architecture",
    "## Ce que montre ce projet",
    "## Mon rôle dans ce projet",
    "## Documentation",
)


def normalize_reference(raw: str) -> str | None:
    """Return an offline repository-relative target or None for a remote/fragment URL."""
    value = raw.strip().split(" ", 1)[0].strip("<>")
    if not value or value.startswith(("#", "mailto:", "data:")):
        return None
    url = urlsplit(value)
    if url.scheme or url.netloc or value.startswith("//"):
        return None
    return unquote(url.path)


def validate_document_links(page: Path) -> list[str]:
    errors: list[str] = []
    body = page.read_text(encoding="utf-8")
    references = [match.group(1) for match in MARKDOWN_LINK.finditer(body)]
    references += [match.group(2) for match in MARKDOWN_IMAGE.finditer(body)]
    references += [match.group(1) for match in HTML_ASSET.finditer(body)]
    for raw in references:
        path = normalize_reference(raw)
        if path is None:
            continue
        # GitHub Markdown absolute-root paths are not used in this project.
        if path.startswith("/"):
            errors.append(f"{page.relative_to(ROOT)}: absolute path: {raw}")
            continue
        target = (page.parent / path).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{page.relative_to(ROOT)}: path traversal: {raw}")
            continue
        if not target.exists():
            errors.append(f"{page.relative_to(ROOT)}: missing target: {raw}")
    for match in MARKDOWN_IMAGE.finditer(body):
        if not match.group(1).strip():
            errors.append(f"{page.relative_to(ROOT)}: image missing alt text")
    return errors


def check_repository() -> list[str]:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in REQUIRED:
        if heading not in readme:
            errors.append(f"README.md: required section missing: {heading}")
    for item in PAGES:
        document = ROOT / item
        if not document.is_file():
            errors.append(f"missing document: {item}")
            continue
        errors.extend(validate_document_links(document))

    for asset in ("docs/images/opsdesk-hero.svg", "docs/diagrams/architecture-globale.svg"):
        path = ROOT / asset
        if not path.is_file():
            errors.append(f"missing graphic: {asset}")
            continue
        try:
            element = ET.parse(path).getroot()
            if element.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"{asset}: invalid SVG root")
        except ET.ParseError as exc:
            errors.append(f"{asset}: invalid XML: {exc}")
    diagram_folder = ROOT / "docs/diagrams"
    for diagram in diagram_folder.glob("*.svg"):
        if not diagram.with_suffix(".drawio").is_file():
            errors.append(f"{diagram.relative_to(ROOT)}: missing draw.io source")
    return errors


def main() -> int:
    errors = check_repository()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Documentation: required headings, links, SVG and diagram sources OK.")
    print("NOTE: This is static validation only, not a visual review or InfraOps deployment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
