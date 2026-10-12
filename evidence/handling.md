# Evidence handling

Evidence is itself sensitive. It shows how your systems work, and screenshots and exports often carry more than you meant.

## Where to keep it

- In a **controlled location**: a private repository or a restricted document store, with a named owner. Not in chat, email threads or personal drives.
- With **access restricted** to the people who need it, reviewed with the access review ([`../controls/01-access-control.md`](../controls/01-access-control.md)). Auditors and customers get a read-only, time-limited copy, not the live store.
- With **history**: version control or a store with immutable versions, so a reviewer can see when a file was produced and that it was not rewritten afterwards.

## What must not be in it

- Secret values, tokens, keys or passwords. Record the name, owner and last four characters at most.
- Personal data beyond what the evidence needs. Use roles, ticket numbers or pseudonyms; crop or redact screenshots.
- Internal addresses, account identifiers and bucket names when the copy is going outside the company, unless the recipient needs them. Redact and note that you did.

Run the sanitise scan ([`../scripts/sanitise_check.py`](../scripts/sanitise_check.py)) over a folder before you share it.

## Do not keep production data or raw logs in a repository

A repository is copied to every clone, cached by every tool, and its history cannot be fully recalled. Treat it as a place for **summaries and references**, not raw material.

- **Do not commit** production logs, database exports, customer files, screenshots showing customer data, access tokens, or session cookies. Production data never leaves production ([`../controls/04-environment-separation.md`](../controls/04-environment-separation.md)).
- **Store the original** (a raw export, a full log) in the controlled evidence store with access limits, and commit only the **summary**, the hash of the original, and where it lives.
- If something sensitive is committed, treat it as exposed: rotate secrets, remove it from history, and record the incident ([`../runbooks/incident-response.md`](../runbooks/incident-response.md)). Deleting it in a later commit is not removal.
- **Retention:** set how long evidence is kept, who may read it, and how it is deleted, in the same way as any other data ([`../privacy/retention-and-deletion.md`](../privacy/retention-and-deletion.md)).
- Keep compiled files, editor files, key files and environment files out of the repository: the scan in [`../scripts/sanitise_check.py`](../scripts/sanitise_check.py) blocks them.

## Making it trustworthy

- **Date it** with the day it was produced, not the day it was filed.
- **Say how it was produced** so someone else could repeat it: the command, the query, the screen.
- **Hash the pack** you give to an outsider (`sha256sum`) and give them the hashes separately, so they can tell it was not altered.
- **Keep the originals** (exports, logs) next to any summary of them.
- **Retention:** keep evidence for the period your customers, auditors or contracts expect, then delete it by the same rules as any other data.

## Redaction check before sharing

- [ ] No secret values. - [ ] No personal data beyond need. - [ ] No identifiers I would not tell this person. - [ ] Dates and tool versions visible. - [ ] Hashes recorded.
