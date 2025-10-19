# CUTOVER CHECKLIST

- [ ] Confirm non‑prod validation complete and signed off.
- [ ] Enable org CloudTrail and Security Hub standards in target regions.
- [ ] Create Permission Sets (read‑only, scoped power user, break‑glass).
- [ ] Tag target accounts and approver groups in Parameter Store.
- [ ] Deploy state machine, Lambdas, EventBridge rules.
- [ ] Configure SNS/Chat notifications (email/slack webhook connector policy).
- [ ] Run an end‑to‑end approved request in prod with limited scope.
- [ ] Verify Scheduler creates revoke task; confirm revocation executes.
- [ ] Enable dashboards and alarms; hand over RUNBOOK.