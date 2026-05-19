# Multi-Cloud Infrastructure Intelligence - Implementation Guide

## Overview

This guide provides a complete walkthrough of the production-grade Agentic AI solution for multi-cloud infrastructure intelligence using IBM Consulting Advantage (ICA), Context Studio, and custom MCP servers.

## Solution Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ USER INTERFACE (ICA Playground) │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ICA AGENTIC APP STUDIO │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Multi-Cloud Infrastructure Analyst Agent │ │
│ │ (15 Tools Total) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────────┐ │
│ │ Context Studio │ │ Multi-Cloud MCP │ │ Workflows │ │
│ │ MCP Gateway │ │ Gateway │ │ (LangGraph) │ │
│ │ (7 Policy Tools) │ │ (8 Data Tools) │ │ │ │
│ └─────────┬─────────┘ └─────────┬─────────┘ └───────────────────────┘ │
└────────────┼───────────────────────┼───────────────────────────────────────┘
│ │
▼ ▼
┌─────────────────────┐ ┌─────────────────────────────────────────────────┐
│ Context Studio │ │ EC2 Instance (AWS) │
│ (IBM Cloud) │ │ MCP Server (Python/FastMCP) │
│ • JSON-LD Schema │ │ 8 Tools: get-resource-summary, │
│ • 8 Policy Files │ │ get-cost-trends, get-cost-anomaly, │
│ • Knowledge Graph │ │ get-new-resources-since, │
└─────────────────────┘ │ find-idle-resources, check-compliance, │
│ get-top-expensive-resources, │
│ get-budget-health │
└─────────────────────────────────────────────────┘
│
▼
┌─────────────────────┐
│ AWS APIs │
│ • EC2 │
│ • Cost Explorer │
│ • CloudWatch │
│ • Config │
└─────────────────────┘

## Implementation Phases

### Phase 1: Context Studio Setup

#### Step 1.1: Generate JSON-LD Schema

Use Bob to generate the schema:

```bash
# Prompt Bob:
"Generate a JSON-LD schema for Multi-Cloud Infrastructure Policies with entities for:
- IdleResourcePolicy (cpuThresholdPercent, lookbackDays)
- CostAnomalyPolicy (thresholdPercent, lookbackDays)
- CompliancePolicy (ruleType, mandatoryTags)
- BudgetPolicy (warningThresholdPercent, criticalThresholdPercent)
- CloudResource (resourceId, provider, type, region, state, createdTime, tags)"
```

#### Step 1.2: Import to Context Studio

1. Navigate to Context Studio in ICA
2. "Start with a Schema" → "Create schema" → "Import schema"
3. Upload `schema/multi-cloud-policies.jsonld`
4. Name: "Multi-Cloud Policies" → Publish
5. "Create a Context" → Name: "Multi-Cloud Infrastructure Context"
6. Link the schema
7. "Source & Data" tab → Upload 8 policy files from `policies/` folder
8. "Expose as MCP" → Copy URL and Bearer Token

### Phase 2: Deploy MCP Server on EC2

#### Step 2.1: Launch EC2 Instance

- AMI: Ubuntu 22.04 LTS
- Instance Type: t2.micro (free tier eligible)
- Security Group: Allow SSH (22) and Custom TCP (8000) from 0.0.0.0/0

#### Step 2.2: Setup EC2

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>

# Clone repository
git clone https://github.com/Suvendu-IBM/MultiCloudInfraIntel.git
cd MultiCloudInfraIntel

# Setup virtual environment
python3 -m venv mcp-env
source mcp-env/bin/activate
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

#### Step 2.3: Run as Systemd Service

Create `/etc/systemd/system/mcp-server.service`:

```ini
[Unit]
Description=Multi-Cloud MCP Server
After=network.target network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/MultiCloudInfraIntel
Environment="PATH=/home/ubuntu/MultiCloudInfraIntel/mcp-env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/ubuntu/MultiCloudInfraIntel/mcp-env/bin/python /home/ubuntu/MultiCloudInfraIntel/mcp_server.py --transport http --port 8000 --host 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
sudo systemctl status mcp-server
```

### Phase 3: ICA Agentic App Studio Setup

#### Step 3.1: Add MCP Servers

| Server | URL | Auth |
|--------|-----|------|
| Multi-Cloud MCP | http://<EC2-IP>:8000/sse | None |
| Context Studio Policies | (from Context Studio) | Bearer Token |

#### Step 3.2: Create Virtual Server

- Name: `multi-cloud-mcp-virtual-server`
- Select ALL tools from both MCP servers (15 total)

#### Step 3.3: Deploy Agent

Use the YAML configuration from the main README.md.

### Phase 4: Testing

```bash
# In ICA Playground, test:
"List all resources"
"Find idle resources"
"Check compliance"
```

## Performance Benchmarks

| Operation | Response Time |
|-----------|---------------|
| Policy retrieval | ~22 seconds |
| Resource listing | ~78 seconds |
| Idle detection | ~30 seconds |
| Compliance check | ~267 milliseconds |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid Host header | Run with `--host 0.0.0.0` |
| EC2 connection refused | Check security group port 8000 |
| No AWS resources | Verify `aws sts get-caller-identity` |