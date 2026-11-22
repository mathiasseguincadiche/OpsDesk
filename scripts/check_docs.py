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


def active_pages() -> list[Path]:
    """Inspect current public Markdown; keep version-1 archives out of the active contract."""
    roots = [ROOT, ROOT / "docs", ROOT / ".github", ROOT / "evidence"]
    files: set[Path] = set()
    for folder in roots:
        if folder == ROOT:
            files.update(folder.glob("*.md"))
        elif folder.exists():
            files.update(folder.rglob("*.md"))
    return sorted(files)


def heading_slug(title: str) -> str:
    """Approximate GitHub heading IDs for the subset used in this repository."""
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"`([^`]*)`", r"\1", title)
    title = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", title)
    title = re.sub(r"[^\w\- ]", "", title.lower().strip(), flags=re.UNICODE)
    return title.replace(" ", "-")


def document_anchors(path: Path) -> set[str]:
    """Collect heading slugs, duplicate suffixes and explicit HTML IDs."""
    body = path.read_text(encoding="utf-8")
    names = set(re.findall(r'<(?:a|h[1-6])\b[^>]*\bid=["\']([^"\']+)', body, re.I))
    seen: dict[str, int] = {}
    in_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            slug = heading_slug(match.group(1))
            if slug:
                count = seen.get(slug, 0)
                names.add(f"{slug}-{count}" if count else slug)
                seen[slug] = count + 1
    return names


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
            continue
        fragment = unquote(urlsplit(raw).fragment)
        if fragment and target.is_file() and target.suffix.lower() == ".md":
            if fragment not in document_anchors(target):
                errors.append(f"{page.relative_to(ROOT)}: missing anchor: {raw}")
    for match in MARKDOWN_IMAGE.finditer(body):
        if not match.group(1).strip():
            errors.append(f"{page.relative_to(ROOT)}: image missing alt text")
    return errors


def check_editorial_contract() -> list[str]:
    """Prevent known misleading claims, not certify literary quality."""
    errors: list[str] = []
    forbidden = {
        "frontend/src/components/NewTicketModal.tsx": ("L'équipe support a été notifiée.",),
        "frontend/src/pages/Users.tsx": ("Inviter un utilisateur",),
        "frontend/src/components/Layout.tsx": ("Systèmes opérationnels",),
    }
    for relative, claims in forbidden.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        for claim in claims:
            if claim in content:
                errors.append(f"{relative}: misleading or outdated claim: {claim}")
    # La documentation du dépôt ne doit pas devenir une seconde base pédagogique.
    for path in ("docs/apprentissage", "docs/templates", "docs/CHARTE_GITHUB.md",
                 "docs/parcours-apprentissage.md", "docs/laboratoire-fedora-kvm-rocky.md"):
        if (ROOT / path).exists():
            errors.append(f"{path}: personal learning content must live in Notion")
    return errors


def check_repository() -> list[str]:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in REQUIRED:
        if heading not in readme:
            errors.append(f"README.md: required section missing: {heading}")
    for document in active_pages():
        errors.extend(validate_document_links(document))
    errors.extend(check_editorial_contract())

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
        source = diagram.with_suffix(".drawio")
        if not source.is_file():
            errors.append(f"{diagram.relative_to(ROOT)}: missing draw.io source")
            continue
        try:
            exported = ET.parse(diagram).getroot()
            if exported.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"{diagram.relative_to(ROOT)}: invalid SVG root")
        except ET.ParseError as exc:
            errors.append(f"{diagram.relative_to(ROOT)}: invalid SVG XML: {exc}")
            continue
        try:
            editable = ET.parse(source).getroot()
            if editable.tag != "mxfile":
                errors.append(f"{source.relative_to(ROOT)}: invalid Draw.io root")
        except ET.ParseError as exc:
            errors.append(f"{source.relative_to(ROOT)}: invalid Draw.io XML: {exc}")
            continue
        if diagram.stem in {"architecture", "architecture-globale"}:
            svg_labels = [t.text or "" for t in exported.findall("{http://www.w3.org/2000/svg}text")]
            source_labels = [
                cell.get("value", "")
                for cell in editable.iter("mxCell")
                if cell.get("style", "").startswith("text;")
            ]
            if svg_labels != source_labels or not source_labels:
                errors.append(f"{diagram.relative_to(ROOT)}: V2 labels differ between Draw.io and SVG")
            text = " ".join(svg_labels)
            for expected in ("ARCHITECTURE V2", "NON DÉPLOYÉE", "Terraform", "HTTPS", "srv-admin", "srv-app", "srv-k3s"):
                if expected not in text:
                    errors.append(f"{diagram.relative_to(ROOT)}: missing V2 content {expected}")
    return errors


def main() -> int:
    errors = check_repository()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Documentation: active Markdown links/anchors, editorial contracts, SVG and Draw.io sources OK.")
    print("NOTE: This is static validation only, not a visual review or InfraOps deployment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
