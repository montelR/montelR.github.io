"""Fixed expectations: same tests run against baseline and corrected policy."""
import os
import unittest
from dataclasses import replace

from handoff import Review, Request, baseline_allows, can_continue


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.review = Review("reviewer", "fictional-draft", 2)
        self.request = Request("reviewer", "fictional-draft", 2, True)
        variant = os.environ.get("HANDOFF_VARIANT", "corrected")
        self.policy = {"baseline": baseline_allows, "corrected": can_continue}[variant]

    def test_current_owner_and_accepted_review_allowed(self):
        self.assertTrue(self.policy(self.review, self.request))

    def test_positive_evidence_from_other_actor_denied(self):
        self.assertFalse(self.policy(self.review, replace(self.request, actor="observer")))

    def test_missing_actor_denied(self):
        self.assertFalse(self.policy(self.review, replace(self.request, actor="")))

    def test_unaccepted_review_denied(self):
        self.assertFalse(self.policy(self.review, replace(self.request, accepted=False)))

    def test_stale_revision_denied(self):
        self.assertFalse(self.policy(self.review, replace(self.request, revision=1)))

    def test_wrong_document_denied(self):
        self.assertFalse(self.policy(self.review, replace(self.request, document="other-draft")))

    def test_closed_review_denied(self):
        self.assertFalse(self.policy(replace(self.review, open=False), self.request))

    def test_newer_unreviewed_revision_denied(self):
        self.assertFalse(self.policy(self.review, replace(self.request, revision=3)))


if __name__ == "__main__":
    unittest.main()
