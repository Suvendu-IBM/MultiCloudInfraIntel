# Prompt: Generate 8 Policy Markdown Files

## Context
This prompt was used to generate 8 detailed policy markdown files that define the business rules, compliance requirements, and operational guidelines for each MCP tool.

## Original Prompt to Bob

Bob, create 8 comprehensive policy markdown files in the `policies/` folder, one for each MCP tool. Each policy must define the rules, criteria, thresholds, and compliance requirements.

## 8 Policy Files Required

### 1. resource-policy.md
**Governs Tool:** `get_resource_summary`

**Key Requirements:**
- Required tags: owner, cost-center, environment
- Approved regions for AWS, Azure, GCP
- Resource states: running, stopped, pending (exclude: terminated, deleted)
- Filtering rules: include/exclude patterns
- Ownership validation rules
- Compliance alert conditions

### 2. cost-trends-policy.md
**Governs Tool:** `get_cost_trends`

**Key Requirements:**
- Trend periods: daily, weekly, monthly
- Increase threshold for alerts
- Cost tracking by service, region, tag
- Historical comparison periods
- Alert conditions for cost increases

### 3. anomaly-policy.md
**Governs Tool:** `get_cost_anomaly`

**Key Requirements:**
- Anomaly threshold: 20% above baseline
- Baseline period: 7-day rolling average
- Detection metrics: cost, CPU, memory, network, storage
- Alert severity levels
- Automatic anomaly detection

### 4. new-resource-policy.md
**Governs Tool:** `get_new_resources_since`

**Key Requirements:**
- Tracking period: resources created after specific date
- Auto-tagging requirements
- Approval workflows
- Notification on creation
- Compliance validation for new resources

### 5. idle-resource-policy.md
**Governs Tool:** `find_idle_resources`

**Key Requirements:**
- CPU threshold: <5% average
- Idle duration: 14 days
- Auto-shutdown options
- Notification before action
- Cost savings calculation

### 6. compliance-policy.md
**Governs Tool:** `check_compliance`

**Key Requirements:**
- Required tags: owner, cost-center, environment
- Encryption requirements
- Public access rules
- Enforcement levels: WARN, BLOCK, AUDIT
- Auto-remediation options

### 7. expensive-resource-policy.md
**Governs Tool:** `get_top_expensive_resources`

**Key Requirements:**
- Cost limit: 10 resources by default
- Limit period: daily, weekly, monthly
- Action on exceed: ALERT, THROTTLE, SHUTDOWN
- Cost ranking methodology

### 8. budget-policy.md
**Governs Tool:** `get_budget_health`

**Key Requirements:**
- Warning threshold: 80%
- Critical threshold: 100%
- Budget periods: monthly, quarterly, yearly
- Spending projections
- Alert escalation

## Policy Structure Template

Each policy file must include:
1. **Policy ID** - Unique identifier (POLICY-XXX)
2. **Version** - Version number
3. **Effective Date** - When policy takes effect
4. **Governs Tool** - Which MCP tool it governs
5. **Purpose** - Why the policy exists
6. **Scope** - What it applies to
7. **Rules** - Detailed rules and criteria
8. **Compliance** - Compliance requirements
9. **Exceptions** - Exception process
10. **Review Schedule** - When policy is reviewed

## Technical Requirements

- **Format:** Markdown
- **Location:** `policies/` folder
- **Naming:** `{policy-name}-policy.md`
- **Structure:** Consistent across all 8 files
- **Detail Level:** Production-ready, enterprise-grade
- **Compliance:** Aligned with industry standards

## Expected Output

8 comprehensive policy markdown files with:
- Clear business rules
- Specific thresholds and criteria
- Compliance requirements
- Alert conditions
- Exception processes
- Review schedules

## Result

Bob successfully generated 8 detailed policy files:
- ✅ `resource-policy.md` (185 lines) - Resource discovery and filtering
- ✅ `cost-trends-policy.md` - Cost trend monitoring
- ✅ `anomaly-policy.md` - Anomaly detection with 20% threshold
- ✅ `new-resource-policy.md` - New resource tracking
- ✅ `idle-resource-policy.md` - Idle resource detection (CPU <5%, 14 days)
- ✅ `compliance-policy.md` - Compliance enforcement (required tags)
- ✅ `expensive-resource-policy.md` - Expensive resource monitoring (limit: 10)
- ✅ `budget-policy.md` - Budget management (80% warning, 100% critical)

**Files Generated:** 8 policy markdown files in `policies/` folder

## Key Features

- **Enterprise-Grade:** Production-ready policies with detailed rules
- **Compliance-Focused:** Clear compliance requirements and alert conditions
- **Actionable:** Specific thresholds and criteria for automation
- **Consistent:** Uniform structure across all 8 policies
- **Reviewable:** Quarterly review schedules and exception processes

---

**Prompt Date:** 2026-05-18  
**Bob Version:** Advanced Mode  
**Outcome:** ✅ Success - 8 production-ready policy files