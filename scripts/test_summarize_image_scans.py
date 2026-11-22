"""Contrôler la lecture des rapports sans lancer de scanner ou de réseau."""
import json
import tempfile
import unittest
from pathlib import Path

from summarize_image_scans import read_report, render


class TrivyReportTests(unittest.TestCase):
    def test_counts_distinct_and_fixable(self):
        with tempfile.TemporaryDirectory() as folder:
            report = Path(folder) / "api.json"
            report.write_text(json.dumps({"Results": [
                {"Vulnerabilities": [
                    {"Severity": "HIGH", "VulnerabilityID": "CVE-1", "FixedVersion": "1.2"},
                    {"Severity": "CRITICAL", "VulnerabilityID": "CVE-1"},
                    {"Severity": "MEDIUM", "VulnerabilityID": "CVE-2"},
                ]},
                {"Vulnerabilities": [
                    {"Severity": "HIGH", "VulnerabilityID": "CVE-3", "FixedVersion": "4.5"},
                ]},
            ]}), encoding="utf-8")
            counts, distinct, fixable = read_report(report)
            self.assertEqual(counts["HIGH"], 2)
            self.assertEqual(counts["CRITICAL"], 1)
            self.assertEqual(distinct, 2)
            self.assertEqual(fixable, 2)
            self.assertIn("| api | 1 | 2 | 2 | 2 |", render([report]))

    def test_invalid_scan_never_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            report = Path(folder) / "postgresql.json"
            report.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_report(report)
            with self.assertRaises(FileNotFoundError):
                read_report(Path(folder) / "absent.json")


if __name__ == "__main__":
    unittest.main()
