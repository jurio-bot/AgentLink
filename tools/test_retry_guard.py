import unittest

from retry_guard import decide


class RetryGuardTests(unittest.TestCase):
    def test_completed_receipt_skips(self):
        self.assertEqual(decide({"receipt_present": True}), "SKIP_COMPLETED")

    def test_succeeded_status_skips(self):
        self.assertEqual(decide({"status": "succeeded"}), "SKIP_COMPLETED")

    def test_unknown_side_effect_reconciles(self):
        self.assertEqual(
            decide({"status": "failed", "side_effect": "unknown"}),
            "RECONCILE",
        )

    def test_confirmed_side_effect_reconciles_without_receipt(self):
        self.assertEqual(
            decide({"status": "failed", "side_effect": "confirmed"}),
            "RECONCILE",
        )

    def test_safe_failure_retries(self):
        self.assertEqual(
            decide({"status": "failed", "side_effect": "none", "attempts": 1}),
            "RETRY",
        )

    def test_human_gate_stops(self):
        self.assertEqual(
            decide({"status": "human_gate", "side_effect": "none"}),
            "HUMAN_REVIEW",
        )

    def test_attempt_limit_stops(self):
        self.assertEqual(
            decide(
                {
                    "status": "failed",
                    "side_effect": "none",
                    "attempts": 3,
                    "max_attempts": 3,
                }
            ),
            "HUMAN_REVIEW",
        )

    def test_invalid_side_effect_fails(self):
        with self.assertRaises(ValueError):
            decide({"status": "failed", "side_effect": "maybe"})

    def test_receipt_present_must_be_boolean(self):
        with self.assertRaisesRegex(ValueError, "receipt_present must be a boolean"):
            decide({"status": "failed", "side_effect": "none", "receipt_present": "false"})
        self.assertEqual(
            decide({"status": "failed", "side_effect": "none", "receipt_present": False}),
            "RETRY",
        )


if __name__ == "__main__":
    unittest.main()
