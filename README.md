# AWS Just‑In‑Time (JIT) Privileged Access — Reference Implementation 🚀

![Redaction Status](https://img.shields.io/badge/REDACTED-no%20secrets%20or%20tenant%20data-success?label=security&logo=amazonaws)
[![IaC](https://img.shields.io/badge/IaC-CloudFormation%20%2F%20SAM-blue)]()
[![Workflow](https://img.shields.io/badge/Workflow-EventBridge%20%2B%20Step%20Functions-informational)]()
[![Auth](https://img.shields.io/badge/Auth-AWS%20IAM%20Identity%20Center%20(SSO)-blueviolet)]()

> ⚠️ **Redaction statement**: This repository contains **no secrets, credentials, IPs, account IDs, or tenant identifiers**. Values are placeholders only and must be provided via secure parameter stores (AWS SSM Parameter Store / Secrets Manager) at deploy time.

---

## 🧩 What this project is
A production‑ready reference for **time‑bound, auditable privileged access** to AWS accounts using **AWS IAM Identity Center (successor to AWS SSO)**. Requests are approved via **Step Functions** and **EventBridge**, access is granted by a **Lambda** that creates an **account assignment** to a chosen **Permission Set**, and a scheduled revocation ensures automatic expiry. All actions are logged to **CloudTrail** and surfaced in **Security Hub** for continuous assurance.

**Key goals**
- ⏱️ Least privilege with **JIT elevation** (minutes to hours, not permanent)
- 🔐 Centralized auth (**Identity Center**) and standardized **permission sets**
- 🧾 Full audit trail (CloudTrail + CloudWatch Logs + optional Detective)
- 🧯 Safe by default: automated **revocation** + cut‑off if approvals time out
- 🌍 Optional: **geo‑/region‑guardrails** via SCP & GuardDuty findings

---

## 🗺️ Architecture (Mermaid)

```mermaid
flowchart LR
    subgraph User & Approver
      RQ[Requester
(asks for elevated role)]
      AP[Approver
(Ops/Sec/On-Call)]
    end

    RQ -->|Submit access request| EVB[Amazon EventBridge
(AccessRequest Bus)]
    EVB --> SFN[Step Functions
Approval State Machine]
    SFN -->|Notify| SNS[SNS/ChatOps
(Email/Slack/Teams)]
    AP -->|Approve/Deny| SFN
    SFN -->|On Approve| L1[Lambda: GrantAssignment]
    L1 --> SSO[AWS IAM Identity Center
(sso-admin API)]
    SSO --> ACC[(Target Account)]
    SFN -->|Schedule expiry| SCH[EventBridge Scheduler]
    SCH --> L2[Lambda: RevokeAssignment]
    L2 --> SSO
    SFN --> CT[CloudTrail & CW Logs]
    CT --> HUB[Security Hub]
```

---

## 🔄 Lifecycle Stages

1. **Plan** — Define permission sets, target accounts, max durations, approver groups, and break‑glass policy.
2. **Build** — Deploy core stack (EventBridge bus, Step Functions, Lambdas, IAM roles, log groups). Register parameters (SSM/Secrets Manager).
3. **Test** — Dry‑run with non‑prod account; validate approvals, assignment, expiry, and logs.
4. **Release** — Promote to prod; enable alarms (CloudWatch, Security Hub standards).
5. **Operate** — Use `RUNBOOK.md` for day‑to‑day requests, on‑call actions, and KPIs.
6. **Monitor** — Dashboards, error alarms, SLA/SLO reporting.
7. **Secure** — Guardrails: SCPs (region allow‑list), CloudTrail org‑trail, GuardDuty, Access Analyzer.
8. **DR & Rollback** — See `docs/ROLLBACK.md` and `docs/CUTOVER_CHECKLIST.md` for safe change and recovery.

---

## 📁 Repository Structure

```
.
├── README.md
├── RUNBOOK.md
├── .gitignore
├── docs
│   ├── OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── CUTOVER_CHECKLIST.md
│   ├── ROLLBACK.md
│   └── SECURITY.md
└── scripts
    ├── deploy.sh
    ├── create-permission-set.ps1
    ├── request_access_example.json
    └── lambda
        ├── assignment_manager.py
        └── template.yaml
```

---

## 🛠️ Quick Start (local)

```bash
# 1) Create and activate a Python venv for Lambda deps (optional)
python3 -m venv .venv && source .venv/bin/activate

# 2) Validate AWS credentials (no account IDs in repo)
aws sts get-caller-identity

# 3) Package & deploy (SAM) - see scripts/deploy.sh
./scripts/deploy.sh dev
```

---

## ✅ Non‑Goals / Out‑of‑Scope
- No hard‑coded account IDs, ARNs, or emails in this repository.
- No sample noise: all examples are **minimal** and **redacted**.
- SCIM/IdP provisioning is assumed present and managed outside this stack.

---

## 🔏 Security Notes
- **Secrets**: Use AWS Secrets Manager / SSM Parameter Store; never commit secrets.
- **Policies**: Permission sets should be **least privilege**, split by duty (e.g., `ReadOnly`, `PowerUserScoped`, `BreakGlassLimited`).
- **Logging**: Lambda logs retained 90d+; CloudTrail org‑trail active; Security Hub enabled in all regions in scope.

---

## 📜 License
MIT — see `LICENSE` if you add one.