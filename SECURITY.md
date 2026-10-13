# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | yes       |
| < 0.5   | no        |

## Reporting a vulnerability

Do not open a public issue for security problems. Email
`security@ai-code-generator-studio.dev` with:

- A description of the issue and its impact.
- A minimal reproduction (prompt, target language, config).
- The version string from `src/config/version.py`.

We aim to acknowledge within 72 hours and ship a patch within 14 days for
confirmed issues.

## Scope

In scope:

- Arbitrary file writes outside the configured `output_root`.
- Prompt-injection paths that cause the studio to execute generated code
  without an explicit `--execute` flag.
- Credential leakage through `services/provider_router.py` logs.

Out of scope:

- Generated code being buggy. The studio generates; you review.
- Local privilege escalation from a user who already controls the machine.

## Hardening defaults

The studio never executes generated code unless `--execute` is passed. The
default `output_root` is `./generated` and is sandboxed to that directory.
Provider API keys are read from environment variables only.