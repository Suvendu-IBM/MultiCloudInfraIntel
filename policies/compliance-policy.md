# Compliance Policy

**Policy ID:** POLICY-006  
**Version:** 1.0  
**Effective Date:** 2026-05-18  
**Governs Tool:** `check_compliance`

## Purpose

This policy defines mandatory compliance requirements for all cloud resources to ensure security, governance, cost accountability, and regulatory adherence across multi-cloud infrastructure.

## Scope

Applies to all resources across AWS, Azure, and GCP in all environments (production, staging, development, test).

## Mandatory Tagging Requirements

### Required Tags for All Resources

#### 1. Owner Tag

**Tag Key:** `owner`  
**Required:** Yes (Critical)  
**Format:** Valid email address or team identifier  
**Examples:**
- `owner: john.doe@company.com`
- `owner: team-platform`
- `owner: svc-dataprocessing@company.com`

**Validation Rules:**
- Must be a valid email format OR team identifier starting with "team-"
- Email must exist in company directory
- Team identifier must be in approved teams list
- Cannot be generic (admin@, root@, noreply@)
- Cannot be placeholder (unknown, tbd, temp)

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** 24 hours to remediate
- **Action:** Resource stopped after 48 hours (non-production)
- **Escalation:** Team lead notified immediately

#### 2. Cost Center Tag

**Tag Key:** `cost-center`  
**Required:** Yes (Critical)  
**Format:** CC-XXXX (where XXXX is 4-digit code)  
**Examples:**
- `cost-center: CC-1234`
- `cost-center: CC-5678`

**Validation Rules:**
- Must match pattern: `CC-[0-9]{4}`
- Must be in approved cost center list
- Must be active (not closed or archived)
- Must have budget allocated

**Approved Cost Centers:**
```
CC-1000: Platform Engineering
CC-1100: Data Engineering
CC-1200: Application Development
CC-1300: Security Operations
CC-1400: DevOps
CC-2000: Research & Development
CC-3000: IT Operations
CC-9999: Shared Services
```

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** 24 hours to remediate
- **Action:** Resource flagged in cost reports
- **Escalation:** Finance team notified

#### 3. Environment Tag

**Tag Key:** `environment`  
**Required:** Yes (Critical)  
**Format:** Lowercase, one of approved values  
**Allowed Values:**
- `production`: Production workloads
- `staging`: Pre-production testing
- `development`: Development and testing
- `test`: Automated testing environments

**Validation Rules:**
- Must be exactly one of the allowed values
- Case-sensitive (must be lowercase)
- Cannot be abbreviated (prod, dev, stg not allowed)

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** 24 hours to remediate
- **Action:** Resource cannot be promoted to production
- **Escalation:** Team lead notified

#### 4. Data Classification Tag

**Tag Key:** `data-classification`  
**Required:** Yes for data resources (storage, databases)  
**Format:** Lowercase, one of approved values  
**Allowed Values:**
- `public`: Publicly accessible data
- `internal`: Internal company data
- `confidential`: Confidential business data
- `restricted`: Highly sensitive data (PII, PHI, financial)

**Validation Rules:**
- Required for: S3/Blob/Cloud Storage, RDS/SQL/Cloud SQL, DynamoDB/Cosmos/Firestore
- Must match data sensitivity assessment
- Cannot be downgraded without security approval
- Restricted data requires additional controls

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** 12 hours to remediate
- **Action:** Public access blocked immediately
- **Escalation:** Security team notified immediately

### Optional but Recommended Tags

**Additional Tags:**
- `project`: Project identifier
- `application`: Application name
- `managed-by`: terraform/cloudformation/manual
- `backup-required`: true/false
- `compliance-scope`: hipaa/pci/sox/gdpr
- `maintenance-window`: day-time format
- `expiration-date`: ISO 8601 date

## Encryption Requirements

### Encryption at Rest

**Requirement:** All data storage resources MUST have encryption at rest enabled

#### Storage Services

**S3 Buckets / Blob Storage / Cloud Storage:**
- **Requirement:** Server-side encryption enabled
- **Allowed Methods:**
  - AWS: SSE-S3, SSE-KMS, SSE-C
  - Azure: Microsoft-managed keys or Customer-managed keys
  - GCP: Google-managed or Customer-managed encryption keys
- **Minimum:** AES-256 encryption
- **Recommended:** Customer-managed keys (CMK) for sensitive data

**Validation:**
- Check encryption configuration on bucket
- Verify default encryption is enabled
- Confirm encryption key is valid and accessible

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** Immediate remediation required
- **Action:** Block public access, enable encryption
- **Escalation:** Security team notified immediately

#### Database Services

**RDS / Azure SQL / Cloud SQL:**
- **Requirement:** Encryption at rest enabled
- **Allowed Methods:**
  - AWS: RDS encryption with KMS
  - Azure: Transparent Data Encryption (TDE)
  - GCP: Encryption with Cloud KMS
- **Minimum:** AES-256 encryption
- **Snapshots:** Must also be encrypted

**Validation:**
- Check database encryption status
- Verify encryption key is valid
- Confirm snapshots are encrypted

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** Cannot be enabled on existing unencrypted databases
- **Action:** Create encrypted copy, migrate data, delete unencrypted
- **Escalation:** Database team and security notified

**NoSQL Databases (DynamoDB/Cosmos/Firestore):**
- **Requirement:** Encryption at rest enabled
- **Default:** Usually enabled by default
- **Validation:** Confirm encryption is active

#### Block Storage

**EBS Volumes / Managed Disks / Persistent Disks:**
- **Requirement:** Encryption enabled
- **Scope:** All volumes (boot and data)
- **Snapshots:** Must also be encrypted

**Validation:**
- Check volume encryption status
- Verify encryption key
- Confirm snapshots are encrypted

**Non-Compliance Action:**
- **Severity:** High
- **Timeline:** 7 days to remediate
- **Action:** Create encrypted copy, migrate data
- **Escalation:** Infrastructure team notified

### Encryption in Transit

**Requirement:** All data transmission MUST use encryption in transit

**HTTPS/TLS Requirements:**
- Minimum TLS version: 1.2
- Recommended: TLS 1.3
- Strong cipher suites only
- Valid SSL/TLS certificates

**Application Load Balancers:**
- HTTPS listeners required for production
- HTTP to HTTPS redirect enabled
- SSL/TLS certificate from trusted CA
- Certificate expiration monitoring

**Database Connections:**
- SSL/TLS required for all connections
- Certificate validation enabled
- No plaintext connections allowed

**API Endpoints:**
- HTTPS only (no HTTP)
- API Gateway with SSL/TLS
- Certificate pinning for mobile apps

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** Immediate remediation required
- **Action:** Block unencrypted traffic
- **Escalation:** Security team notified immediately

## Public Access Rules

### Block Public Access for All Storage

**Requirement:** Public access MUST be blocked unless explicitly approved

#### S3 Buckets

**Default Configuration:**
- Block all public access enabled
- Block public ACLs: True
- Ignore public ACLs: True
- Block public bucket policies: True
- Restrict public buckets: True

**Exceptions Process:**
- Submit exception request with business justification
- Security review required
- Approval from CISO required
- Document in exception registry
- Quarterly review of all exceptions
- Implement additional controls (CloudFront, WAF)

**Validation:**
- Check bucket public access settings
- Scan for public ACLs
- Review bucket policies for public access
- Monitor access logs for public requests

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** Immediate remediation required
- **Action:** Block public access automatically
- **Escalation:** Security team notified immediately

#### Azure Blob Storage

**Default Configuration:**
- Allow Blob public access: Disabled
- Require secure transfer: Enabled
- Minimum TLS version: 1.2

**Validation:**
- Check storage account public access settings
- Verify container access levels
- Review SAS token usage

#### GCP Cloud Storage

**Default Configuration:**
- Uniform bucket-level access enabled
- Public access prevention: Enforced
- No allUsers or allAuthenticatedUsers permissions

**Validation:**
- Check bucket IAM policies
- Verify no public access grants
- Review signed URL usage

### Database Public Access

**Requirement:** Databases MUST NOT be publicly accessible

**RDS / Azure SQL / Cloud SQL:**
- Publicly accessible: False
- VPC/VNet only access
- Security groups restrict access to known IPs
- No 0.0.0.0/0 ingress rules

**Exceptions:**
- Development databases may allow specific IP ranges
- Must use strong authentication
- Must enable audit logging
- Quarterly review required

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** Immediate remediation required
- **Action:** Remove public access
- **Escalation:** Security and database teams notified immediately

### Compute Instance Public Access

**Requirement:** Minimize public IP assignments

**Best Practices:**
- Use load balancers for public-facing services
- Use bastion hosts for administrative access
- Use VPN for internal access
- Implement security groups/NSGs with least privilege

**Validation:**
- Identify instances with public IPs
- Verify security group rules
- Check for open ports (22, 3389, 3306, 5432, etc.)
- Review access logs

**Non-Compliance Action:**
- **Severity:** High
- **Timeline:** 7 days to remediate
- **Action:** Remove public IP or restrict access
- **Escalation:** Infrastructure team notified

## Backup Requirements

### Backup Policy by Environment

#### Production Resources

**Requirement:** Daily backups with defined RPO and RTO

**Recovery Point Objective (RPO): 24 hours**
- Maximum acceptable data loss: 24 hours
- Backup frequency: Daily minimum
- Critical systems: Hourly backups

**Recovery Time Objective (RTO): 4 hours**
- Maximum acceptable downtime: 4 hours
- Backup must be restorable within 4 hours
- Regular restore testing required

**Backup Configuration:**
- Automated daily backups
- Retention: 30 days minimum
- Cross-region replication for critical systems
- Encryption of backups required
- Backup verification and testing monthly

**Validation:**
- Check backup schedule is configured
- Verify backups are completing successfully
- Confirm retention policy is set
- Test restore process quarterly

**Non-Compliance Action:**
- **Severity:** Critical
- **Timeline:** 24 hours to configure backups
- **Action:** Resource flagged as non-compliant
- **Escalation:** Infrastructure and management notified

#### Staging Resources

**Requirement:** Weekly backups

**RPO:** 7 days  
**RTO:** 24 hours

**Backup Configuration:**
- Automated weekly backups
- Retention: 14 days minimum
- Encryption of backups required

#### Development Resources

**Requirement:** Optional (recommended for important dev data)

**RPO:** 7 days  
**RTO:** 48 hours

**Backup Configuration:**
- Manual or automated weekly backups
- Retention: 7 days minimum

### Backup Validation

**Monthly Backup Testing:**
- Select random backups for restore testing
- Verify data integrity
- Measure restore time
- Document results

**Quarterly Disaster Recovery Drills:**
- Full restore from backup
- Validate RTO and RPO
- Test failover procedures
- Update runbooks

## Compliance Monitoring

### Automated Compliance Checks

**Scan Frequency:**
- Critical checks: Every 4 hours
- High priority checks: Daily
- Medium priority checks: Weekly
- Low priority checks: Monthly

**Compliance Checks:**

**Tagging Compliance:**
- All required tags present
- Tag values valid
- Tag format correct

**Encryption Compliance:**
- Encryption at rest enabled
- Encryption in transit configured
- Valid encryption keys

**Access Control Compliance:**
- No public access (unless approved)
- Security groups follow least privilege
- IAM policies follow least privilege

**Backup Compliance:**
- Backup configured
- Backups completing successfully
- Retention policy set

**Network Compliance:**
- Resources in approved VPCs/VNets
- No direct internet access (unless approved)
- Network ACLs configured

### Compliance Scoring

**Scoring Methodology:**

**Per-Resource Score:**
- Each compliance check has a weight
- Critical checks: 10 points
- High checks: 5 points
- Medium checks: 2 points
- Low checks: 1 point

**Calculation:**
```
Resource Score = (Passed Checks Points / Total Possible Points) × 100
```

**Overall Compliance Score:**
```
Team Score = Average of all team's resource scores
Environment Score = Average of all resources in environment
Organization Score = Average of all resource scores
```

**Compliance Levels:**
- **Excellent:** 95-100% (Green)
- **Good:** 85-94% (Light Green)
- **Fair:** 70-84% (Yellow)
- **Poor:** 50-69% (Orange)
- **Critical:** <50% (Red)

### Compliance Reporting

**Daily Compliance Report:**
- New compliance violations (last 24 hours)
- Critical violations requiring immediate attention
- Compliance score by team
- Top violators

**Weekly Compliance Summary:**
- Compliance trends
- Violations by category
- Remediation progress
- Team compliance rankings

**Monthly Compliance Review:**
- Comprehensive compliance analysis
- Policy effectiveness review
- Recommendations for improvements
- Executive summary

## Violation Handling

### Violation Severity Levels

**Critical Violations:**
- Missing owner or cost-center tag
- Unencrypted sensitive data
- Public access to databases
- No backups for production resources

**High Violations:**
- Missing environment tag
- Unencrypted storage
- Overly permissive security groups
- Missing backups for staging

**Medium Violations:**
- Missing optional tags
- Weak encryption configuration
- Suboptimal network configuration

**Low Violations:**
- Inconsistent tag formatting
- Missing documentation
- Optimization opportunities

### Remediation Timelines

**Critical Violations:**
- **Detection:** Immediate alert
- **Notification:** Within 15 minutes
- **Remediation Required:** 24 hours
- **Escalation:** Team lead and security immediately
- **Auto-Remediation:** Enabled for some violations (e.g., block public access)

**High Violations:**
- **Detection:** Within 4 hours
- **Notification:** Within 1 hour of detection
- **Remediation Required:** 7 days
- **Escalation:** Team lead after 3 days

**Medium Violations:**
- **Detection:** Daily scan
- **Notification:** Daily digest
- **Remediation Required:** 30 days
- **Escalation:** Team lead after 14 days

**Low Violations:**
- **Detection:** Weekly scan
- **Notification:** Weekly digest
- **Remediation Required:** 90 days
- **Escalation:** Optional

### Auto-Remediation

**Enabled for:**
- Block public access on storage
- Enable default encryption on new buckets
- Add default tags from account/project
- Enable CloudTrail/Activity logging

**Requires Approval:**
- Modify security groups
- Delete resources
- Change encryption keys
- Modify IAM policies

**Never Auto-Remediate:**
- Production resources (manual review required)
- Resources with active connections
- Databases with data
- Resources tagged `auto-remediation: false`

## Compliance Exceptions

### Exception Request Process

**Valid Exception Reasons:**
- Technical limitation
- Third-party integration requirement
- Regulatory or compliance requirement
- Business-critical temporary need

**Request Requirements:**
1. **Justification:** Detailed business/technical reason
2. **Risk Assessment:** Security and operational risks
3. **Compensating Controls:** Alternative security measures
4. **Duration:** Specific timeframe (max 90 days)
5. **Approvals:** Required approvals based on severity

**Approval Requirements:**
- Critical violations: CISO approval required
- High violations: Security team approval
- Medium violations: Team lead approval
- Low violations: Self-service with documentation

**Exception Tracking:**
- Document in exception registry
- Add tag `compliance-exception: true`
- Add tag `exception-reason: [reason]`
- Add tag `exception-expires: [date]`
- Quarterly review of all exceptions
- Automatic expiration and re-evaluation

### Exception Monitoring

**Active Exception Review:**
- Weekly review of critical exceptions
- Monthly review of all exceptions
- Quarterly re-approval required
- Annual comprehensive audit

**Exception Metrics:**
- Number of active exceptions
- Exception duration
- Exception approval rate
- Exception expiration compliance

## Regulatory Compliance

### Industry Standards

**Supported Compliance Frameworks:**
- **HIPAA:** Healthcare data protection
- **PCI DSS:** Payment card data security
- **SOX:** Financial reporting controls
- **GDPR:** European data protection
- **SOC 2:** Service organization controls
- **ISO 27001:** Information security management

**Framework-Specific Requirements:**

**HIPAA Compliance:**
- PHI data must be tagged `data-classification: restricted`
- Encryption required (at rest and in transit)
- Access logging enabled
- Audit trail maintained
- Business Associate Agreements (BAA) documented

**PCI DSS Compliance:**
- Cardholder data must be tagged `compliance-scope: pci`
- Network segmentation required
- Strong access controls
- Regular security testing
- Quarterly compliance scans

**GDPR Compliance:**
- Personal data must be tagged `data-classification: restricted`
- Data residency requirements enforced
- Right to erasure capability
- Data processing agreements documented
- Privacy impact assessments completed

### Compliance Attestation

**Quarterly Attestation:**
- Team leads attest to compliance
- Review all resources under their ownership
- Confirm compliance with policies
- Document any exceptions or issues

**Annual Audit:**
- Comprehensive compliance audit
- Third-party assessment (if required)
- Remediation of findings
- Update policies based on audit results

## Integration with Other Policies

### Cost Policy Integration

- Compliance violations may indicate cost optimization opportunities
- Untagged resources cannot be properly allocated to cost centers
- Compliance score affects budget allocation decisions

### Security Policy Integration

- Compliance checks include security best practices
- Security incidents trigger compliance reviews
- Compliance violations may indicate security risks

### Operational Policy Integration

- Compliance requirements affect operational procedures
- Backup compliance ensures operational resilience
- Tagging compliance enables operational automation

## Training and Awareness

### Compliance Training

**Required Training:**
- New employee onboarding: Compliance basics
- Quarterly refresher: Policy updates
- Role-specific training: Deep dives for specific roles

**Training Topics:**
- Tagging requirements and best practices
- Encryption requirements
- Public access risks
- Backup and recovery procedures
- Compliance exception process

### Compliance Resources

**Documentation:**
- Compliance policy (this document)
- Quick reference guides
- Tagging standards
- Exception request templates
- Remediation playbooks

**Tools:**
- Compliance dashboard
- Auto-tagging scripts
- Compliance checker CLI
- Remediation automation

## Review and Updates

This policy is reviewed quarterly and updated to reflect:
- New regulatory requirements
- Changes in cloud services
- Security best practices
- Lessons learned from violations
- Feedback from teams

---

**Policy Owner:** Security Team & FinOps Team  
**Approved By:** CISO & CTO  
**Next Review Date:** 2026-08-18