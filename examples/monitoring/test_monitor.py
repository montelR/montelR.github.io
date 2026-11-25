import unittest
from monitor import Reading, classify, summarize, verify
import json


class MonitoringTests(unittest.TestCase):
    def test_fresh_healthy(self):
        self.assertEqual(classify(Reading(100, True), 110), "HEALTHY")

    def test_fresh_unhealthy(self):
        self.assertEqual(classify(Reading(100, False), 110), "UNHEALTHY")

    def test_stale_unknown(self):
        self.assertEqual(classify(Reading(100, True), 161), "UNKNOWN")

    def test_missing_unknown(self):
        self.assertEqual(classify(None, 110), "UNKNOWN")

    def test_future_unknown(self):
        self.assertEqual(classify(Reading(100, True), 99), "UNKNOWN")

    def test_age_boundary(self):
        self.assertEqual(classify(Reading(100, True), 160), "HEALTHY")

    def test_raw_preservation_and_counts(self):
        raw = b"INFO a\r\nERROR b\nINFO c"
        saved, summary = summarize(raw)
        self.assertEqual(saved, raw)
        self.assertEqual(json.loads(summary)["errors"], 1)
        self.assertTrue(verify(saved, summary))

    def test_changed_evidence_rejected(self):
        raw, summary = summarize(b"INFO original")
        self.assertFalse(verify(raw + b"x", summary))

    def test_negative_age_rejected(self):
        with self.assertRaises(ValueError):
            classify(Reading(1, True), 2, -1)
