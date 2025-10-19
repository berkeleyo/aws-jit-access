# SECURITY

- **Secret management**: Use AWS Secrets Manager / SSM Parameter Store; never commit secrets.
- **Principle of least privilege**: Lambda execution role limited to specific `sso-admin` actions: `CreateAccountAssignment`, `DeleteAccountAssignment`, `ListAccountAssignments`, and read‑only `Describe*` as needed.
- **Network**: Lambdas run in private subnets (optional) with VPC endpoints for SSM and CloudWatch Logs.
- **Detection**: Enable GuardDuty; forward findings to Security Hub; create alerts for anomalous geo‑access.
- **Compliance**: Produce evidence with CloudTrail event IDs; map controls to ISO 27001 A.5/A.7, SOC2 CC6/CC7.
- **Change control**: All changes via IaC; use change sets, code reviews, and protected branches.