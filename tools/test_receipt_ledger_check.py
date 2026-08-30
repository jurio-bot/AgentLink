import io
import unittest

import receipt_ledger_check as checker


class ReceiptLedgerCheckTests(unittest.TestCase):
    def test_valid_completed_receipt(self):
        src = io.StringIO('{"idempotency_key":"send-a-v1","status":"completed","provider_object_id":"msg-1"}\n')
        records, errors = checker.load_lines(src)
        self.assertEqual([], checker.validate(records, errors))

    def test_duplicate_idempotency_key(self):
        src = io.StringIO(
            '{"idempotency_key":"x","status":"pending"}\n'
            '{"idempotency_key":"x","status":"failed"}\n'
        )
        records, errors = checker.load_lines(src)
        kinds = {issue["kind"] for issue in checker.validate(records, errors)}
        self.assertIn("duplicate_idempotency_key", kinds)

    def test_completed_requires_provider_id(self):
        src = io.StringIO('{"idempotency_key":"x","status":"succeeded"}\n')
        records, errors = checker.load_lines(src)
        kinds = {issue["kind"] for issue in checker.validate(records, errors)}
        self.assertIn("completed_without_provider_id", kinds)

    def test_bad_json_is_reported(self):
        records, errors = checker.load_lines(io.StringIO('{bad}\n'))
        kinds = {issue["kind"] for issue in checker.validate(records, errors)}
        self.assertIn("invalid_json", kinds)

    def test_missing_or_blank_status_is_reported(self):
        src = io.StringIO(
            '{"idempotency_key":"missing"}\n'
            '{"idempotency_key":"blank","status":"   "}\n'
        )
        records, errors = checker.load_lines(src)
        issues = checker.validate(records, errors)
        missing = [issue for issue in issues if issue["kind"] == "missing_status"]
        self.assertEqual([1, 2], [issue["line"] for issue in missing])

    def test_blank_idempotency_key_is_missing(self):
        src = io.StringIO('{"idempotency_key":"   ","status":"pending"}\n')
        records, errors = checker.load_lines(src)
        kinds = {issue["kind"] for issue in checker.validate(records, errors)}
        self.assertIn("missing_idempotency_key", kinds)

    def test_blank_provider_id_does_not_complete_receipt(self):
        src = io.StringIO('{"idempotency_key":"x","status":"completed","provider_object_id":"   "}\n')
        records, errors = checker.load_lines(src)
        kinds = {issue["kind"] for issue in checker.validate(records, errors)}
        self.assertIn("completed_without_provider_id", kinds)

    def test_idempotency_key_comparison_trims_outer_whitespace(self):
        src = io.StringIO(
            '{"idempotency_key":"x","status":"pending"}\n'
            '{"idempotency_key":" x ","status":"failed"}\n'
        )
        records, errors = checker.load_lines(src)
        kinds = {issue["kind"] for issue in checker.validate(records, errors)}
        self.assertIn("duplicate_idempotency_key", kinds)


if __name__ == "__main__":
    unittest.main()
