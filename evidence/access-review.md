# Access review , <YYYY-QN>

<!-- kit-evidence: control=01 date=YYYY-MM-DD result=pass type=operational -->

**Reviewer:** <role> **Date:** <YYYY-MM-DD> **Systems in scope:** <cloud, code host, database, secrets manager, domain registrar, email, ...>

## Method

Export the list of accounts and roles from each system on the date above. Compare with the current list of people and their jobs.

## Result

| System | Account | Role / permission | Still needed? | Action | Done on |
|---|---|---|---|---|---|
| <system> | <account> | <role> | Yes / No | Keep / Remove / Reduce | <YYYY-MM-DD> |

## Checks

- [ ] MFA is enforced on every account listed.
- [ ] No shared accounts.
- [ ] Everyone who left since the last review has been removed.
- [ ] Service accounts each have an owner and a purpose.
- [ ] Production roles are held only by those who need them.

## Sign-off

<Role> confirms every action above is complete as of <YYYY-MM-DD>.
