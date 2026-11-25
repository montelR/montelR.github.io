import unittest
from dataclasses import replace
from fractions import Fraction
from fixtures import HOLD_CASES, SECOND_MECHANISM
from gate import evaluate


class GateTests(unittest.TestCase):
    def test_all_correct_but_only_one_mechanism_holds(self):
        r = evaluate(HOLD_CASES)
        self.assertEqual((r.correct, r.total), (14, 14))
        self.assertEqual(r.reduction, Fraction(1))
        self.assertEqual(r.improving_mechanisms, 1)
        self.assertEqual(r.verdict, "HOLD")

    def test_second_independent_mechanism_passes_development_gate(self):
        self.assertEqual(evaluate(HOLD_CASES + (SECOND_MECHANISM,)).verdict, "PASS")

    def test_wrong_expected_classification_fails(self):
        cases = (replace(HOLD_CASES[0], observed_b="blocked"),) + HOLD_CASES[1:]
        self.assertEqual(evaluate(cases).verdict, "FAIL")

    def test_unauthorized_effect_fails(self):
        cases = (replace(HOLD_CASES[0], unauthorized_effects=1),) + HOLD_CASES[1:]
        self.assertEqual(evaluate(cases).verdict, "FAIL")

    def test_suppressing_necessary_review_fails(self):
        cases = HOLD_CASES[:5] + (replace(HOLD_CASES[5], notices_b=0),) + HOLD_CASES[6:]
        self.assertEqual(evaluate(cases).verdict, "FAIL")

    def test_below_reduction_threshold_holds_even_with_two_mechanisms(self):
        cases = tuple(replace(p, notices_a=10, notices_b=9)
                      for p in HOLD_CASES[:5] + (SECOND_MECHANISM,))
        r = evaluate(cases)
        self.assertEqual(r.reduction, Fraction(1, 10))
        self.assertEqual(r.improving_mechanisms, 2)
        self.assertEqual(r.verdict, "HOLD")

    def test_exact_threshold_passes(self):
        cases = tuple(replace(p, notices_a=4, notices_b=3)
                      for p in (HOLD_CASES[0], SECOND_MECHANISM))
        self.assertEqual(evaluate(cases).verdict, "PASS")

    def test_no_eligible_denominator_holds(self):
        r = evaluate(HOLD_CASES[5:])
        self.assertIsNone(r.reduction)
        self.assertEqual(r.verdict, "HOLD")

    def test_repeated_case_id_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(HOLD_CASES + (HOLD_CASES[0],))

    def test_negative_counts_rejected(self):
        with self.assertRaises(ValueError):
            evaluate((replace(HOLD_CASES[0], notices_b=-1),))

    def test_empty_sample_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(())


if __name__ == "__main__":
    unittest.main()
