# URL / repository rename migration checklist

Renaming a GitHub user, repository, domain, or public route is not finished when the source tree is clean. Public references can survive outside normal code search.

## Fast pass

1. Search repository files for the old identifier or URL.
2. Verify the new identifier appears where expected.
3. Check public GitHub surfaces: issues, pull requests, and releases.
4. Check GitHub Pages / portfolio / docs links.
5. Check queued social copy, templates, and distribution artifacts.
6. Change only the stale reference first. Do not mix copy, pricing, or scope changes into a link migration.
7. Re-run the audit after the edit.

## AgentLink helper

`tools/url_contract_check.py` is read-only and can scan local text files plus public GitHub issue/PR and release text.

```bash
python tools/url_contract_check.py . \
  --forbid 'github.com/old-owner/example' \
  --require 'github.com/new-owner/example' \
  --github-repo new-owner/example
```

Use `--json` when the result needs to feed another automation step.

## What `--github-repo` covers

For each public repository it currently inspects up to:

- 100 issue / pull-request bodies returned by the GitHub issues endpoint
- 100 public release bodies

It does not claim to cover every public surface. In particular, issue comments, review comments, external social platforms, private repositories, and third-party caches need separate checks.

## Failure behavior

If a requested GitHub surface cannot be read, the report records a `remote_errors` entry and returns a failing status instead of silently treating the remote audit as clean.

That distinction matters during migrations: "not scanned" should never be translated into "no stale links found."
