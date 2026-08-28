import unittest

from demo import ActionReceipt, ReceiptState, RecoveryDecision, decide_recovery


class RecoveryDecisionTests(unittest.TestCase):
    def test_completed_is_not_replayed(self):
        receipt = ActionReceipt("send-summary", ReceiptState.COMPLETED)
        self.assertEqual(
            decide_recovery(receipt),
            RecoveryDecision.SKIP_ALREADY_COMPLETED,
        )

    def test_not_started_can_retry(self):
        receipt = ActionReceipt("write-report", ReceiptState.NOT_STARTED)
        self.assertEqual(decide_recovery(receipt), RecoveryDecision.RETRY)

    def test_uncertain_requires_reconciliation(self):
        receipt = ActionReceipt("external-update", ReceiptState.UNCERTAIN)
        self.assertEqual(
            decide_recovery(receipt),
            RecoveryDecision.RECONCILE_MANUALLY,
        )


if __name__ == "__main__":
    unittest.main()
