#!/usr/bin/env python3
"""Conservative, offline checks for the public documentation and illustration assets.

This verifies files, not the rendering of GitHub or the operation of a Rocky VM.
No third-party dependencies, network requests, subprocesses or secrets are needed.
"""

from __future__ import annotations

import re
from html import unescape
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

    diagram_folder = ROOT / "docs/diagrams"
    diagrams = sorted(diagram_folder.glob("*.svg"))
    hero = ROOT / "docs/images/opsdesk-hero.svg"
    presentation = ROOT / "docs/images/opsdesk-presentation-v3.svg"
    for graphic in (hero, presentation, *diagrams):
        try:
            element = ET.parse(graphic).getroot()
            if element.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"{graphic.relative_to(ROOT)}: invalid SVG root")
        except FileNotFoundError:
            errors.append(f"{graphic.relative_to(ROOT)}: missing graphic")
        except ET.ParseError as exc:
            errors.append(f"{graphic.relative_to(ROOT)}: invalid SVG XML: {exc}")

    global_preview = diagram_folder / "architecture-globale.png"
    try:
        with global_preview.open("rb") as image:
            if image.read(8) != b"\x89PNG\r\n\x1a\n":
                errors.append(f"{global_preview.relative_to(ROOT)}: invalid PNG signature")
    except FileNotFoundError:
        errors.append(f"{global_preview.relative_to(ROOT)}: missing graphic")

    global_source = diagram_folder / "architecture-globale-v3.drawio"
    diagram_sources = {diagram.with_suffix(".drawio") for diagram in diagrams}
    diagram_sources.add(presentation.with_suffix(".drawio"))
    for source in sorted(diagram_sources | {global_source}):
        try:
            editable = ET.parse(source).getroot()
            if editable.tag != "mxfile":
                errors.append(f"{source.relative_to(ROOT)}: invalid Draw.io root")
        except FileNotFoundError:
            errors.append(f"{source.relative_to(ROOT)}: missing Draw.io source")
            continue
        except ET.ParseError as exc:
            errors.append(f"{source.relative_to(ROOT)}: invalid Draw.io XML: {exc}")
            continue
        if source == presentation.with_suffix(".drawio"):
            try:
                visible = ET.parse(presentation).getroot()
                labels = {"".join(node.itertext()).strip() for node in visible.iter("{http://www.w3.org/2000/svg}text")}
                source_values = {unescape(cell.get("value", "")).strip() for cell in editable.iter("mxCell")}
                for label in sorted(labels - source_values):
                    errors.append(f"{source.relative_to(ROOT)}: SVG label missing in editable source: {label}")
            except (FileNotFoundError, ET.ParseError) as exc:
                errors.append(f"{presentation.relative_to(ROOT)}: cannot compare labels: {exc}")
        if source == global_source:
            cells = {cell.get("id"): cell for cell in editable.iter("mxCell")}
            for cell_id in (
                "titre", "hote", "reseau", "srv-admin", "srv-app",
                "srv-k3s", "terraform", "navigateur", "compose",
                "web", "api", "postgres", "backup", "ghcr",
            ):
                cell = cells.get(cell_id)
                if cell is None or cell.find("mxGeometry") is None:
                    errors.append(
                        f"{source.relative_to(ROOT)}: missing editable node {cell_id}"
                    )
            source_labels = " ".join(
                unescape(cell.get("value", ""))
                for cell in editable.iter("mxCell")
            ).casefold()
            for expected in (
                "terraform", "ansible", "blackbox exporter", "https", "srv-admin", "srv-app",
                "srv-k3s", "postgresql", "borg", "ghcr",
            ):
                if expected not in source_labels:
                    errors.append(
                        f"{source.relative_to(ROOT)}: missing public content {expected}"
                    )
            if any(bad in source_labels for bad in ("http :8080", "qemu+ssh", "srv-ops", "srv-learning", "srv-loadtest")):
                errors.append(f"{source.relative_to(ROOT)}: obsolete public label")

    for graphic in (diagram_folder / "architecture-globale-v3.svg", presentation):
        if graphic.exists():
            content = graphic.read_text(encoding="utf-8").casefold()
            for obsolete in ("srv-ops", "srv-learning", "srv-loadtest"):
                if obsolete in content:
                    errors.append(f"{graphic.relative_to(ROOT)}: obsolete V3 label {obsolete}")
            for pattern in (r"192[.]168[.][0-9]{1,3}[.][0-9]{1,3}", r"qemu[+]ssh"):
                if re.search(pattern, content):
                    errors.append(f"{graphic.relative_to(ROOT)}: private infrastructure detail")

    for private_file in ("architecture.drawio", "architecture.svg"):
        if (diagram_folder / private_file).exists():
            errors.append(
                f"docs/diagrams/{private_file}: private detailed view must not be published"
            )

    # Guard against re-publishing archived infrastructure internals.
    for relative in (
        "legacy/diagrams/architecture-technique.drawio",
        "legacy/diagrams/architecture-technique.svg",
    ):
        if (ROOT / relative).exists():
            errors.append(f"{relative}: private technical diagram must not be public")

    protected_markdown = [ROOT / "README.md", ROOT / "ROADMAP.md", ROOT / "STATUS.md"]
    protected_markdown += list((ROOT / "docs").rglob("*.md"))
    protected_markdown += list((ROOT / "legacy" / "docs").rglob("*.md"))
    protected_markdown += list((ROOT / "legacy" / "diagrams").rglob("*.md"))
    private_patterns = (
        re.compile(r"(?:192[.]168[.][0-9]{1,3}[.][0-9]{1,3}|10[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}|172[.](?:1[6-9]|2[0-9]|3[0-1])[.][0-9]{1,3}[.][0-9]{1,3})"),
        re.compile(r"/var/backups/"),
        re.compile(r"qemu[+]ssh"),
    )
    for document in protected_markdown:
        if not document.is_file():
            continue
        body = document.read_text(encoding="utf-8")
        for pattern in private_patterns:
            if pattern.search(body):
                errors.append(
                    f"{document.relative_to(ROOT)}: private infrastructure detail in public docs"
                )

    return errors


def main() -> int:
    errors = check_repository()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Documentation: active Markdown links/anchors, editorial contracts, PNG, SVG and Draw.io sources OK.")
    print("NOTE: This is static validation only, not a visual review or InfraOps deployment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
