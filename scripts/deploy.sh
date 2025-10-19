#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-dev}"
STACK="jit-access-${ENVIRONMENT}"

echo "[+] Packaging SAM template for ${ENVIRONMENT}"
sam validate
sam build
sam package --s3-bucket "CHANGE_ME-sam-artifacts" --output-template-file scripts/lambda/template-packaged.yaml

echo "[+] Deploying CloudFormation stack ${STACK}"
sam deploy   --stack-name "${STACK}"   --template-file scripts/lambda/template-packaged.yaml   --capabilities CAPABILITY_NAMED_IAM   --parameter-overrides     Environment="${ENVIRONMENT}"     ApprovalEmail="secops@example.com"     MaxDurationMinutes="120"   --no-fail-on-empty-changeset

echo "[+] Done. Remember to configure EventBridge rules and SNS subscriptions."