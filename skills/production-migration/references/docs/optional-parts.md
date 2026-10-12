# Lean or full: what you can skip

The guide defaults to the full path because it is easier to drop steps than to add them under audit pressure. Choose deliberately.

## Lean path

Use when no customer, partner or investor is asking for audit evidence yet and the main goal is a rebuildable, safer production.

| Item | Lean | Why it is safe to defer |
| --- | --- | --- |
| Demo environment | Skip; use dev and a rehearsal clone | Only needed for external demos or a soak environment |
| Separate accounts per environment | Skip; one account with role separation and deny policies | Role separation gives most of the protection |
| Evidence pack | Keep the phase evidence files, skip the assembled pack | You can assemble it later from the files |
| Second host, read replica, cross-region copies | Skip | Availability targets are lower; record the accepted risk |
| Threat detection and security alarms | Keep alarms for root login, no-MFA login and policy changes; defer the rest | Cheap and high value; the rest is lower priority |

Never skip: the backup before touching anything, the inventory, the scratch restore and timing, the rehearsal, the rollback owner and deadline, deleting scratch copies of production data, and the 14-day soak.

## Full path

Use when you expect SOC 2, ISO 27001, GDPR or DORA scrutiny, partner security questionnaires or a bank integration. Adds a demo environment, an assembled evidence pack, and stricter separation.

## Product-specific parts

These come from the author's product and are not universal. Keep them only if they apply.

- **Verification list:** your own journeys (sign in, core transaction, partner or API integrations, an email send). The guide only requires that you list them and test them from outside.
- **Integration endpoints that must survive cutover:** list them in ENDPOINTS TO KEEP; the cutover prompt keeps them working.
- **Second hostname scheme:** moving a user-facing hostname at cutover is optional and adds redirect work.

## When not to migrate

- The live system is stable, patched and recoverable, and nobody is asking for more. Fix the backups and monitoring and stop there.
- You cannot stop shipping features for several weeks and have no second pair of hands. Do Phase 0 only: it carries the safety gains for little effort.
- The platform you are on is not actually being deprecated and its limits do not bite yet.
