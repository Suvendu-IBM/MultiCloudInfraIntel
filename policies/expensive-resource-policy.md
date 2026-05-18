# Expensive Resource Policy

**Policy ID:** POLICY-007  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `get_top_expensive_resources`

## Purpose

This policy defines criteria for identifying expensive cloud resources, establishes review processes, and provides guidelines for cost optimization and rightsizing to ensure efficient cloud spending.

## Scope

Applies to all cloud resources across AWS, Azure, and GCP that contribute significantly to overall cloud costs.

## Definition of "Expensive Resource"

### Primary Criteria

**Absolute Cost Threshold:**
- **Monthly Cost > $500:** Resource costs more than $500 per month
- Calculation: Based on last 30 days of actual usage
- Includes all associated costs (compute, storage, network, licensing)

**Relative Cost Threshold:**
- **>5% of Team Budget:** Resource represents more than 5% of team's monthly cloud budget
- Calculation: (Resource Cost / Team Budget) × 100 > 5%
- Evaluated monthly against current budget allocation

**Either Threshold Triggers "Expensive" Classification:**
- Resource meets absolute threshold ($500/month), OR
- Resource meets relative threshold (>5% of team budget), OR
- Both thresholds are met

### Cost Calculation Methodology

**Included Costs:**
- Compute costs (instance hours, vCPU, memory)
- Storage costs (disk, object storage, snapshots)
- Network costs (data transfer, load balancers)
- Database costs (instance, storage, IOPS, backups)
- Licensing costs (OS, database, software)
- Support costs (if allocated per resource)

**Excluded Costs:**
- Reserved Instance upfront payments (amortized separately)
- Savings Plan commitments (tracked separately)
- One-time purchases (tracked as CapEx)
- Credits and discounts (shown separately)

**Cost Attribution:**
- Direct costs: Attributed to specific resource
- Shared costs: Allocated proportionally (e.g., VPC costs)
- Indirect costs: Allocated based on usage (e.g., data transfer)

### Resource Grouping

**Individual Resources:**
- Single EC2 instance, RDS database, etc.
- Evaluated independently

**Resource Groups:**
- Auto-scaling groups (evaluated as a group)
- Database clusters (primary + replicas)
- Application stacks (all resources for one application)

**Grouping Rules:**
- Resources with same `application` tag grouped together
- Auto-scaling group members always grouped
- Database replicas grouped with primary
- Option to view individual or grouped costs

## Top N Configuration

### Dashboard Display

**Top 10 Resources (Default):**
- Use Case: Real-time monitoring dashboard
- Update Frequency: Every 4 hours
- Display: Current month-to-date costs
- Sorting: By cost (highest to lowest)

**Dashboard Content:**
```
TOP 10 EXPENSIVE RESOURCES - May 2026

Rank | Resource | Type | Environment | Cost (MTD) | % of Budget | Trend
-----|----------|------|-------------|------------|-------------|-------
1    | prod-db-primary | RDS | Production | $2,450 | 12.3% | ↑ 8%
2    | data-warehouse | Redshift | Production | $1,890 | 9.5% | → 2%
3    | ml-training-cluster | EMR | Development | $1,650 | 8.3% | ↓ 5%
4    | api-gateway-prod | API Gateway | Production | $1,200 | 6.0% | ↑ 15%
5    | cdn-distribution | CloudFront | Production | $980 | 4.9% | → 1%
...

Total Top 10: $12,450 (62.3% of total spend)
```

**Dashboard Features:**
- Click resource for detailed cost breakdown
- Filter by environment, team, or service type
- Export to CSV/PDF
- Set custom date range
- Compare to previous period

### Weekly Report

**Top 20 Resources:**
- Use Case: Weekly team review meetings
- Delivery: Monday 09:00 local time
- Recipients: Team leads, FinOps team
- Period: Previous 7 days

**Report Content:**
- Resource details (name, type, owner, environment)
- Weekly cost and trend
- Month-to-date cost
- Comparison to previous week
- Optimization recommendations
- Action items from previous week

**Report Format:**
```
WEEKLY EXPENSIVE RESOURCES REPORT
Week of May 11-17, 2026

Summary:
- Total spend: $18,500 (↑ 12% vs. previous week)
- Top 20 resources: $14,200 (76.8% of total)
- New expensive resources: 2
- Resources optimized: 3 (saved $450/week)

Top 20 Resources:
[Detailed table with 20 resources]

Optimization Opportunities:
1. prod-db-primary: Consider Reserved Instance (save $800/month)
2. ml-training-cluster: Use Spot instances (save $600/month)
3. api-gateway-prod: Review caching strategy (save $200/month)

Action Items:
- [ ] Review prod-db-primary sizing (Owner: John Doe, Due: May 20)
- [ ] Implement Spot for ml-training (Owner: Jane Smith, Due: May 22)
- [x] Optimize cdn-distribution (Completed: May 15, Saved: $150/month)
```

### Monthly Report

**Top 50 Resources:**
- Use Case: Monthly business review and planning
- Delivery: 1st business day of month at 10:00 local time
- Recipients: Management, finance, all team leads
- Period: Previous calendar month

**Report Content:**
- Comprehensive cost analysis
- Month-over-month trends
- Year-to-date comparison
- Budget variance analysis
- Optimization achievements
- Recommendations for next month
- Strategic initiatives

**Report Sections:**
1. **Executive Summary:** Key metrics and highlights
2. **Top 50 Resources:** Detailed cost breakdown
3. **Cost Trends:** Historical analysis and projections
4. **Optimization Wins:** Savings achieved
5. **Recommendations:** Prioritized action items
6. **Budget Impact:** Effect on annual budget

## Review Actions and Rightsizing Recommendations

### Automated Analysis

**Rightsizing Analysis Triggers:**
- Resource in top expensive list for 3+ consecutive weeks
- Cost increase >20% month-over-month
- Utilization metrics indicate over/under-provisioning
- New instance types available with better price/performance

**Analysis Components:**

**1. Utilization Analysis:**
- CPU utilization (average, peak, 95th percentile)
- Memory utilization (if available)
- Network throughput
- Disk I/O
- Database connections (for databases)

**2. Performance Requirements:**
- Current performance metrics
- SLA requirements
- Peak load handling
- Growth projections

**3. Cost-Performance Ratio:**
- Current cost per unit of work
- Alternative instance types
- Reserved Instance opportunities
- Savings Plan opportunities

### Rightsizing Recommendations

#### Compute Resources (EC2/VMs/GCE)

**Downsize Recommendation:**
```
Resource: prod-api-server-01 (m5.2xlarge)
Current Cost: $280/month
CPU Utilization: 15% average, 35% peak
Memory Utilization: 30% average

Recommendation: Downsize to m5.xlarge
Projected Cost: $140/month
Savings: $140/month ($1,680/year)
Risk: Low (sufficient headroom for peak loads)
Action: Test in staging, then implement in production
```

**Upsize Recommendation:**
```
Resource: prod-db-server-01 (m5.large)
Current Cost: $140/month
CPU Utilization: 85% average, 98% peak
Memory Utilization: 90% average

Recommendation: Upsize to m5.xlarge
Projected Cost: $280/month
Additional Cost: $140/month
Benefit: Improved performance, reduced latency, better user experience
Risk: Low (current resource is bottleneck)
Action: Schedule maintenance window for upgrade
```

**Instance Family Change:**
```
Resource: ml-training-01 (c5.4xlarge - compute optimized)
Current Cost: $500/month
Workload: Memory-intensive ML training

Recommendation: Change to r5.2xlarge (memory optimized)
Projected Cost: $450/month
Savings: $50/month
Benefit: Better suited for workload, improved performance
Action: Test with sample workload, then migrate
```

#### Database Resources

**Storage Optimization:**
```
Resource: prod-db-primary (db.r5.2xlarge, 1TB storage)
Current Cost: $800/month
Storage Utilization: 250 GB (25%)
IOPS: 3000 provisioned, 500 average used

Recommendation: 
1. Reduce storage to 500 GB (save $150/month)
2. Switch to GP3 with lower IOPS (save $100/month)
Total Savings: $250/month ($3,000/year)
Risk: Low (sufficient capacity with growth room)
```

**Read Replica Optimization:**
```
Resource: prod-db-replica-01 (db.r5.xlarge)
Current Cost: $400/month
Read Traffic: 50 queries/hour (very low)

Recommendation: Remove read replica, use primary for reads
Savings: $400/month ($4,800/year)
Risk: Medium (slight increase in primary load)
Mitigation: Monitor primary performance, can recreate if needed
```

#### Storage Resources

**Storage Class Optimization:**
```
Resource: backup-bucket (S3 Standard, 5 TB)
Current Cost: $115/month
Access Pattern: Accessed once per month for compliance

Recommendation: Move to S3 Glacier Deep Archive
Projected Cost: $5/month
Savings: $110/month ($1,320/year)
Risk: Low (access pattern supports archival storage)
Action: Implement lifecycle policy
```

**Snapshot Cleanup:**
```
Resource: prod-server-snapshots (500 snapshots, 10 TB)
Current Cost: $500/month
Analysis: 450 snapshots older than 90 days, never accessed

Recommendation: Delete snapshots older than 90 days
Savings: $450/month ($5,400/year)
Risk: Low (retain recent snapshots for recovery)
Action: Implement automated cleanup policy
```

### Reserved Instance and Savings Plan Recommendations

**Reserved Instance Opportunity:**
```
Resource: prod-db-primary (db.r5.2xlarge)
Current Cost: $800/month (On-Demand)
Usage Pattern: 24/7 for 12+ months

Recommendation: Purchase 1-year Reserved Instance
Projected Cost: $550/month
Savings: $250/month ($3,000/year)
Upfront Cost: $0 (No Upfront option)
Risk: Low (stable, long-term workload)
```

**Savings Plan Opportunity:**
```
Resources: Multiple EC2 instances (m5 family)
Current Cost: $2,500/month (On-Demand)
Usage Pattern: Consistent compute usage

Recommendation: Purchase Compute Savings Plan ($1,500/month commitment)
Projected Cost: $1,800/month
Savings: $700/month ($8,400/year)
Flexibility: Can change instance types/regions
Risk: Low (commitment matches usage pattern)
```

### Spot Instance Opportunities

**Spot Instance Recommendation:**
```
Resource: ml-training-cluster (10x c5.4xlarge)
Current Cost: $5,000/month (On-Demand)
Workload: Batch processing, fault-tolerant

Recommendation: Use Spot Instances with fallback to On-Demand
Projected Cost: $1,500/month (70% discount)
Savings: $3,500/month ($42,000/year)
Risk: Medium (interruptions possible)
Mitigation: Implement checkpointing, use Spot Fleet
```

## Review Process

### Weekly Review Meeting

**Attendees:**
- Team lead
- Resource owners
- FinOps representative
- Technical lead (optional)

**Agenda:**
1. Review top 20 expensive resources
2. Discuss cost trends and anomalies
3. Review optimization recommendations
4. Assign action items
5. Follow up on previous action items

**Duration:** 30 minutes

**Outcomes:**
- Approved optimization actions
- Assigned owners and deadlines
- Updated resource tags (if needed)
- Documented decisions

### Monthly Review Meeting

**Attendees:**
- Management
- All team leads
- Finance representative
- FinOps team
- Infrastructure lead

**Agenda:**
1. Review top 50 expensive resources
2. Analyze month-over-month trends
3. Review budget performance
4. Discuss strategic optimizations
5. Plan for next month
6. Review policy effectiveness

**Duration:** 60 minutes

**Outcomes:**
- Strategic optimization initiatives
- Budget adjustments (if needed)
- Policy updates (if needed)
- Cross-team collaboration opportunities

### Quarterly Business Review

**Attendees:**
- Executives
- Finance leadership
- All team leads
- FinOps team

**Agenda:**
1. Quarterly cost analysis
2. Optimization achievements
3. Budget performance
4. Strategic initiatives
5. Annual planning (Q4 only)

**Duration:** 90 minutes

**Outcomes:**
- Strategic direction
- Budget allocation for next quarter
- Major optimization projects
- Policy and process improvements

## Optimization Tracking

### Action Item Management

**Action Item Template:**
```
Action: Downsize prod-api-server-01 from m5.2xlarge to m5.xlarge
Owner: John Doe
Due Date: May 25, 2026
Priority: Medium
Estimated Savings: $140/month
Status: In Progress
Steps:
1. [x] Analyze utilization (Completed: May 15)
2. [x] Test in staging (Completed: May 18)
3. [ ] Schedule maintenance window (Due: May 22)
4. [ ] Implement in production (Due: May 25)
5. [ ] Monitor for 7 days (Due: June 1)
```

**Status Tracking:**
- **Not Started:** Action identified but not begun
- **In Progress:** Work underway
- **Testing:** Changes being validated
- **Completed:** Implemented and verified
- **Blocked:** Waiting on dependency or approval
- **Cancelled:** No longer needed or feasible

### Savings Tracking

**Savings Calculation:**
```
Baseline Cost: Cost before optimization (30-day average)
Current Cost: Cost after optimization (30-day average)
Savings: Baseline Cost - Current Cost
Annualized Savings: Monthly Savings × 12
```

**Savings Verification:**
- Wait 30 days after implementation
- Compare actual costs to baseline
- Verify no performance degradation
- Document actual vs. projected savings

**Savings Reporting:**
- Weekly: Savings from last 7 days
- Monthly: Cumulative monthly savings
- Quarterly: Cumulative quarterly savings
- Annual: Total annual savings achieved

### Success Metrics

**Key Performance Indicators:**

**Cost Metrics:**
- Total spend on top 50 resources
- Percentage of total spend (target: <80%)
- Month-over-month cost trend
- Cost per unit of work

**Optimization Metrics:**
- Number of optimization actions completed
- Total savings achieved
- Average time to implement optimization
- Optimization success rate

**Efficiency Metrics:**
- Average resource utilization
- Percentage of resources rightsized
- Reserved Instance/Savings Plan coverage
- Spot Instance adoption rate

## Alert Configuration

### Cost Increase Alerts

**Significant Increase (>20%):**
```
Alert: Expensive Resource Cost Spike

Resource: prod-db-primary
Previous Cost: $800/month
Current Cost: $1,000/month
Increase: 25% ($200/month)

Action Required: Investigate cause within 24 hours
Possible Causes:
- Increased usage/traffic
- Configuration change
- Pricing change
- Data growth

Investigate: [Link to detailed analysis]
```

**Recipients:**
- Resource owner
- Team lead
- FinOps team

**New Expensive Resource:**
```
Alert: New Resource Exceeds Expensive Threshold

Resource: new-ml-cluster
Type: EMR Cluster
Cost: $650/month (first 7 days)
Projected Monthly: $2,800/month

Action Required: Review and justify within 48 hours
Questions:
- Is this expected?
- Is it properly sized?
- Is it temporary or permanent?
- Can it be optimized?

Review: [Link to resource details]
```

**Recipients:**
- Resource creator
- Team lead
- FinOps team

## Reporting and Dashboards

### Real-Time Dashboard

**Widgets:**
1. **Top 10 Expensive Resources:** Current month-to-date
2. **Cost Trend:** Last 30 days
3. **Budget Status:** Percentage used
4. **Optimization Opportunities:** Prioritized list
5. **Recent Changes:** Resources added/removed from top list

**Filters:**
- Environment (production, staging, development)
- Team/Cost Center
- Resource Type
- Date Range

**Actions:**
- Drill down into resource details
- View cost breakdown
- See optimization recommendations
- Create action item
- Export data

### Weekly Email Report

**Content:**
- Top 20 expensive resources
- Week-over-week changes
- New expensive resources
- Optimization wins
- Action items due this week

**Format:** HTML email with embedded charts

### Monthly Executive Report

**Content:**
- Executive summary (1 page)
- Top 50 resources analysis
- Cost trends and projections
- Optimization achievements
- Strategic recommendations

**Format:** PDF with executive-friendly visualizations

## Integration with Other Policies

### Budget Policy Integration

- Expensive resources tracked against team budgets
- Budget alerts consider expensive resource costs
- Budget planning includes expensive resource projections

### Idle Resource Policy Integration

- Expensive idle resources prioritized for action
- Higher urgency for expensive + idle combination
- Savings potential amplified

### Compliance Policy Integration

- Expensive resources require proper tagging
- Compliance violations on expensive resources escalated
- Cost optimization considers compliance requirements

## Continuous Improvement

### Monthly Policy Review

**Review Areas:**
- Threshold effectiveness ($500 and 5% appropriate?)
- Top N configuration (10/20/50 appropriate?)
- Recommendation accuracy
- Savings realization rate

**Adjustment Process:**
1. Analyze previous month's data
2. Gather feedback from teams
3. Propose policy changes
4. Test changes with historical data
5. Implement approved changes
6. Monitor impact

### Automation Enhancements

**Current Automation:**
- Automatic expensive resource detection
- Automated rightsizing recommendations
- Scheduled reporting

**Future Automation:**
- Machine learning for usage prediction
- Automatic Reserved Instance recommendations
- Predictive cost modeling
- Automated testing of optimizations

## Review and Updates

This policy is reviewed monthly and updated to reflect:
- Changes in cloud pricing
- New instance types and services
- Organizational budget changes
- Feedback from optimization efforts
- Industry best practices

---

**Policy Owner:** FinOps Team  
**Approved By:** CFO & CTO  
**Next Review Date:** 2026-06-18