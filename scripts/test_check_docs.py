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

    def test_active_pages_cover_product_docs_and_exclude_legacy(self) -> None:
        files = {str(path.relative_to(ROOT)) for path in check_docs.active_pages()}
        self.assertIn("docs/architecture.md", files)
        self.assertIn("docs/exploitation-day2.md", files)
        self.assertNotIn("legacy/docs/README.md", files)

    def test_headings_and_explicit_anchors(self) -> None:
        self.assertEqual("points-daccès-pour-lexploitation", check_docs.heading_slug("Points d'accès pour l'exploitation"))
        anchors = check_docs.document_anchors(ROOT / "docs/architecture.md")
        self.assertIn("décisions-retenues", anchors)

    def test_v2_diagrams_sources_and_exports_synchronized(self) -> None:
        # La vérification par appariement est incluse dans check_repository().
        # Elle inspecte la structure XML et les textes des paires V2.
        self.assertEqual([], check_docs.check_repository())
        for name in ("architecture", "architecture-globale"):
            self.assertTrue((ROOT / "docs" / "diagrams" / f"{name}.drawio").is_file())
            self.assertTrue((ROOT / "docs" / "diagrams" / f"{name}.svg").is_file())

    def test_no_known_misleading_claims(self) -> None:
        self.assertEqual([], check_docs.check_editorial_contract())

    def test_no_personal_training_documents_in_product_tree(self) -> None:
        self.assertFalse((ROOT / "docs/apprentissage").exists())
        self.assertFalse((ROOT / "docs/templates").exists())
        self.assertFalse((ROOT / "docs/CHARTE_GITHUB.md").exists())

    def test_security_and_contribution_policies_explicit(self) -> None:
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("ne pas", security.lower())
        self.assertIn("sans", security.lower())
        self.assertIn("SECURITY.md", contributing)
        self.assertIn("check_docs.py", contributing)


if __name__ == "__main__":
    unittest.main()
