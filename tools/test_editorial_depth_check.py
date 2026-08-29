import unittest

from editorial_depth_check import analyze


class EditorialDepthCheckTests(unittest.TestCase):
    def test_deep_flagship_passes(self):
        paragraph = "最近、実際に自動化を増やしていて、便利になった。"
        tension = "ただ、楽になるほど確認の仕事が濃くなる。"
        counter = "でも手作業にも確認はあったので、自動化だけのせいとは限らない。"
        wider = "生活まで測れる今、使わない場所を決めることも設計だと思う。"
        text = "\n\n".join([paragraph, tension, counter, wider] * 18)
        result = analyze(text)
        self.assertTrue(result["pass"])
        self.assertEqual(result["flags"], [])

    def test_short_flagship_is_flagged(self):
        result = analyze("最近ちょっと考えた。でもまだ分からない。")
        self.assertIn("too_short_for_flagship", result["flags"])

    def test_micro_allows_short_raw_note(self):
        result = analyze("眠いのに寝たくない夜がある。", mode="micro")
        self.assertTrue(result["pass"])

    def test_heading_heavy_listicle_is_flagged(self):
        sections = []
        for i in range(1, 6):
            sections.append(f"## {i}. 項目\n最近の話です。でも説明は短いです。")
        text = "# まとめ\n\n" + "\n\n".join(sections)
        result = analyze(text)
        self.assertIn("outline_heavier_than_thought", result["flags"])

    def test_flagship_needs_counterangle_and_trigger(self):
        text = "一般論だけを長く書く。" * 500
        result = analyze(text)
        self.assertIn("no_visible_tension_or_counterangle", result["flags"])
        self.assertIn("no_concrete_trigger_signal", result["flags"])


if __name__ == "__main__":
    unittest.main()
