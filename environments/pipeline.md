# Pipeline: build once, sign, promote by digest

## Shape

```
pull request --> checks (tests, lint, vulnerability scan, secret scan)
     |
merge to the main branch --> build image --> scan --> push --> SIGN (keyless, pipeline identity)
     |
dev pulls the new digest, runs a candidate, smoke tests, migrates, switches
     |
demo: promote a digest that already ran on dev (a tag names the digest)
     |
production: promote the digest that already ran on demo, after the soak, with an explicit approval
```

## Rules

- **Build once.** Never rebuild for another environment. A rebuild is a different artefact.
- **Promote by digest, not by tag.** A tag can move. Record the digest at every step.
- **Sign and verify.** The pipeline signs. Every host verifies the signature against the pipeline's pinned identity before it runs the image, and refuses otherwise. Test the refusal with an unsigned image.
- **Required checks, by exact name.** Branch rules list every check the pipeline runs on a pull request. A check missing from the list is not enforced.
- **No bypass.** Not for administrators, not for emergencies. Emergencies use the same path, faster.
- **Hosts pull; nothing connects in.** The deploy runs on the host and reaches out to the registry. No inbound route is opened for the pipeline.
- **Migrations are part of the deploy.** Run them as a separate user, check for drift between the files and the recorded ledger, and stop on drift.
- **Candidate first.** Start the new version beside the live one on another port with its own throwaway database, run the smoke tests, and only then switch.
- **Failed digests are not retried.** An immutable artefact that failed will fail again. Pin the failed digest and wait for a new one.

## Branch rules (all long-lived branches)

- Require a pull request.
- Require every pipeline check by name.
- No bypass for anyone, no force pushes, no deletion.
- Require up-to-date branches before merge.

## What to record

For each production deploy: digest, pipeline run, pull request(s), who approved, time, and result. This is the evidence for [`../controls/03-change-management.md`](../controls/03-change-management.md).
