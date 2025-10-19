# ROLLBACK

> Objective: Safely revert JIT access changes without leaving residual privileges.

## Immediate
1. Disable new requests: set EventBridge rule to **Disabled**.
2. Cancel pending approvals in Step Functions.
3. Revoke all active assignments created by this workflow:
   - Query CloudWatch logs for `CreateAccountAssignment` events during change window.
   - Iterate and call `DeleteAccountAssignment`.

## Infrastructure
- Revert to previous stack version using CloudFormation change sets.
- If revert fails, delete Scheduler tasks and disable Lambdas.
- Validate org‑trail & Security Hub remain enabled; no drift.

## Data
- No persistent data except CloudWatch logs; retain per policy (e.g., 90 days).

## Validation
- Confirm no users retain temporary roles in Identity Center.
- Re‑run a smoke test on previous version if applicable.