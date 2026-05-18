# New Resource Policy

**Policy ID:** POLICY-004  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `get_new_resources_since`

## Purpose

This policy defines the standards for tracking, validating, and managing newly created cloud resources to ensure compliance, cost control, and security from the moment of creation.

## Scope

Applies to all new resources created across AWS, Azure, and GCP in all environments (production, staging, development, test).

## Definition of "New Resource"

### Time-Based Definition

**Default: Within Last 7 Days**
- Resources created within the past 7 calendar days
- Calculated from current UTC time
- Includes resources in any state (running, stopped, pending)

**Alternative Timeframes:**
- **Last 24 Hours:** For daily operational monitoring
- **Last 3 Days:** For mid-week reviews
- **Last 14 Days:** For bi-weekly compliance audits
- **Last 30 Days:** For monthly comprehensive reviews
- **Custom Range:** For specific investigations or audits

### Resource Creation Timestamp

**Timestamp Sources:**
- AWS: `LaunchTime`, `CreationDate`, or `CreateTime` depending on resource type
- Azure: `createdTime` or `timeCreated` property
- GCP: `creationTimestamp` field

**Timezone Handling:**
- All timestamps normalized to UTC
- Display in user's local timezone with UTC offset
- Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

### Excluded from "New" Classification

**Pre-existing Resources:**
- Resources created before monitoring implementation
- Migrated resources (retain original creation date)
- Resources recreated with same identifier

**System-Managed Resources:**
- Auto-created VPC components (default VPCs)
- Service-linked roles (AWS)
- System-managed disks (Azure)
- Automatic backups and snapshots (if configured)

## Notification Rules

### Production Resources - Immediate Notification

**Trigger Conditions:**
- Any resource created in production environment
- Resource tagged with `environment: production`
- Resource in production account/subscription/project

**Notification Timing:**
- Within 5 minutes of resource creation
- Real-time monitoring with 1-minute polling interval

**Notification Channels:**
- **Slack:** `#production-changes` channel
  - @here mention for compute resources
  - Standard notification for other resources
- **Email:** Production team lead and on-call engineer
- **PagerDuty:** For after-hours production changes (optional)

**Notification Content:**
```
🚨 NEW PRODUCTION RESOURCE DETECTED

Resource Type: EC2 Instance
Resource ID: i-0123456789abcdef0
Region: us-east-1
Created By: john.doe@company.com
Created At: 2026-05-18T10:30:00Z
Tags: 
  - environment: production
  - owner: john.doe@company.com
  - cost-center: CC-1234
  
Action Required: Verify this resource is authorized
Review Link: [Dashboard URL]
```

**Escalation:**
- If no acknowledgment within 15 minutes → Escalate to team lead
- If no acknowledgment within 30 minutes → Escalate to management
- If unauthorized → Initiate incident response

### Development Resources - Daily Digest

**Trigger Conditions:**
- Resources created in development environment
- Resource tagged with `environment: development` or `environment: test`
- Resource in dev/test accounts

**Notification Timing:**
- Daily digest at 09:00 local time
- Consolidated report of all dev resources created in last 24 hours

**Notification Channels:**
- **Slack:** `#dev-resources` channel (no mentions)
- **Email:** Development team leads

**Notification Content:**
```
📊 DAILY NEW RESOURCES REPORT - Development

Date: 2026-05-18
Total New Resources: 15

By Type:
- EC2 Instances: 8
- S3 Buckets: 3
- RDS Databases: 2
- Lambda Functions: 2

By Owner:
- john.doe@company.com: 6 resources
- jane.smith@company.com: 5 resources
- bob.jones@company.com: 4 resources

Compliance Issues:
- 3 resources missing required tags
- 1 resource in non-standard region

Full Report: [Dashboard URL]
```

**Review Frequency:**
- Daily review by team leads
- Weekly cleanup of unused resources
- Monthly audit of all dev resources

### Staging Resources - Daily Digest

**Trigger Conditions:**
- Resources created in staging environment
- Resource tagged with `environment: staging`

**Notification Timing:**
- Daily digest at 09:00 local time
- Separate from development digest

**Notification Channels:**
- **Slack:** `#staging-resources` channel
- **Email:** Staging environment owners

**Special Considerations:**
- Staging treated as pre-production
- Higher scrutiny than development
- Require approval for long-running resources (>7 days)

## Approval Workflow for Untagged Resources

### Detection of Untagged Resources

**Required Tags:**
- `owner`: Resource owner email or team
- `cost-center`: Valid cost center code
- `environment`: production/staging/development/test
- `project`: Project identifier
- `data-classification`: public/internal/confidential/restricted (for data resources)

**Detection Timing:**
- Check tags within 5 minutes of resource creation
- Re-check after 1 hour if initially untagged
- Final check after 24 hours

### Approval Workflow Stages

#### Stage 1: Automatic Tagging Attempt (0-5 minutes)

**Auto-Tagging Rules:**
- Inherit tags from parent resource (e.g., VPC, subnet)
- Copy tags from similar resources by same creator
- Apply default tags based on account/project
- Use creator's email as default owner

**Auto-Tagging Sources:**
- CloudFormation/Terraform stack tags
- Launch template tags
- Account-level default tags
- Creator's user profile

#### Stage 2: Owner Notification (5 minutes)

**If Auto-Tagging Fails:**
- Send notification to resource creator
- Provide tagging instructions and link
- Set deadline: 1 hour for production, 24 hours for non-production

**Notification Content:**
```
⚠️ ACTION REQUIRED: Tag Your New Resource

You created a resource without required tags:

Resource: EC2 Instance (i-0123456789abcdef0)
Created: 2026-05-18T10:30:00Z
Region: us-east-1

Missing Tags:
- cost-center (REQUIRED)
- project (REQUIRED)

Please add tags within 1 hour to avoid automatic actions.

Tag Now: [Quick Tag Link]
Learn More: [Tagging Policy]
```

#### Stage 3: Team Lead Escalation (1 hour for production)

**If Not Tagged After 1 Hour:**
- Escalate to team lead
- Request approval or tagging
- Provide resource details and cost estimate

**Team Lead Actions:**
- Approve and tag resource
- Request creator to tag
- Reject and schedule for termination

#### Stage 4: Automatic Action (24 hours for production, 7 days for dev)

**Production Resources (24 hours):**
- Stop resource (if safe to stop)
- Send final warning
- Schedule termination in 48 hours if still untagged

**Development Resources (7 days):**
- Send warning at 7 days
- Stop resource at 10 days
- Terminate at 14 days

**Exceptions:**
- Critical production resources: Manual review required
- Resources with active connections: Notify before stopping
- Databases with data: Backup before any action

### Approval Tracking

**Approval Records:**
- Approver name and timestamp
- Approval reason
- Expected lifetime
- Cost estimate
- Review date

**Approval Types:**
- **Automatic:** Auto-tagged successfully
- **Self-Service:** Creator tagged within deadline
- **Team Lead:** Approved by team lead
- **Exception:** Approved with policy exception

## Resource Validation Rules

### Compliance Checks

**Immediate Checks (Within 5 Minutes):**
1. **Tagging Compliance:**
   - All required tags present
   - Tag values valid (not empty, not placeholder)
   - Owner email valid and active

2. **Region Compliance:**
   - Resource in approved region
   - Region matches environment policy
   - No resources in restricted regions

3. **Security Compliance:**
   - No public access (unless explicitly approved)
   - Encryption enabled (for data resources)
   - Security groups follow least privilege
   - IAM roles follow least privilege

4. **Cost Compliance:**
   - Resource size within approved limits
   - No expensive instance types without approval
   - Reserved capacity utilized when available

**Extended Checks (Within 24 Hours):**
1. **Configuration Compliance:**
   - Monitoring enabled
   - Logging enabled
   - Backup configured (if required)
   - Disaster recovery plan documented

2. **Network Compliance:**
   - Proper VPC/subnet placement
   - Network ACLs configured
   - Route tables correct
   - DNS configuration valid

3. **Integration Compliance:**
   - Integrated with monitoring systems
   - Integrated with logging systems
   - Integrated with backup systems
   - Integrated with security scanning

### Validation Results

**Compliant Resource:**
- Green status in dashboard
- No further action required
- Included in regular monitoring

**Non-Compliant Resource:**
- Red status in dashboard
- Notification to owner and team lead
- Remediation required within SLA
- Escalation if not remediated

**Partially Compliant Resource:**
- Yellow status in dashboard
- Notification to owner
- Remediation recommended
- Review in next audit cycle

## Resource Categorization

### By Resource Type

**Compute Resources:**
- Virtual Machines (EC2, Azure VMs, GCE)
- Containers (ECS, AKS, GKE)
- Serverless (Lambda, Functions, Cloud Functions)
- Batch (Batch, Azure Batch, Cloud Batch)

**Storage Resources:**
- Object Storage (S3, Blob, Cloud Storage)
- Block Storage (EBS, Managed Disks, Persistent Disk)
- File Storage (EFS, Files, Filestore)
- Archive (Glacier, Archive Storage, Coldline)

**Database Resources:**
- Relational (RDS, SQL Database, Cloud SQL)
- NoSQL (DynamoDB, Cosmos DB, Firestore)
- Cache (ElastiCache, Redis Cache, Memorystore)
- Data Warehouse (Redshift, Synapse, BigQuery)

**Network Resources:**
- Load Balancers
- VPCs/Virtual Networks
- Subnets
- NAT Gateways
- VPN Connections

### By Environment

**Production:**
- Highest priority monitoring
- Immediate notifications
- Strict compliance requirements
- Change control required

**Staging:**
- High priority monitoring
- Daily notifications
- Standard compliance requirements
- Change approval recommended

**Development:**
- Standard monitoring
- Daily digest notifications
- Basic compliance requirements
- Self-service allowed

**Test:**
- Basic monitoring
- Weekly digest notifications
- Minimal compliance requirements
- Automatic cleanup after 30 days

### By Creator

**Individual Users:**
- Track by user email
- Personal accountability
- Training opportunities
- Performance metrics

**Service Accounts:**
- Track by automation tool
- Review automation policies
- Validate intended behavior
- Audit trail required

**Unknown/System:**
- Investigate immediately
- Potential security concern
- Determine actual creator
- Update tracking

## Reporting and Metrics

### Daily New Resource Report

**Recipients:** Team leads, FinOps team
**Delivery:** 09:00 local time
**Content:**
- Total new resources (last 24 hours)
- Breakdown by type, environment, owner
- Compliance status summary
- Resources requiring attention
- Cost estimate for new resources

### Weekly New Resource Summary

**Recipients:** Management, finance
**Delivery:** Monday 10:00 local time
**Content:**
- Weekly resource creation trends
- Top creators and teams
- Compliance metrics
- Cost impact analysis
- Unusual patterns or concerns

### Monthly New Resource Analysis

**Recipients:** Executives, all stakeholders
**Delivery:** 1st business day of month
**Content:**
- Monthly resource creation statistics
- Growth trends by service and environment
- Compliance improvement tracking
- Cost optimization opportunities
- Policy effectiveness review

### Key Metrics

**Creation Metrics:**
- Resources created per day/week/month
- Creation rate by environment
- Creation rate by team
- Resource type distribution

**Compliance Metrics:**
- Percentage properly tagged at creation
- Time to compliance (average)
- Untagged resource rate
- Policy violation rate

**Response Metrics:**
- Time to notification
- Time to acknowledgment
- Time to remediation
- Escalation rate

## Integration with Other Policies

### Compliance Policy Integration

- New resources automatically checked against compliance policy
- Compliance violations flagged immediately
- Remediation tracked in compliance system

### Cost Policy Integration

- New resource costs estimated and tracked
- Budget impact calculated
- Expensive resources flagged for review

### Security Policy Integration

- Security posture assessed at creation
- Vulnerabilities identified early
- Security team notified of high-risk resources

## Exception Handling

### Temporary Exceptions

**Valid Reasons:**
- Emergency production fix
- Time-sensitive business requirement
- Technical limitation preventing compliance

**Exception Process:**
1. Submit exception request with justification
2. Obtain approval from team lead and security
3. Document expected duration (max 30 days)
4. Set reminder for compliance
5. Review and close exception

### Permanent Exceptions

**Valid Reasons:**
- Legacy system constraints
- Third-party integration requirements
- Regulatory or compliance requirements

**Exception Process:**
1. Submit detailed exception request
2. Obtain approval from management and security
3. Document compensating controls
4. Quarterly review required
5. Annual re-approval required

## Review and Updates

This policy is reviewed monthly and updated to reflect:
- New resource types and services
- Changes in compliance requirements
- Feedback from resource creators
- Automation improvements
- Industry best practices

---

**Policy Owner:** Infrastructure Team  
**Approved By:** CTO & CISO  
**Next Review Date:** 2026-06-18