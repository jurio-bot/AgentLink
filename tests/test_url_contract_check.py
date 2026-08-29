from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "url_contract_check.py"
spec = importlib.util.spec_from_file_location("url_contract_check", MODULE_PATH)
url_contract_check = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(url_contract_check)


def test_github_public_surfaces_classifies_issue_pr_and_release(monkeypatch):
    def fake_json(path: str, timeout: float = 8.0):
        if "/issues?" in path:
            return [
                {
                    "number": 3,
                    "title": "Issue title",
                    "body": "old-owner/example",
                    "html_url": "https://github.com/new-owner/example/issues/3",
                },
                {
                    "number": 4,
                    "title": "PR title",
                    "body": "new-owner/example",
                    "html_url": "https://github.com/new-owner/example/pull/4",
                    "pull_request": {},
                },
            ]
        if "/releases?" in path:
            return [
                {
                    "tag_name": "v1.0.0",
                    "name": "Release",
                    "body": "new-owner/example",
                    "html_url": "https://github.com/new-owner/example/releases/tag/v1.0.0",
                }
            ]
        raise AssertionError(path)

    monkeypatch.setattr(url_contract_check, "_github_json", fake_json)
    surfaces = url_contract_check.github_public_surfaces("new-owner/example")

    assert [item["source"] for item in surfaces] == [
        "github:new-owner/example:issue#3",
        "github:new-owner/example:pr#4",
        "github:new-owner/example:release:v1.0.0",
    ]
    assert "old-owner/example" in surfaces[0]["text"]


def test_analyze_combines_local_and_github_surfaces(tmp_path, monkeypatch):
    (tmp_path / "README.md").write_text("new-owner/example\n", encoding="utf-8")

    monkeypatch.setattr(
        url_contract_check,
        "github_public_surfaces",
        lambda repo: [
            {
                "source": f"github:{repo}:issue#9",
                "text": "stale link: old-owner/example",
            }
        ],
    )

    report = url_contract_check.analyze(
        tmp_path,
        forbidden=["old-owner/example"],
        required=["new-owner/example"],
        github_repos=["new-owner/example"],
    )

    assert report["scanned_files"] == 1
    assert report["scanned_remote_surfaces"] == 1
    assert report["missing_required"] == []
    assert report["stale_references"][0]["path"] == "github:new-owner/example:issue#9"
    assert report["ok"] is False
