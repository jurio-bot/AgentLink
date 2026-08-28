# Debugging `systemctl --user` from Remote Shells

A user service can be healthy while a remote, automated, or non-login shell reports that the user bus is unavailable.

The common trap is treating this as a service failure before checking the shell environment.

## The symptom

A command such as:

```bash
systemctl --user is-active my-worker.service
```

may fail with an error mentioning `DBUS_SESSION_BUS_ADDRESS` or `XDG_RUNTIME_DIR`.

That result does **not** by itself prove that `my-worker.service` is stopped.

`systemctl --user` talks to the per-user systemd manager over the user D-Bus. A remote command runner can inherit a much smaller environment than an interactive desktop or login shell, so the manager can be alive while the shell has lost the coordinates needed to reach it.

## 1. Inspect before changing anything

```bash
uid="$(id -u)"
printf 'uid=%s\n' "$uid"
printf 'XDG_RUNTIME_DIR=%s\n' "${XDG_RUNTIME_DIR:-<unset>}"
printf 'DBUS_SESSION_BUS_ADDRESS=%s\n' "${DBUS_SESSION_BUS_ADDRESS:-<unset>}"
ls -ld "/run/user/$uid" 2>/dev/null || true
ls -l "/run/user/$uid/bus" 2>/dev/null || true
```

The important distinction is:

- environment variables missing, **but** `/run/user/<uid>/bus` exists: likely an environment propagation problem;
- the runtime directory or bus socket itself is absent: do not invent an address and assume the user manager exists.

## 2. Restore coordinates only when the bus exists

If the socket is present:

```bash
uid="$(id -u)"
export XDG_RUNTIME_DIR="/run/user/$uid"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"

systemctl --user is-active my-worker.service
systemctl --user status my-worker.service --no-pager
```

This does not start or restart anything. It only lets the current shell address the already-existing user bus.

## 3. Verify the process independently

When the control-plane check is uncertain, use a second read-only signal instead of immediately restarting the service:

```bash
pgrep -af 'my-worker|expected-process-name'
```

For services that expose a health endpoint, socket, PID file, or application-level status command, check that too. Two independent observations are more useful than turning every D-Bus error into a restart.

## 4. Avoid the `sudo systemctl --user` trap

Running:

```bash
sudo systemctl --user ...
```

usually changes which user manager and environment you are talking about. It is not a general fix for a missing user bus and can make diagnosis more confusing.

Use the intended service owner and verify the runtime directory for that user.

## 5. If the bus socket is absent

Treat this as a different class of problem. Check the login/user-manager lifecycle instead of forging environment variables:

```bash
loginctl user-status "$(id -un)"
loginctl show-user "$(id -un)" -p State -p Linger
```

Depending on how the machine is operated, a persistent user service may rely on an active login session or user lingering. Changing linger state is an administrative side effect, so diagnose first and change it only when that lifecycle is actually intended.

## Practical rule

**Control-plane unreachable is not the same as workload down.**

Before restarting a `systemd --user` service from automation:

1. check the remote shell environment;
2. check whether the user bus socket exists;
3. reconnect the shell to that bus only when it exists;
4. verify the workload through an independent read-only signal;
5. restart only when the evidence says the workload itself needs it.

That small distinction prevents a diagnostic shell problem from becoming an unnecessary production-side effect.