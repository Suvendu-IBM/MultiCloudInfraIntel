# Resource Policy

**Policy ID:** POLICY-001  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `get_resource_summary`

## Purpose

This policy defines the rules and criteria for resource discovery, filtering, and reporting across multi-cloud infrastructure (AWS, Azure, GCP).

## Scope

Applies to all cloud resources managed by the organization across all environments (production, staging, development).

## Resource Inclusion Criteria

### By Tags

**Required Tags for Inclusion:**
- `owner`: Must be present and non-empty
- `cost-center`: Must match approved cost center codes
- `environment`: Must be one of: `production`, `staging`, `development`, `test`

**Optional Tags for Enhanced Filtering:**
- `project`: Project identifier
- `application`: Application name
- `data-classification`: `public`, `internal`, `confidential`, `restricted`

### By Regions

**Included Regions:**

**AWS:**
- `us-east-1` (Primary)
- `us-west-2` (Secondary)
- `eu-west-1` (Europe)
- `ap-southeast-1` (Asia Pacific)

**Azure:**
- `eastus` (Primary)
- `westus2` (Secondary)
- `westeurope` (Europe)
- `southeastasia` (Asia Pacific)

**GCP:**
- `us-central1` (Primary)
- `us-west1` (Secondary)
- `europe-west1` (Europe)
- `asia-southeast1` (Asia Pacific)

### By Resource States

**Included States:**
- `running` / `active` / `available`
- `stopped` / `deallocated` (for cost tracking)
- `pending` (for new resource monitoring)

**Excluded States:**
- `terminated` / `deleted`
- `failed` (unless specifically requested for troubleshooting)

## Filtering Rules

### Include Patterns

Resources matching ANY of these patterns are included:
- Resources with tag `managed-by: terraform` or `managed-by: cloudformation`
- Resources in approved regions (see above)
- Resources with valid `owner` and `cost-center` tags
- Resources created within the last 90 days (for active monitoring)

### Exclude Patterns

Resources matching ANY of these patterns are excluded:
- Resources tagged with `exclude-from-inventory: true`
- Resources in `sandbox` accounts (unless explicitly requested)
- Temporary resources with tag `temporary: true` older than 7 days
- Resources with tag `decommissioned: true`
- Default VPCs and their associated resources (unless modified)
- AWS service-linked roles and managed policies

### Special Cases

**Production Resources:**
- Always included regardless of age
- Require additional validation of compliance tags
- Generate alerts if missing required tags

**Development Resources:**
- Included only if created within last 30 days
- Automatically flagged for review if older than 30 days
- Lower priority in reporting

## Ownership Requirements

### Mandatory Ownership Information

Every resource MUST have:
1. **Owner Tag:** Valid email address or team identifier
   - Format: `owner: user@company.com` or `owner: team-platform`
   - Must match organization directory

2. **Cost Center Tag:** Valid cost center code
   - Format: `cost-center: CC-XXXX`
   - Must be in approved cost center list

3. **Environment Tag:** Valid environment identifier
   - Values: `production`, `staging`, `development`, `test`

### Ownership Validation Rules

**Valid Owner Formats:**
- Individual: `firstname.lastname@company.com`
- Team: `team-[platform|data|application|security]`
- Service Account: `svc-[service-name]@company.com`

**Invalid Owners (Trigger Compliance Alert):**
- Generic emails: `admin@`, `root@`, `noreply@`
- Placeholder values: `unknown`, `tbd`, `temp`
- Empty or missing owner tag

### Ownership Transfer

When ownership changes:
1. Update `owner` tag within 24 hours
2. Update `last-owner` tag with previous owner
3. Update `ownership-changed-date` tag with ISO 8601 timestamp
4. Notify both old and new owners via email

## Resource Grouping

Resources are grouped by:
1. **Primary:** Cloud Provider (AWS, Azure, GCP)
2. **Secondary:** Environment (production, staging, development)
3. **Tertiary:** Cost Center
4. **Quaternary:** Resource Type (compute, storage, network, database)

## Reporting Requirements

### Summary Report Must Include:
- Total resource count by cloud provider
- Resource count by environment
- Resource count by cost center
- Resource count by type
- Resources missing required tags (compliance violations)
- Resources in non-standard regions
- Orphaned resources (no owner or invalid owner)

### Alert Conditions:
- Any resource missing `owner` tag → **Critical Alert**
- Any resource missing `cost-center` tag → **High Alert**
- Any resource missing `environment` tag → **Medium Alert**
- Resources in non-approved regions → **Medium Alert**
- Resources older than 90 days without activity → **Low Alert**

## Compliance

Resources not meeting these criteria will be:
1. Flagged in compliance reports
2. Owners notified within 24 hours
3. Escalated to management after 7 days
4. Subject to automatic shutdown after 14 days (non-production only)

## Exceptions

Exceptions to this policy require:
- Written approval from Infrastructure Lead
- Documentation in exception registry
- Quarterly review of all active exceptions
- Automatic expiration after 90 days unless renewed

## Review and Updates

This policy is reviewed quarterly and updated as needed to reflect:
- New cloud providers or regions
- Changes in organizational structure
- New compliance requirements
- Lessons learned from incidents

---

**Policy Owner:** Infrastructure Team  
**Approved By:** CTO  
**Next Review Date:** 2026-08-18