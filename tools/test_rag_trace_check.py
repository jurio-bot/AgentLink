import unittest

from rag_trace_check import validate_trace


class RagTraceCheckTests(unittest.TestCase):
    def test_valid_trace(self):
        self.assertEqual(
            validate_trace(
                {
                    "run_id": "run-123",
                    "agent_id": "support-rag",
                    "sources": [
                        {"source_id": "doc-a", "score": 0.91},
                        {"source_id": "doc-b", "score": 0.44},
                    ],
                }
            ),
            [],
        )

    def test_missing_run_id(self):
        issues = validate_trace({"agent_id": "a", "sources": [{"source_id": "s"}]})
        self.assertIn("missing_or_empty_run_id", issues)

    def test_missing_agent_id(self):
        issues = validate_trace({"run_id": "r", "sources": [{"source_id": "s"}]})
        self.assertIn("missing_or_empty_agent_id", issues)

    def test_empty_sources(self):
        self.assertIn("sources_empty", validate_trace({"run_id": "r", "agent_id": "a", "sources": []}))

    def test_duplicate_source_ids(self):
        issues = validate_trace(
            {
                "run_id": "r",
                "agent_id": "a",
                "sources": [{"source_id": "same"}, {"source_id": "same"}],
            }
        )
        self.assertIn("duplicate_source_id:same", issues)

    def test_score_range(self):
        issues = validate_trace(
            {"run_id": "r", "agent_id": "a", "sources": [{"source_id": "s", "score": 1.2}]}
        )
        self.assertIn("source_0_score_out_of_range", issues)


if __name__ == "__main__":
    unittest.main()
