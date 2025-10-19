# RUNBOOK — JIT Privileged Access

> Operational procedures for granting, verifying, and revoking time‑bound access.

## Request → Approve → Grant

1. **Submit request** (ChatOps form / ticket / API) including:
   - `principal` (user or group display name)
   - `permissionSetName` (e.g., `PowerUserScoped`)
   - `accountName` (human‑friendly; mapping resolved at runtime)
   - `durationMinutes` (e.g., 60, 120; capped by policy)
   - `changeRef` (ticket/incident number)

2. **Approval**:
   - Approver receives notification via SNS integration (email/Slack/Teams).
   - Approver selects **Approve** or **Deny**. Approval timeout results in auto‑deny.

3. **Grant**:
   - `assignment_manager` Lambda calls **sso-admin** to **create account assignment**.
   - On success, an **EventBridge Scheduler** job is created to revoke at expiry.

## Verification

- Requester should see the role in **AWS Access Portal** within ~1–2 minutes.
- `aws sso login` then `aws sts get-caller-identity` confirms access.
- CloudTrail shows `CreateAccountAssignment` from the Lambda role.

## Expiry & Revocation

- At `expiry`, Scheduler invokes Lambda to call `DeleteAccountAssignment`.
- If revoke fails, CloudWatch Alarm notifies on-call, and a retry policy runs.

## Break‑Glass

- Break‑glass permission set exists behind a sealed process (separate approver).
- Post‑incident, revoke immediately and trigger a full access review.

## Troubleshooting

- **Assignment not visible**: Check Identity Center provisioning status per account.
- **Access denied**: Validate permission set policy and session duration cap.
- **Revoke failed**: Manually call `DeleteAccountAssignment` via console/CLI.
- **ChatOps not delivered**: Confirm SNS/Chat integration and topic policy.

## KPIs

- MTTA (approval), MTTR (revocation), auto‑revoke success rate, denied vs approved, stale assignments (should be 0).