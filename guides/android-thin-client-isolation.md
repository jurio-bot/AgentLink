# Android Thin Clients Without Weakening Identity

A small Android companion app can be useful when one narrow job deserves its own surface: approvals, notifications, capture, or a single operational control.

The tempting shortcut is to copy the existing app's credentials or signing identity. That is usually the wrong boundary.

## A different application ID is a different client

On Android, changing the application ID creates a separate installed application identity. App-private storage and Android Keystore material should be treated as separate too.

If device identity is derived partly from the package identity, the thin client will also have a distinct device identity. Do not try to make the new app impersonate the original app by copying private keys or weakening server-side checks.

## Reuse the protocol, not the secrets

The safer pattern is:

1. keep the existing server / bridge protocol unchanged
2. let the thin client generate its own app-local key
3. enroll that public identity through the existing pairing or registration contract
4. receive only the client credential the normal protocol already issues
5. use the same expiry, replay, device-binding, request-binding, and acknowledgement checks as the full client

The protocol is shared. Mutable state and secret material are not.

## Build variants can be enough

A separate Gradle module is not always necessary. When the approval or notification implementation already exists in the main codebase, an isolated build type or product flavor can sometimes provide the thinner installed surface:

- distinct application ID suffix
- dedicated app label / resources
- launcher manifest overlay
- removal of unrelated launcher activities
- feature or lane filters through build-time configuration

This keeps security-sensitive protocol code shared instead of maintaining a second copy that can drift.

## Keep the UI narrow, not the verification

A thin client should reduce interface surface, not verification depth. An approval-only app can still preserve:

- strong biometric authentication
- one-time challenge expiry
- task / request identity checks
- device binding
- duplicate-dispatch prevention
- acknowledgement identity checks
- retry versus terminal-error classification

The fact that the UI contains one button is not a reason for the backend contract to become one check.

## Instrument lifecycle stages without logging secrets

When debugging an approval flow, record sanitized milestones rather than payloads or signatures. A useful vocabulary is:

- opened
- biometric_started
- biometric_ok
- sign_ok
- send_ok
- server_ack
- binding_rejected
- expired

Tie those events to safe identifiers such as task ID, principal, timestamp, and expiry where policy permits. Never log private keys, signature bytes, authentication tokens, challenge payloads, or reusable secret material.

## Practical rule

When a second app needs the same capability, ask:

> Can this be a second properly enrolled client of the same protocol?

If the answer is yes, that is usually cleaner than cloning identity, forking the security model, or inventing another privileged route.
