import unittest

from image_model_benchmark import summarize


def row(model, category, score):
    return {
        "model": model,
        "category": category,
        "scores": {
            "composition": score,
            "prompt_adherence": score,
            "subject_consistency": score,
            "background_logic": score,
            "artifact_control": score,
        },
    }


class ImageModelBenchmarkTests(unittest.TestCase):
    def test_complete_model_beats_high_scoring_incomplete_model(self):
        records = [row("balanced", c, 4) for c in ("photo", "illustration", "manga", "complex_composition")]
        records += [row("one-trick", "photo", 5)]
        out = summarize(records)
        self.assertEqual(out[0]["model"], "balanced")
        self.assertEqual(out[0]["coverage"], 1.0)
        self.assertEqual(out[1]["missing_required_categories"], ["illustration", "manga", "complex_composition"])

    def test_worst_case_breaks_tie_before_mean(self):
        records = [row("steady", c, 4) for c in ("photo", "illustration", "manga", "complex_composition")]
        records += [row("spiky", "photo", 5), row("spiky", "illustration", 5), row("spiky", "manga", 5), row("spiky", "complex_composition", 2)]
        out = summarize(records)
        self.assertEqual(out[0]["model"], "steady")
        self.assertGreater(out[0]["worst_case"], out[1]["worst_case"])

    def test_rejects_out_of_range_scores(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 5"):
            summarize([row("bad", "photo", 6)])

    def test_reports_dimension_means(self):
        out = summarize([row("m", c, 3.5) for c in ("photo", "illustration", "manga", "complex_composition")])
        self.assertEqual(out[0]["dimension_means"]["composition"], 3.5)
        self.assertEqual(out[0]["worst_case"], 3.5)


if __name__ == "__main__":
    unittest.main()
