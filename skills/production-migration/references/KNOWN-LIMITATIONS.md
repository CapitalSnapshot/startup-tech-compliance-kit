# Known limitations

- **Not tested end to end on every provider.** The method comes from one real migration. The provider mapping and variants are written from documentation and general knowledge; verify each row before relying on it.
- **Assumes a conventional web application:** relational database, file uploads, background jobs. Event-streaming systems, large analytics stores, mobile backends with push infrastructure, and multi-region active-active setups need extra planning.
- **Single-region, small-team scale.** It does not cover multi-region failover, sharded databases or zero-downtime blue-green on a large fleet.
- **Compliance mapping is indicative.** It supports evidence for SOC 2, ISO 27001, GDPR and DORA but does not map controls clause by clause and is not advice. Other regimes (HIPAA, PCI DSS) have requirements it does not cover.
- **Coding agents make mistakes.** The one-action-at-a-time rule exists for that reason. Read every command, especially against production.
- **The gate script checks that files exist, not that they are right.** Read the evidence.
- **Cutover timing is estimated from your own restore test.** Large databases may need logical replication or another low-downtime technique.
- **Provider features change.** Treat service names and capabilities as a starting point.
