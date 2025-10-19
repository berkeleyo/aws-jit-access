"""
Lambda: assignment_manager
- GrantAssignment: Creates an Identity Center account assignment
- RevokeAssignment: Deletes the assignment
All environment values are placeholders. No account IDs or ARNs are hard-coded.
"""
import json
import os
import boto3
from botocore.exceptions import ClientError

sso = boto3.client("sso-admin")
events = boto3.client("scheduler")

INSTANCE_ARN = os.getenv("IDENTITY_CENTER_INSTANCE_ARN", "arn:aws:sso:::instance/EXAMPLE")
SCHEDULE_ROLE_ARN = os.getenv("SCHEDULER_ROLE_ARN", "arn:aws:iam::123456789012:role/EXAMPLE")  # placeholder

def lambda_handler(event, context):
    action = event.get("action")
    if action == "GrantAssignment":
        return grant_assignment(event)
    elif action == "RevokeAssignment":
        return revoke_assignment(event)
    else:
        return {"statusCode": 400, "body": f"Unknown action {action}"}

def grant_assignment(evt):
    """
    evt keys: principalType, principalId, permissionSetArn, accountId, durationMinutes, scheduleToken
    principalId should be resolved externally (e.g., by displayName lookup in IdC/IdP).
    """
    try:
        resp = sso.create_account_assignment(
            InstanceArn=INSTANCE_ARN,
            TargetId=evt["accountId"],
            TargetType="AWS_ACCOUNT",
            PermissionSetArn=evt["permissionSetArn"],
            PrincipalType=evt["principalType"],
            PrincipalId=evt["principalId"],
        )
        # schedule revocation via EventBridge Scheduler (one-shot job)
        duration = int(evt.get("durationMinutes", 60))
        schedule_name = f"jit-revoke-{evt['principalId']}-{evt['accountId']}"
        events.create_schedule(
            Name=schedule_name,
            ScheduleExpression=f"at({{EXPIRES_AT_ISO8601}})",  # replaced by the workflow
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": os.environ.get("FUNCTION_ARN", "arn:aws:lambda:region:acct:function:assignment_manager"),
                "RoleArn": SCHEDULE_ROLE_ARN,
                "Input": json.dumps({
                    "action": "RevokeAssignment",
                    "principalType": evt["principalType"],
                    "principalId": evt["principalId"],
                    "permissionSetArn": evt["permissionSetArn"],
                    "accountId": evt["accountId"]
                })
            }
        )
        return {"statusCode": 200, "body": {"requestId": resp.get("RequestId", "n/a")}}
    except ClientError as e:
        return {"statusCode": 500, "error": str(e)}

def revoke_assignment(evt):
    try:
        resp = sso.delete_account_assignment(
            InstanceArn=INSTANCE_ARN,
            TargetId=evt["accountId"],
            TargetType="AWS_ACCOUNT",
            PermissionSetArn=evt["permissionSetArn"],
            PrincipalType=evt["principalType"],
            PrincipalId=evt["principalId"],
        )
        return {"statusCode": 200, "body": {"requestId": resp.get("RequestId", "n/a")}}
    except ClientError as e:
        return {"statusCode": 500, "error": str(e)}