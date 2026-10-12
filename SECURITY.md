# Security policy

## Reporting a vulnerability

**Please report privately. Do not open a public issue with exploit details.**

1. Use GitHub's private vulnerability reporting: on this repository, go to **Security → Report a vulnerability**.
2. If that option is not available, open a public issue titled **"Security contact request"** with **no details**. A maintainer will arrange a private channel.

Include what you found, where, how to reproduce it, and what you think the impact is. We will acknowledge a report as soon as a maintainer can, work out the impact with you, and credit you in the changelog if you wish. This is a volunteer-style open source project with **no service level agreement**: see [`MAINTENANCE.md`](MAINTENANCE.md).

## What is in scope

- The scripts: `audit/kit-audit.py`, `scripts/sanitise_check.py`, `scripts/kit_start.py`, `scripts/controls_index.py`, and the CI workflows.
- A command in `verify/` that could change something, print a secret value, or put a user at risk.
- Guidance that would, if followed, **weaken** a user's security or lead to unlawful handling of personal data. Report these through the "Documentation correction" issue template unless they are exploitable, in which case report privately.
- Credentials, tokens, personal data or real identifiers committed by mistake.

## What is out of scope

- Findings about your own systems or a cloud provider.
- Missing coverage of a framework or provider (open a normal issue).
- Disagreements about which framework applies to you.

## Our own rules

The kit holds no credentials, and the scan in `scripts/sanitise_check.py` runs on every change to block real identifiers, keys and compiled files. If you find one it missed, tell us privately.
