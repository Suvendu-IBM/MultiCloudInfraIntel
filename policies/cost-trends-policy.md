# Cost Trends Policy

**Policy ID:** POLICY-002  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `get_cost_trends`

## Purpose

This policy defines the standards for analyzing, reporting, and acting upon cost trends across multi-cloud infrastructure to ensure financial accountability and cost optimization.

## Scope

Applies to all cloud spending across AWS, Azure, and GCP for all teams and environments.

## Default Date Ranges

### Standard Reporting Periods

**Last 30 Days (Default):**
- Use Case: Daily operational monitoring
- Granularity: Daily data points
- Comparison: Current 30 days vs. previous 30 days
- Refresh: Every 24 hours at 00:00 UTC

**Current Month:**
- Use Case: Monthly budget tracking
- Granularity: Daily data points
- Comparison: Month-to-date vs. same period last month
- Refresh: Every 24 hours at 00:00 UTC
- Projection: Extrapolate to end of month based on current trend

**Last Quarter:**
- Use Case: Quarterly business reviews
- Granularity: Weekly data points
- Comparison: Current quarter vs. previous quarter
- Refresh: Weekly on Mondays at 00:00 UTC

### Custom Date Ranges

**Allowed Custom Ranges:**
- Minimum: 7 days
- Maximum: 365 days
- Must align with calendar boundaries for month/quarter comparisons

**Restricted Ranges:**
- Cannot query data older than 13 months (AWS Cost Explorer limitation)
- Cannot query future dates
- Cannot create ranges spanning multiple years (use year-over-year comparison instead)

## Service Inclusion/Exclusion Rules

### Included Services (Default)

**Compute Services:**
- AWS: EC2, Lambda, ECS, EKS, Fargate
- Azure: Virtual Machines, App Service, Container Instances, AKS
- GCP: Compute Engine, Cloud Functions, GKE, Cloud Run

**Storage Services:**
- AWS: S3, EBS, EFS, Glacier
- Azure: Blob Storage, Disk Storage, File Storage
- GCP: Cloud Storage, Persistent Disk, Filestore

**Database Services:**
- AWS: RDS, DynamoDB, Aurora, ElastiCache, Redshift
- Azure: SQL Database, Cosmos DB, Database for PostgreSQL/MySQL
- GCP: Cloud SQL, Firestore, BigQuery, Memorystore

**Network Services:**
- AWS: VPC, CloudFront, Route53, Load Balancers, Data Transfer
- Azure: Virtual Network, CDN, DNS, Load Balancer, Bandwidth
- GCP: VPC, Cloud CDN, Cloud DNS, Load Balancing, Network Egress

**Analytics & AI/ML:**
- AWS: Athena, EMR, SageMaker, Glue
- Azure: Synapse Analytics, Machine Learning, Data Factory
- GCP: BigQuery, Dataflow, AI Platform, Dataproc

### Excluded Services (Default)

**Support & Credits:**
- AWS Support plans (tracked separately)
- Azure Support plans (tracked separately)
- GCP Support charges (tracked separately)
- Promotional credits and discounts (shown separately)
- Reserved Instance upfront payments (amortized separately)

**Tax & Fees:**
- Sales tax
- VAT
- Regulatory fees
- Marketplace fees (unless specifically requested)

**Free Tier Usage:**
- Services within free tier limits
- Trial credits
- Educational credits

### Service Grouping Rules

Services are grouped by:
1. **Category:** Compute, Storage, Database, Network, Analytics, Security, Management
2. **Sub-category:** Specific service type
3. **Environment:** Production, Staging, Development
4. **Cost Center:** Team or project allocation

## Currency and Formatting Rules

### Currency Standards

**Primary Currency:** USD (United States Dollar)
- All costs reported in USD by default
- Exchange rates updated daily at 00:00 UTC
- Historical exchange rates used for past data (no retroactive adjustments)

**Secondary Currencies (Optional):**
- EUR (Euro) - for European teams
- GBP (British Pound) - for UK teams
- INR (Indian Rupee) - for India teams

**Currency Conversion Rules:**
- Use official exchange rates from European Central Bank
- Round to 2 decimal places
- Display original currency in tooltips/details
- Note exchange rate and date in reports

### Number Formatting

**Cost Display:**
- Format: `$1,234.56` (comma thousands separator, 2 decimal places)
- Small amounts (<$0.01): Display as `$0.00` with actual value in tooltip
- Large amounts (>$1M): Option to display as `$1.2M` in summaries
- Negative values (credits): Display as `($123.45)` or `-$123.45`

**Percentage Display:**
- Format: `12.34%` (2 decimal places)
- Trend indicators: `↑ 15.5%` (increase), `↓ 8.2%` (decrease), `→ 0.5%` (stable)
- Color coding: Red (>10% increase), Yellow (5-10% increase), Green (decrease), Gray (stable ±5%)

**Date Display:**
- Format: `YYYY-MM-DD` (ISO 8601)
- Date ranges: `2026-04-01 to 2026-04-30`
- Relative dates: `Last 30 days`, `Current month`, `Previous quarter`

### Rounding Rules

**Cost Rounding:**
- Individual line items: 2 decimal places
- Subtotals: 2 decimal places
- Grand totals: 2 decimal places
- Percentages: 2 decimal places
- No rounding until final display (maintain precision in calculations)

**Aggregation Rules:**
- Sum costs before rounding
- Apply rounding only to displayed values
- Maintain audit trail of unrounded values
- Reconcile totals to match cloud provider bills (±$0.01 tolerance)

## Trend Analysis Rules

### Trend Calculation Methods

**Simple Trend:**
- Compare current period to previous period
- Formula: `((Current - Previous) / Previous) * 100`
- Display: Percentage change with direction indicator

**Moving Average:**
- 7-day moving average for daily data
- 4-week moving average for weekly data
- Smooths out daily fluctuations
- Highlights underlying trends

**Compound Growth Rate:**
- For multi-period analysis
- Formula: `((End Value / Start Value)^(1/Number of Periods) - 1) * 100`
- Use for quarterly and annual trends

### Trend Thresholds

**Normal Variation:** ±5%
- No alert required
- Standard operational fluctuation
- Document in monthly reports

**Moderate Increase:** 5-15%
- Yellow alert
- Notify team lead
- Investigate within 48 hours
- Document findings

**Significant Increase:** 15-30%
- Orange alert
- Notify team lead and finance
- Investigate within 24 hours
- Provide explanation and action plan

**Critical Increase:** >30%
- Red alert
- Immediate notification to team lead, finance, and management
- Investigate immediately
- Emergency review meeting within 4 hours
- Implement cost controls if needed

### Seasonality Adjustments

**Known Seasonal Patterns:**
- Month-end processing spikes (last 3 days of month)
- Quarter-end reporting loads (last week of quarter)
- Holiday periods (reduced usage)
- Business cycle patterns (fiscal year-end)

**Adjustment Rules:**
- Compare to same period last year for seasonal trends
- Exclude known one-time events from trend analysis
- Document seasonal patterns in trend reports
- Use seasonally-adjusted baselines for alerts

## Reporting Requirements

### Daily Cost Trend Report

**Recipients:** Team leads, FinOps team
**Delivery:** Email at 08:00 local time
**Content:**
- Yesterday's total cost vs. previous day
- Week-to-date cost vs. previous week
- Month-to-date cost vs. budget
- Top 5 cost increases (>10%)
- Top 5 cost decreases (>10%)

### Weekly Cost Trend Report

**Recipients:** Team leads, finance, management
**Delivery:** Monday at 09:00 local time
**Content:**
- Last 7 days cost trend
- Week-over-week comparison
- Month-to-date progress vs. budget
- Service-level breakdown
- Environment-level breakdown
- Anomalies and explanations

### Monthly Cost Trend Report

**Recipients:** All stakeholders, executives
**Delivery:** 1st business day of month at 10:00 local time
**Content:**
- Full month cost summary
- Month-over-month comparison
- Year-to-date trend
- Budget variance analysis
- Cost optimization opportunities
- Forecast for next month

## Alert Configuration

### Alert Channels

**Slack Notifications:**
- Channel: `#cloud-costs`
- Frequency: Real-time for critical, daily digest for moderate
- Format: Structured message with charts

**Email Notifications:**
- Recipients: Based on severity and ownership
- Frequency: Immediate for critical, daily digest for others
- Format: HTML email with embedded charts

**Dashboard Alerts:**
- Location: Cost management dashboard
- Visibility: All team members
- Persistence: Until acknowledged

### Alert Suppression

**Maintenance Windows:**
- Suppress alerts during planned maintenance
- Document maintenance window in advance
- Resume alerts after maintenance completion

**Known Events:**
- Suppress alerts for documented one-time events
- Require approval for suppression
- Automatic re-enablement after event

## Data Quality Standards

### Data Accuracy

**Validation Rules:**
- Cross-check with cloud provider bills (monthly)
- Reconcile totals within ±1% tolerance
- Investigate discrepancies >1%
- Document and resolve all discrepancies

**Data Freshness:**
- AWS: 24-hour delay (Cost Explorer limitation)
- Azure: 24-48 hour delay
- GCP: 24-hour delay
- Display data age in all reports

### Data Completeness

**Required Data Points:**
- Cost amount
- Service name
- Resource tags (owner, cost-center, environment)
- Usage quantity
- Pricing unit

**Missing Data Handling:**
- Flag incomplete records
- Estimate based on similar resources
- Document estimation methodology
- Update when actual data available

## Compliance and Audit

### Audit Trail

**Required Logging:**
- All cost trend queries (user, timestamp, parameters)
- All alert generations (type, recipient, timestamp)
- All data exports (user, timestamp, scope)
- All policy exceptions (approver, reason, duration)

**Retention:**
- Query logs: 90 days
- Alert logs: 1 year
- Export logs: 1 year
- Exception logs: 3 years

### Access Control

**View Access:**
- All employees: Own team's costs
- Team leads: Full team costs
- Finance: All costs
- Executives: All costs with aggregations

**Export Access:**
- Team leads: Own team data
- Finance: All data
- Auditors: Read-only all data

## Review and Updates

This policy is reviewed quarterly and updated to reflect:
- Changes in cloud provider pricing models
- New services and features
- Organizational structure changes
- Lessons learned from cost incidents

---

**Policy Owner:** FinOps Team  
**Approved By:** CFO  
**Next Review Date:** 2026-08-18