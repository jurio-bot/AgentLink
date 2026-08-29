# systemd-managed Chrome session continuity

A browser automation service can look healthy while still losing the state that made it useful. A common failure pattern is:

1. Chrome exits or is restarted by systemd.
2. `Restart=always` brings the process back.
3. The new browser opens successfully, but authenticated work tabs are gone.
4. A drop-in has also replaced part of `ExecStart`, so important DevTools flags silently disappear.

The process recovered. The work context did not.

## Checks that catch this early

Inspect the effective unit, not only the base file:

```bash
systemctl --user cat my-browser.service
systemctl --user show my-browser.service \
  -p ActiveState -p NRestarts -p ActiveEnterTimestamp -p ExecStart
journalctl --user -u my-browser.service --since '-30 min'
```

`active` by itself is not enough. `NRestarts`, the journal, and the effective `ExecStart` tell you whether the browser is quietly cycling or running with different flags than expected.

## Preserve the continuity-critical flags

A persistent automation profile normally needs one stable `--user-data-dir`. If DevTools access and session recovery are part of the design, keep those switches together in every `ExecStart` override, for example:

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/google-chrome-stable \
  --user-data-dir=%h/.local/share/my-browser-profile \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --restore-last-session \
  --no-first-run \
  --no-default-browser-check
```

Use the narrowest acceptable DevTools origin policy for your environment. The wildcard above is only a compact example for a loopback-isolated setup.

## The drop-in trap

A systemd drop-in that contains a blank `ExecStart=` resets the original command completely. Every required flag must then be restated in the replacement command.

This makes the following sequence important after any browser-service patch:

```bash
systemctl --user daemon-reload
systemctl --user cat my-browser.service
systemctl --user show my-browser.service -p ExecStart
```

If the last two commands disagree with what you intended, do not assume the browser will inherit flags from the base unit.

## Recovery validation

After a controlled maintenance restart, verify both layers:

- process layer: service is active and `NRestarts` is stable
- work layer: expected authenticated tabs or recoverable session state returned
- control layer: the DevTools target list is reachable and automation can reconnect

For long-running agents, browser recovery is complete only when the work context is recoverable too.