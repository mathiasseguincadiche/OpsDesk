#!/usr/bin/env python3
"""Résumer les alertes Trivy, sans confondre scan réussi et image sans risque."""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path


def read_report(path: Path) -> tuple[Counter[str], int, int]:
    """Retourner les occurrences, les CVE distinctes et les corrections annoncées."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("Results"), list):
        raise ValueError(f"{path}: rapport Trivy JSON absent ou invalide")
    counts: Counter[str] = Counter()
    identifiers: set[str] = set()
    fixable = 0
    for target in document["Results"]:
        if not isinstance(target, dict):
            raise ValueError(f"{path}: cible mal formée")
        for item in target.get("Vulnerabilities") or []:
            if not isinstance(item, dict):
                raise ValueError(f"{path}: vulnérabilité mal formée")
            severity = item.get("Severity", "UNKNOWN")
            if severity not in ("HIGH", "CRITICAL"):
                continue
            counts[severity] += 1
            if item.get("VulnerabilityID"):
                identifiers.add(item["VulnerabilityID"])
            if item.get("FixedVersion"):
                fixable += 1
    return counts, len(identifiers), fixable


def render(paths: list[Path]) -> str:
    lines = [
        "## Scan Trivy des images OpsDesk",
        "",
        "Les chiffres comptent des **occurrences** ; plusieurs peuvent correspondre à une même CVE.",
        "Un job vert valide le déroulement du scanner, **pas** la sécurité des images.",
        "",
        "| Image | CRITICAL | HIGH | CVE distinctes | Occurrences avec correctif annoncé |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for path in paths:
        counts, distinct, fixable = read_report(path)
        lines.append(f"| {path.stem} | {counts['CRITICAL']} | {counts['HIGH']} | {distinct} | {fixable} |")
        if counts["CRITICAL"] or counts["HIGH"]:
            print(f"::warning title=Trivy {path.stem}::{counts['CRITICAL']} CRITICAL et {counts['HIGH']} HIGH")
    lines.extend([
        "",
        "Les rapports JSON et les identifiants des images se trouvent dans les artefacts du run.",
        "Traiter les risques résiduels dans l'issue #51 avant toute exposition publique.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    markdown = render(arguments.reports)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(markdown, encoding="utf-8")
    step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if step_summary:
        with Path(step_summary).open("a", encoding="utf-8") as output:
            output.write(markdown)
    print(markdown)


if __name__ == "__main__":
    main()
