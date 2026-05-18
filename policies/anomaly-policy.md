# Anomaly Detection Policy

**Policy ID:** POLICY-003  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `get_cost_anomaly`

## Purpose

This policy establishes the framework for detecting, classifying, and responding to cost anomalies across multi-cloud infrastructure to prevent budget overruns and identify optimization opportunities.

## Scope

Applies to all cloud spending across AWS, Azure, and GCP, covering all services, environments, and cost centers.

## Anomaly Detection Methodology

### Baseline Calculation

**7-Day Rolling Average (Default):**
- Calculate average daily cost for previous 7 days
- Exclude weekends if business operates Monday-Friday only
- Exclude known maintenance windows
- Update baseline daily at 00:00 UTC

**Alternative Baselines:**
- 14-day rolling average: For more stable baseline (less sensitive)
- 30-day rolling average: For long-term trend analysis
- Same-day-last-week: For weekly cyclical patterns
- Same-day-last-month: For monthly cyclical patterns

### Anomaly Threshold

**Default Threshold: 20% Above Baseline**
- Formula: `Anomaly if Current Cost > (Baseline * 1.20)`
- Rationale: Balances sensitivity with false positive reduction
- Applied uniformly across all services initially

**Dynamic Thresholds by Service Category:**

**High Variability Services (30% threshold):**
- Compute: EC2, Azure VMs, GCE (auto-scaling workloads)
- Serverless: Lambda, Azure Functions, Cloud Functions
- Batch Processing: EMR, Dataflow, Batch jobs

**Medium Variability Services (20% threshold - default):**
- Databases: RDS, Azure SQL, Cloud SQL
- Storage: S3, Blob Storage, Cloud Storage
- Networking: Data transfer, Load balancers

**Low Variability Services (10% threshold):**
- Reserved Instances: Predictable monthly costs
- Support Plans: Fixed monthly costs
- Domain Registration: Annual fixed costs

## Lookback Period

**Default: 30 Days**
- Provides sufficient historical context
- Captures monthly cyclical patterns
- Balances data volume with relevance

**Extended Lookback (90 Days):**
- Use for quarterly trend analysis
- Identify seasonal patterns
- Validate persistent anomalies

**Short Lookback (7 Days):**
- Use for rapid response scenarios
- Focus on immediate issues
- Higher sensitivity to recent changes

**Lookback Period Selection Rules:**
- New resources (<30 days old): Use 7-day lookback
- Stable resources: Use 30-day lookback
- Seasonal analysis: Use 90-day lookback
- Post-incident review: Use custom range

## Severity Classification

### Medium Severity (20-40% Above Baseline)

**Characteristics:**
- Cost increase: 20-40% above 7-day average
- Duration: Single day or intermittent
- Impact: Moderate budget concern

**Response Actions:**
- Automated Slack notification to `#cloud-costs-alerts`
- Log in anomaly tracking system
- Team lead review within 24 hours
- Document findings in weekly report

**Example Scenarios:**
- Unexpected traffic spike
- Batch job running longer than usual
- Development environment left running overnight
- Increased data transfer during deployment

### High Severity (40-60% Above Baseline)

**Characteristics:**
- Cost increase: 40-60% above 7-day average
- Duration: Multiple consecutive days or significant single-day spike
- Impact: Serious budget concern

**Response Actions:**
- Immediate Slack notification with @channel mention
- Email to team lead and finance
- Investigation required within 4 hours
- Root cause analysis within 24 hours
- Action plan to prevent recurrence

**Example Scenarios:**
- Misconfigured auto-scaling policy
- Runaway process consuming resources
- Unintended production deployment
- Data processing job stuck in loop
- Storage bucket receiving unexpected data volume

### Critical Severity (>60% Above Baseline)

**Characteristics:**
- Cost increase: >60% above 7-day average
- Duration: Any duration
- Impact: Critical budget risk

**Response Actions:**
- **Immediate (within 15 minutes):**
  - Slack notification with @here mention to `#cloud-costs-critical`
  - Email to team lead, finance, and management
  - SMS to on-call engineer
  - Create incident ticket (P1 priority)

- **Within 1 Hour:**
  - Incident response team assembled
  - Initial assessment completed
  - Containment actions initiated if needed

- **Within 4 Hours:**
  - Root cause identified
  - Remediation plan approved
  - Implementation started

- **Within 24 Hours:**
  - Issue resolved or contained
  - Post-incident review scheduled
  - Documentation completed

**Example Scenarios:**
- Cryptocurrency mining malware
- DDoS attack causing massive data transfer
- Accidental deployment to wrong region/account
- Database replication failure causing data duplication
- Misconfigured backup creating excessive snapshots

## Exclusion Rules

### Maintenance Windows

**Scheduled Maintenance:**
- Suppress anomaly detection during planned maintenance
- Maintenance window must be registered 24 hours in advance
- Maximum duration: 8 hours
- Automatic re-enablement after window closes

**Registration Requirements:**
- Maintenance ticket number
- Approver name
- Expected cost impact
- Start and end time (UTC)
- Affected services/resources

**Example Maintenance Windows:**
- Database migration: 4-hour window
- Infrastructure upgrade: 6-hour window
- Disaster recovery test: 8-hour window

### First-of-Month Spikes

**Known Monthly Patterns:**
- Month-end reporting jobs (last 3 days of month)
- Monthly backup cycles (1st of month)
- Billing cycle processing (1st-3rd of month)
- Monthly data aggregation jobs

**Handling Rules:**
- Increase threshold by 50% during first 3 days of month
- Compare to same period previous month instead of 7-day average
- Document expected spike in advance
- Alert only if exceeds historical pattern by >30%

**Example Adjustments:**
- Normal threshold: 20%
- First-of-month threshold: 30%
- Alert if: Current > (Last Month Same Period * 1.30)

### Planned Events

**Business Events:**
- Product launches
- Marketing campaigns
- Black Friday/Cyber Monday
- End of fiscal year processing

**Technical Events:**
- Load testing
- Disaster recovery drills
- Data migration projects
- Platform upgrades

**Exclusion Process:**
1. Submit exclusion request 48 hours in advance
2. Include expected cost increase (percentage or dollar amount)
3. Specify duration and affected resources
4. Obtain approval from finance and management
5. Document in exclusion registry
6. Review actual vs. expected after event

### One-Time Purchases

**Excluded from Anomaly Detection:**
- Reserved Instance upfront payments
- Savings Plan commitments
- Annual support plan renewals
- Domain registration renewals
- SSL certificate purchases

**Handling:**
- Track separately in capital expenditure reports
- Amortize over commitment period
- Include in budget planning but not daily anomaly detection

## Anomaly Investigation Workflow

### Step 1: Initial Detection (Automated)

**System Actions:**
- Calculate deviation from baseline
- Classify severity level
- Identify affected services and resources
- Generate alert with context
- Create investigation ticket

**Alert Content:**
- Current cost vs. baseline
- Percentage increase
- Affected services (top 5 contributors)
- Time period
- Historical comparison chart
- Direct link to detailed analysis

### Step 2: Triage (Within 1 Hour for High/Critical)

**Investigator Actions:**
- Review alert details
- Check for known maintenance or planned events
- Verify data accuracy (not a billing error)
- Identify primary cost driver
- Assess business impact
- Determine if immediate action needed

**Triage Outcomes:**
- **False Positive:** Close ticket, adjust detection rules if needed
- **Expected Spike:** Document reason, close ticket
- **Legitimate Anomaly:** Proceed to investigation
- **Critical Issue:** Escalate immediately

### Step 3: Root Cause Analysis

**Investigation Areas:**

**Resource Level:**
- Which specific resources increased?
- When did the increase start?
- What changed (configuration, usage, pricing)?
- Who made recent changes?

**Service Level:**
- Which services are affected?
- Is it usage increase or pricing change?
- Are multiple resources affected?
- Is it isolated or widespread?

**Account/Environment Level:**
- Is it specific to one environment?
- Are multiple teams affected?
- Is it a cross-service issue?
- Could it be a security incident?

**Tools for Investigation:**
- Cloud provider cost explorer
- Resource tagging analysis
- CloudTrail/Activity logs
- Monitoring dashboards
- Application logs

### Step 4: Remediation

**Immediate Actions (Critical Severity):**
- Stop runaway resources if safe to do so
- Scale down auto-scaling groups
- Disable problematic services temporarily
- Block suspicious traffic
- Engage security team if needed

**Short-Term Actions (High Severity):**
- Optimize resource configurations
- Adjust auto-scaling policies
- Fix application bugs
- Update deployment procedures
- Implement cost controls

**Long-Term Actions (All Severities):**
- Update architecture for cost efficiency
- Implement better monitoring
- Enhance automation
- Update policies and procedures
- Train team on cost awareness

### Step 5: Documentation

**Required Documentation:**
- Root cause summary
- Timeline of events
- Actions taken
- Cost impact (actual and prevented)
- Lessons learned
- Preventive measures implemented

**Documentation Location:**
- Incident ticket system
- Knowledge base article
- Monthly cost review presentation
- Anomaly pattern database

## Anomaly Patterns and Signatures

### Common Anomaly Patterns

**Pattern 1: Gradual Increase**
- Characteristics: Steady daily increase over 7+ days
- Common Causes: Data growth, user growth, feature adoption
- Response: Capacity planning review, optimization opportunities

**Pattern 2: Sudden Spike**
- Characteristics: Single-day 2x-10x increase
- Common Causes: Misconfiguration, incident, attack
- Response: Immediate investigation, potential rollback

**Pattern 3: Step Change**
- Characteristics: Permanent increase to new baseline
- Common Causes: New feature launch, infrastructure change
- Response: Budget adjustment, validate expected behavior

**Pattern 4: Cyclical Spike**
- Characteristics: Regular pattern (daily, weekly, monthly)
- Common Causes: Scheduled jobs, business cycles
- Response: Adjust baseline, optimize scheduling

**Pattern 5: Weekend Drop**
- Characteristics: Lower costs on weekends
- Common Causes: Reduced business activity
- Response: Consider auto-scaling for weekends

### Anomaly Signatures by Service

**Compute Anomalies:**
- Unexpected instance launches
- Instances running in wrong region
- Oversized instance types
- Instances not stopped after hours

**Storage Anomalies:**
- Rapid data growth
- Excessive snapshot creation
- Data transfer spikes
- Replication issues

**Database Anomalies:**
- Increased IOPS usage
- Storage growth
- Backup failures causing retries
- Query performance issues

**Network Anomalies:**
- Data transfer spikes
- Cross-region traffic
- Internet egress increases
- NAT gateway usage spikes

## Reporting and Metrics

### Daily Anomaly Report

**Recipients:** FinOps team, team leads
**Content:**
- Number of anomalies detected (by severity)
- Total cost impact
- Top 5 anomalies by cost
- Resolution status
- Trends vs. previous day

### Weekly Anomaly Summary

**Recipients:** Management, finance
**Content:**
- Weekly anomaly count and trends
- Total cost impact and savings from early detection
- Root cause distribution
- Mean time to detection (MTTD)
- Mean time to resolution (MTTR)
- Recurring anomalies requiring attention

### Monthly Anomaly Analysis

**Recipients:** Executives, all stakeholders
**Content:**
- Monthly anomaly statistics
- Cost impact analysis
- Pattern analysis and trends
- Policy effectiveness review
- Recommendations for improvements
- Success stories and lessons learned

### Key Performance Indicators (KPIs)

**Detection Metrics:**
- Anomaly detection rate: Target >95% of actual issues
- False positive rate: Target <10%
- Mean time to detection: Target <1 hour

**Response Metrics:**
- Mean time to triage: Target <1 hour (high/critical)
- Mean time to resolution: Target <4 hours (critical), <24 hours (high)
- Escalation rate: Track percentage requiring escalation

**Impact Metrics:**
- Cost prevented through early detection
- Budget variance reduction
- Incident recurrence rate

## Continuous Improvement

### Monthly Policy Review

**Review Areas:**
- Threshold effectiveness (too sensitive or not sensitive enough)
- Exclusion rule accuracy
- False positive analysis
- Missed anomalies (false negatives)
- Response time performance

**Adjustment Process:**
1. Analyze previous month's data
2. Identify improvement opportunities
3. Propose policy changes
4. Test changes in non-production
5. Implement approved changes
6. Monitor impact

### Machine Learning Enhancement

**Future Capabilities:**
- Automatic baseline adjustment based on patterns
- Predictive anomaly detection
- Anomaly clustering and categorization
- Automated root cause suggestions
- Cost forecasting with anomaly consideration

## Compliance and Audit

### Audit Requirements

**Logged Information:**
- All anomaly detections (with full context)
- All investigations (actions and findings)
- All exclusions (with approvals)
- All policy changes (with justification)

**Retention Period:**
- Anomaly logs: 2 years
- Investigation records: 3 years
- Exclusion records: 3 years
- Policy change history: Indefinite

### Access Control

**View Anomalies:**
- All employees: Own team's anomalies
- Team leads: Full team anomalies
- FinOps team: All anomalies
- Executives: Summary reports

**Investigate Anomalies:**
- Team leads: Own team
- FinOps team: All teams
- Security team: Security-related anomalies

**Modify Policy:**
- FinOps team: Propose changes
- Finance: Approve changes
- CTO: Final approval for major changes

## Review and Updates

This policy is reviewed monthly and updated to reflect:
- Effectiveness of current thresholds
- New anomaly patterns discovered
- Changes in cloud usage patterns
- Feedback from investigation teams
- Industry best practices

---

**Policy Owner:** FinOps Team  
**Approved By:** CFO & CTO  
**Next Review Date:** 2026-06-18