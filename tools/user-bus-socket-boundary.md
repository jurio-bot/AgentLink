# User Bus Doctor socket boundary

`DBUS_SESSION_BUS_ADDRESS=unix:path=...` is only considered healthy when the referenced path both exists and is a Unix-domain socket.

A regular file at the same path is an error, not a healthy bus. This avoids a false-positive where a stale or unrelated filesystem entry made remote automation look connected to the systemd user bus.

The check remains read-only. It does not create sockets, start services, rewrite environment variables, or attempt login/session recovery.

Regression coverage includes both a real `AF_UNIX` socket and an existing regular file.
