Param(
    [Parameter(Mandatory=$true)][string]$InstanceArn,
    [Parameter(Mandatory=$true)][string]$PermissionSetName,
    [Parameter(Mandatory=$false)][int]$SessionDurationMinutes = 60
)

# Redacted: No account IDs or ARNs stored in repo.
# Example: Create a permission set with least privilege policy.
Write-Host "[+] Creating permission set $PermissionSetName"

$duration = "PT{0}M" -f $SessionDurationMinutes

aws sso-admin create-permission-set `
  --instance-arn $InstanceArn `
  --name $PermissionSetName `
  --session-duration $duration `
  --relay-state "https://console.aws.amazon.com/" `
  --tags Key=Owner,Value=Security

# Attach a managed policy example (readonly); customize as needed.
# aws sso-admin attach-managed-policy-to-permission-set `
#   --instance-arn $InstanceArn `
#   --permission-set-arn arn:aws:sso:::permissionSet/ps-EXAMPLE `
#   --managed-policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess