# 10. Supply chain and signing

| | |
|---|---|
| **Control ID** | KIT-SCM-01 |
| **Evidence number** | 10 (the `control=` value in evidence headers) |
| **Applies to** | Everything that is built and run in production, and the tools used to build it |
| **Owner (role)** | Engineering lead |
| **Review frequency** | Every 100 days or sooner (quarterly); the audit flags evidence older than 100 days |
| **Limitations** | Verifying signatures shows what ran was built by your pipeline, not that the code in it is free of flaws |

**Objective:** You know what is in your software, who built it, and that what runs in production is exactly what your pipeline produced.

## What to do

- Build once in the pipeline. Promote the same artefact, referenced by its content digest, through environments.
- Sign every image or release with keyless signing tied to your pipeline's identity, and verify the signature on the host before running it. Refuse to run anything unsigned.
- Scan dependencies and images for known vulnerabilities on every build, and set a time limit for fixing critical findings.
- Pin versions and verify checksums for tools you install on hosts.
- Keep a software bill of materials for each release.
- Protect the pipeline itself: least-privilege tokens, protected branches, no secrets in logs.

## Why a reviewer asks

Reviewers ask how you know the code in production is the code you reviewed, and what you do about a vulnerable dependency.

## Done when

- [ ] The host verifies a signature against a pinned pipeline identity before it starts an image, and a negative test shows it refuses an unsigned one.
- [ ] Vulnerability scanning blocks the build on a critical finding or records a dated exception.
- [ ] Every deployed digest traces to a pipeline run and a pull request.
- [ ] A software bill of materials exists for the current release.

## Evidence to keep

- The verification step and a negative test result.
- Scan reports and exceptions.
- The trace from digest to pull request.
- The bill of materials.

### Kinds of evidence

- **Configuration:** Registry and signing configuration
- **Operational:** The digest-to-pull-request trace
- **Effectiveness:** An unsigned image refused by the host (the negative test)
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Deploying a mutable tag instead of a digest.
- Signing in the pipeline but never verifying on the host.
- Installing tools with `curl | sh` and no checksum.
- Ignoring scanner output until an audit.

## Indicative framework references

SOC 2 CC7.1, CC8.1 · ISO 27001:2022 A.8.8, A.8.25, A.8.28, A.5.21 · GDPR Art. 32 · DORA Art. 9, 28

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Provider-neutral commands: [`../verify/common.md`](../verify/common.md). Cloud-provider commands, where they apply: [`../verify/`](../verify/) (section 10). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../environments/pipeline.md`](../environments/pipeline.md)
