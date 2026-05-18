# Idle Resource Policy

**Policy ID:** POLICY-005  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `find_idle_resources`

## Purpose

This policy establishes criteria for identifying idle or underutilized cloud resources and defines actions to optimize costs while maintaining operational requirements.

## Scope

Applies to all cloud resources across AWS, Azure, and GCP that consume costs when idle or underutilized.

## Idle Resource Definitions by Type

### Compute Resources

#### EC2 Instances / Azure VMs / GCE Instances

**Idle Definition:**
- **CPU Utilization:** Average CPU < 5% for 14 consecutive days
- **Network Activity:** < 1 MB/hour average for 14 days
- **Disk I/O:** < 100 IOPS average for 14 days

**Measurement Period:** 14 days (336 hours)
**Sampling Frequency:** 5-minute intervals
**Data Points Required:** Minimum 95% data availability

**Exclusions:**
- Instances with tag `idle-exempt: true`
- Instances running scheduled jobs (check CloudWatch Events/Scheduler)
- Instances in auto-scaling groups (evaluate group, not individual instances)
- Instances with active SSH/RDP sessions in last 7 days
- Instances serving as bastion/jump hosts

**Special Cases:**
- **Windows Instances:** CPU threshold 10% (higher baseline due to OS overhead)
- **GPU Instances:** GPU utilization < 5% for 7 days (more expensive, shorter threshold)
- **Spot Instances:** CPU < 5% for 7 days (already cost-optimized)

#### Lambda Functions / Azure Functions / Cloud Functions

**Idle Definition:**
- Zero invocations in last 30 days
- No scheduled triggers configured
- Not referenced in any active workflows

**Measurement Period:** 30 days
**Cost Threshold:** Only flag if storage cost > $1/month

**Exclusions:**
- Functions with tag `disaster-recovery: true`
- Functions invoked by rare events (documented)
- Functions in active development (created < 30 days ago)

#### Container Instances (ECS/AKS/GKE)

**Idle Definition:**
- Task/Pod CPU < 5% for 14 days
- No active connections for 14 days
- Container restart count = 0 (not crashing)

**Measurement Period:** 14 days

**Exclusions:**
- Sidecar containers (logging, monitoring)
- Init containers
- Containers in DaemonSets
- Containers with HPA (Horizontal Pod Autoscaler)

### Database Resources

#### RDS / Azure SQL / Cloud SQL Instances

**Idle Definition:**
- **Connection Count:** Average < 10 connections for 30 consecutive days
- **Read/Write IOPS:** < 100 IOPS average for 30 days
- **Network Throughput:** < 1 MB/hour for 30 days
- **CPU Utilization:** < 10% for 30 days

**Measurement Period:** 30 days (longer due to database criticality)
**Sampling Frequency:** 5-minute intervals

**Exclusions:**
- Production databases (environment: production)
- Databases with tag `idle-exempt: true`
- Read replicas (evaluate primary instead)
- Databases in failover configurations
- Databases with active replication
- Databases modified in last 7 days

**Special Considerations:**
- **Multi-AZ Databases:** Higher cost, flag at 20 days instead of 30
- **Reserved Instances:** Already committed, lower priority for action
- **Development Databases:** More aggressive thresholds (20 days)

#### DynamoDB / Cosmos DB / Firestore

**Idle Definition:**
- Zero read/write requests for 30 days
- Provisioned capacity > 0 (not on-demand)
- Storage size not growing

**Measurement Period:** 30 days

**Exclusions:**
- Tables with on-demand billing (already cost-optimized)
- Tables with streams enabled (may be used for CDC)
- Global tables (replication targets)

#### ElastiCache / Redis Cache / Memorystore

**Idle Definition:**
- **Connection Count:** < 5 connections for 14 days
- **Cache Hit Rate:** N/A or 0% for 14 days
- **Network Throughput:** < 100 KB/hour for 14 days
- **CPU Utilization:** < 5% for 14 days

**Measurement Period:** 14 days

**Exclusions:**
- Caches in production with tag `always-on: true`
- Caches in Redis Cluster mode
- Caches with backup enabled (may be for DR)

### Storage Resources

#### S3 Buckets / Blob Storage / Cloud Storage

**Idle Definition:**
- Zero GET/PUT requests for 90 days
- No new objects added in 90 days
- No lifecycle policies configured
- Storage class: Standard (not already optimized)

**Measurement Period:** 90 days (longer due to archival nature)

**Exclusions:**
- Buckets with tag `archive: true`
- Buckets with versioning enabled (may be for compliance)
- Buckets with replication configured
- Buckets serving static websites
- Buckets with CloudFront distributions
- Buckets < 1 GB (negligible cost)

**Actions:**
- Recommend lifecycle policy to move to cheaper storage class
- Suggest archival to Glacier/Archive Storage
- Consider deletion if truly unused

#### EBS Volumes / Managed Disks / Persistent Disks

**Idle Definition:**
- **Status:** Available (unattached) for 7 days
- **Read/Write IOPS:** 0 for 7 days (if attached but unused)
- **Snapshot Exists:** Yes (safe to delete)

**Measurement Period:** 7 days

**Exclusions:**
- Volumes with tag `backup: true`
- Volumes in snapshot creation process
- Volumes attached to stopped instances (evaluate instance instead)
- Boot volumes (never delete without instance)

**Special Cases:**
- **Unattached Volumes:** Flag immediately if > 7 days
- **Attached but Unused:** Flag after 14 days
- **Expensive Volume Types (io2, Premium SSD):** Flag after 3 days

#### EFS / Azure Files / Filestore

**Idle Definition:**
- Zero client connections for 30 days
- No file modifications for 30 days
- Storage size not growing

**Measurement Period:** 30 days

**Exclusions:**
- File systems with tag `shared-storage: true`
- File systems in production
- File systems with backup policies

### Network Resources

#### Load Balancers (ALB/NLB/ELB, Azure LB, GCP LB)

**Idle Definition:**
- **Request Count:** < 5 requests per hour for 7 consecutive days
- **Active Connections:** 0 for 7 days
- **Healthy Targets:** 0 for 7 days
- **Network Throughput:** < 1 MB/hour for 7 days

**Measurement Period:** 7 days

**Exclusions:**
- Load balancers with tag `always-on: true`
- Load balancers in production (unless truly idle)
- Load balancers with SSL certificates (may be for future use)
- Load balancers with WAF rules

**Cost Impact:** High (load balancers are expensive even when idle)
**Priority:** High for cost savings

#### NAT Gateways / NAT Instances

**Idle Definition:**
- **Data Processed:** < 1 GB per day for 14 days
- **Active Connections:** < 10 per hour for 14 days

**Measurement Period:** 14 days

**Exclusions:**
- NAT gateways in production VPCs
- NAT gateways with tag `always-on: true`

**Alternative:** Consider NAT instances for low-traffic scenarios

#### Elastic IPs / Public IPs

**Idle Definition:**
- **Status:** Not associated with any resource for 7 days
- **Network Traffic:** 0 bytes for 7 days

**Measurement Period:** 7 days

**Cost Impact:** Low but accumulates
**Action:** Release immediately if confirmed idle

## Savings Estimation Rules

### Cost Calculation Methodology

**Current Cost:**
- Use actual billing data from last 30 days
- Average daily cost × 30 = monthly cost
- Include all associated costs (storage, network, etc.)

**Potential Savings:**
- **Stop Action:** 100% of compute cost, retain storage cost
- **Downsize Action:** Difference between current and recommended size
- **Delete Action:** 100% of all costs
- **Archive Action:** Difference between current and archive storage class

**Savings Confidence Levels:**
- **High (90-100%):** Resource clearly idle, no dependencies
- **Medium (70-89%):** Resource idle but has some dependencies
- **Low (50-69%):** Resource usage unclear, needs investigation

### Savings Calculation Examples

**Example 1: Idle EC2 Instance**
```
Resource: m5.2xlarge EC2 instance
Current Cost: $280/month
CPU Usage: 2% average (14 days)
Action: Stop instance
Savings: $280/month (compute) - $20/month (EBS) = $260/month
Confidence: High (95%)
```

**Example 2: Underutilized RDS Database**
```
Resource: db.r5.4xlarge RDS instance
Current Cost: $1,200/month
Connections: 5 average (30 days)
CPU: 8% average
Action: Downsize to db.r5.xlarge
Savings: $1,200 - $300 = $900/month
Confidence: Medium (80%)
```

**Example 3: Idle S3 Bucket**
```
Resource: S3 bucket (Standard storage)
Current Cost: $50/month (2 TB)
Access: 0 requests (90 days)
Action: Move to Glacier Deep Archive
Savings: $50 - $2 = $48/month
Confidence: High (95%)
```

### Annual Savings Projection

**Formula:** Monthly Savings × 12 × Confidence Level

**Reporting:**
- Conservative estimate: Use confidence level
- Optimistic estimate: Assume 100% confidence
- Realistic estimate: Use confidence level × 0.9

## Action Policies by Environment

### Development Environment

**Idle Threshold:** 14 days
**Action:** Auto-stop (with notification)

**Workflow:**
1. **Day 14:** Detect idle resource
2. **Day 14:** Send notification to owner
3. **Day 15:** Auto-stop resource (if no response)
4. **Day 30:** Send deletion warning
5. **Day 37:** Auto-delete (if still stopped and no response)

**Notification Content:**
```
⚠️ IDLE RESOURCE DETECTED - Development

Resource: EC2 Instance (i-0123456789abcdef0)
Type: m5.large
Cost: $70/month
Idle Period: 14 days (CPU < 5%)

Action: Will be STOPPED in 24 hours
To prevent: Reply "keep" or add tag idle-exempt:true

Estimated Savings: $60/month
Owner: john.doe@company.com
```

**Override Options:**
- Add tag `idle-exempt: true` (requires justification)
- Reply to notification with "keep" (valid for 30 days)
- Manually restart resource (resets idle timer)

### Staging Environment

**Idle Threshold:** 21 days
**Action:** Manual review required

**Workflow:**
1. **Day 21:** Detect idle resource
2. **Day 21:** Send notification to owner and team lead
3. **Day 23:** Team lead review required
4. **Day 28:** Escalate to management if no action
5. **Day 35:** Management decision required

**Notification Content:**
```
⚠️ IDLE RESOURCE DETECTED - Staging

Resource: RDS Instance (mydb-staging)
Type: db.r5.large
Cost: $300/month
Idle Period: 21 days (< 10 connections)

Action Required: Manual review by team lead
Options:
1. Stop instance (save $300/month)
2. Downsize to db.t3.medium (save $200/month)
3. Keep as-is (provide justification)

Review By: 2026-05-25
Owner: jane.smith@company.com
Team Lead: bob.jones@company.com
```

**Review Criteria:**
- Is resource needed for upcoming testing?
- Can it be stopped and started on-demand?
- Should it be downsized?
- Is it part of disaster recovery plan?

### Production Environment

**Idle Threshold:** 30 days
**Action:** Manual review required (no auto-actions)

**Workflow:**
1. **Day 30:** Detect idle resource
2. **Day 30:** Send notification to owner, team lead, and management
3. **Day 32:** Schedule review meeting
4. **Day 35:** Review meeting with stakeholders
5. **Day 40:** Implement approved action

**Notification Content:**
```
🔴 IDLE RESOURCE DETECTED - PRODUCTION

Resource: Load Balancer (prod-api-lb)
Type: Application Load Balancer
Cost: $25/month
Idle Period: 30 days (< 5 requests/hour)

⚠️ MANUAL REVIEW REQUIRED - NO AUTO-ACTIONS

Review Meeting: 2026-05-23 at 10:00 AM
Attendees: Owner, Team Lead, Infrastructure Lead

Questions to Address:
1. Is this load balancer still needed?
2. Is it part of disaster recovery?
3. Can it be deleted or replaced?
4. What is the risk of removal?

Estimated Savings: $25/month ($300/year)
Owner: alice.williams@company.com
```

**Review Requirements:**
- Architecture review
- Dependency analysis
- Risk assessment
- Rollback plan
- Approval from 2+ stakeholders

**Production Safeguards:**
- Never auto-stop production resources
- Never auto-delete production resources
- Require written approval for any action
- Implement changes during maintenance window
- Have rollback plan ready

## Monitoring and Alerting

### Idle Resource Detection

**Scan Frequency:**
- Development: Daily at 02:00 UTC
- Staging: Daily at 03:00 UTC
- Production: Daily at 04:00 UTC

**Detection Process:**
1. Query CloudWatch/Azure Monitor/Cloud Monitoring metrics
2. Calculate average utilization over threshold period
3. Check for exclusion tags
4. Verify resource state and dependencies
5. Calculate potential savings
6. Generate report and notifications

### Alert Channels

**Slack Notifications:**
- `#idle-resources-dev`: Development environment
- `#idle-resources-staging`: Staging environment
- `#idle-resources-prod`: Production environment (with @channel)

**Email Notifications:**
- Resource owner (always)
- Team lead (staging and production)
- Management (production only)

**Dashboard:**
- Real-time idle resource dashboard
- Filterable by environment, type, owner
- Sortable by cost savings potential
- Exportable reports

### Escalation Path

**Level 1: Owner (Day 0)**
- Notification sent to resource owner
- 48-hour response window
- Self-service remediation options

**Level 2: Team Lead (Day 2)**
- Escalate if no owner response
- Team lead review required
- 72-hour response window

**Level 3: Management (Day 5)**
- Escalate if no team lead action
- Management decision required
- 7-day response window

**Level 4: Automatic Action (Day 12 for dev)**
- Only for development environment
- Automatic stop/delete based on policy
- Final notification before action

## Reporting and Metrics

### Daily Idle Resource Report

**Recipients:** FinOps team, team leads
**Delivery:** 09:00 local time
**Content:**
- New idle resources detected (last 24 hours)
- Total idle resources by environment
- Potential monthly savings
- Resources pending action
- Resources recently remediated

### Weekly Idle Resource Summary

**Recipients:** Management, finance
**Delivery:** Monday 10:00 local time
**Content:**
- Weekly idle resource trends
- Savings realized from remediation
- Top idle resources by cost
- Compliance with action timelines
- Recommendations for policy improvements

### Monthly Idle Resource Analysis

**Recipients:** Executives, all stakeholders
**Delivery:** 1st business day of month
**Content:**
- Monthly idle resource statistics
- Total savings achieved
- Savings opportunity remaining
- Policy effectiveness metrics
- Success stories and lessons learned

### Key Performance Indicators

**Detection Metrics:**
- Idle resources detected per week
- Average idle duration before detection
- False positive rate (< 5% target)

**Action Metrics:**
- Time to remediation (by environment)
- Remediation rate (% of idle resources addressed)
- Auto-stop success rate (development)

**Savings Metrics:**
- Monthly savings realized
- Annual savings projection
- Savings as % of total cloud spend
- ROI of idle resource program

## Exception Handling

### Valid Exception Reasons

**Technical Reasons:**
- Disaster recovery standby
- Scheduled job runner (infrequent jobs)
- Development/testing environment (intentionally idle)
- Capacity reservation for future use

**Business Reasons:**
- Regulatory compliance requirement
- Customer SLA commitment
- Contractual obligation
- Strategic reserve capacity

### Exception Request Process

1. **Submit Request:**
   - Resource identifier
   - Exception reason
   - Expected duration
   - Business justification
   - Cost impact acknowledgment

2. **Approval Required:**
   - Team lead approval (all exceptions)
   - Finance approval (> $100/month)
   - Management approval (production resources)

3. **Documentation:**
   - Add tag `idle-exempt: true`
   - Add tag `idle-exempt-reason: [reason]`
   - Add tag `idle-exempt-until: [date]`
   - Record in exception registry

4. **Review:**
   - Quarterly review of all exceptions
   - Automatic expiration after 90 days
   - Renewal required with new justification

## Integration with Other Tools

### Cost Optimization Integration

- Idle resources feed into cost optimization recommendations
- Savings tracked against cost reduction goals
- Prioritized by savings potential

### Rightsizing Integration

- Underutilized resources (not fully idle) flagged for rightsizing
- Recommendations for smaller instance types
- Cost-benefit analysis provided

### Compliance Integration

- Idle resources checked for compliance violations
- Untagged idle resources prioritized for cleanup
- Compliance score improved by removing idle resources

## Continuous Improvement

### Monthly Policy Review

**Review Areas:**
- Threshold effectiveness (too aggressive or too lenient)
- False positive analysis
- Missed idle resources (false negatives)
- Action timeline appropriateness

**Adjustment Process:**
1. Analyze previous month's data
2. Gather feedback from teams
3. Propose policy changes
4. Test changes in development
5. Implement approved changes
6. Monitor impact

### Automation Enhancements

**Current Automation:**
- Automatic detection and notification
- Auto-stop for development (with safeguards)
- Scheduled reporting

**Future Automation:**
- Machine learning for usage pattern prediction
- Automatic rightsizing recommendations
- Smart scheduling (stop/start based on usage patterns)
- Predictive idle detection

## Review and Updates

This policy is reviewed monthly and updated to reflect:
- Effectiveness of current thresholds
- New resource types and services
- Changes in business requirements
- Feedback from resource owners
- Industry best practices

---

**Policy Owner:** FinOps Team  
**Approved By:** CTO & CFO  
**Next Review Date:** 2026-06-18