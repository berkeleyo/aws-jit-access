# ARCHITECTURE

## Components
- **AWS IAM Identity Center (SSO)** — Central auth; Permission Sets per role.
- **Lambda (assignment_manager)** — Creates & revokes account assignments.
- **Step Functions** — Orchestrates approval workflow with timeouts.
- **EventBridge (bus + scheduler)** — Event intake and scheduled revocation.
- **SNS / Chat** — Approval notifications to approvers.
- **CloudTrail, CloudWatch, Security Hub** — Audit & detection.

## Sequence (Mermaid)

```mermaid
sequenceDiagram
  participant U as User
  participant EV as EventBridge
  participant SF as Step Functions
  participant L as Lambda
  participant SSO as Identity Center
  participant SCH as Scheduler

  U->>EV: Submit AccessRequest
  EV->>SF: Trigger state machine
  SF->>U: Send approval prompt (via SNS/Chat)
  U-->>SF: Approve
  SF->>L: GrantAssignment(principal, permissionSet, account, duration)
  L->>SSO: CreateAccountAssignment
  SF->>SCH: Schedule Revoke at expiry
  SCH->>L: RevokeAssignment(principal, permissionSet, account)
  L->>SSO: DeleteAccountAssignment
```

## Guardrails
- **SCP** to restrict regions/services as needed.
- **Access Analyzer** for external access detection.
- **GuardDuty** for anomaly findings routed to Security Hub.