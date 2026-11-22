"""Offline contracts for public documentation. These are NOT runtime tests on Rocky."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts import check_docs

ROOT = Path(__file__).resolve().parents[1]


class DocumentationContracts(unittest.TestCase):
    def test_all_public_entry_points_and_local_links(self) -> None:
        self.assertEqual([], check_docs.check_repository())

    def test_normalization_never_dereferences_remote_content(self) -> None:
        for url in (
            "https://github.com/example/repository",
            "mailto:security@example.invalid",
            "#architecture",
            "data:image/svg+xml;base64,AAAA",
        ):
            self.assertIsNone(check_docs.normalize_reference(url))
        self.assertEqual(
            "docs/images/opsdesk-hero.svg",
            check_docs.normalize_reference("docs/images/opsdesk-hero.svg"),
        )
        self.assertEqual(
            "docs/diagrams/architecture.svg",
            check_docs.normalize_reference(
                "docs/diagrams/architecture.svg#technical-view"
            ),
        )

    def test_active_pages_include_all_exercises_and_exclude_legacy(self) -> None:
        files = {str(path.relative_to(ROOT)) for path in check_docs.active_pages()}
        self.assertIn("docs/apprentissage/13-autonomie.md", files)
        self.assertIn("docs/exploitation-day2.md", files)
        self.assertNotIn("legacy/docs/README.md", files)

    def test_headings_and_explicit_anchors(self) -> None:
        self.assertEqual("points-daccès-pour-lexploitation", check_docs.heading_slug("Points d'accès pour l'exploitation"))
        anchors = check_docs.document_anchors(ROOT / "docs/apprentissage/README.md")
        self.assertIn("preuve-et-progression-personnelles", anchors)
        self.assertIn("les-13-exercices", anchors)

    def test_no_known_misleading_claims(self) -> None:
        self.assertEqual([], check_docs.check_editorial_contract())

    def test_templates_never_prevalidate_exercises(self) -> None:
        templates = sorted((ROOT / "docs/templates").glob("*.md"))
        self.assertEqual(5, len(templates))
        for path in templates:
            self.assertTrue(path.read_text(encoding="utf-8").strip())
        evidence = (ROOT / "docs/templates/PREUVE.md").read_text(encoding="utf-8")
        self.assertIn("Non vérifié", evidence)
        self.assertIn("Non exécuté", evidence)
        design = (ROOT / "docs/CHARTE_GITHUB.md").read_text(encoding="utf-8")
        self.assertIn("Notion", design)
        self.assertIn("d'installation", design)
        self.assertIn("l'autonomie", design)
        self.assertIn("rendu", design.lower())

    def test_security_and_contribution_policies_explicit(self) -> None:
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("ne pas", security.lower())
        self.assertIn("sans", security.lower())
        self.assertIn("SECURITY.md", contributing)
        self.assertIn("check_docs.py", contributing)


if __name__ == "__main__":
    unittest.main()
