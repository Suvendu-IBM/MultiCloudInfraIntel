# Multi-Cloud Infrastructure Intelligence - Complete Agentic AI Solution

An end-to-end Agentic AI solution for multi-cloud infrastructure intelligence using IBM Consulting Advantage (ICA), Context Studio, and custom MCP servers.

## Solution Overview

This solution provides natural language querying and automated reasoning across **AWS, Azure, and GCP** for:
- **Resource Inventory**: Unified view of all cloud resources across multiple providers
- **Cost Analysis**: Cost trends, anomaly detection, budget tracking
- **Idle Resource Detection**: Identify waste and estimate savings
- **Compliance Checking**: Tagging, encryption, and public access validation

**Multi-Cloud Capability**: The MCP server code is fully implemented for AWS, Azure, and GCP. Currently tested with AWS credentials only. To enable Azure and GCP, simply add their respective credentials to the configuration.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (ICA Playground)                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ICA AGENTIC APP STUDIO                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │            Multi-Cloud Infrastructure Analyst Agent                 │   │
│  │                        (15 Tools Total)                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                │                      │                      │               │
│    ┌───────────────────┼───────────────────────┐                            │
│    ▼                   ▼                       ▼                            │
│  ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────────┐    │
│  │ Context Studio    │ │ Multi-Cloud MCP   │ │ Workflows             │    │
│  │ MCP Gateway       │ │ Gateway           │ │ (LangGraph)           │    │
│  │ (7 Policy Tools)  │ │ (8 Data Tools)    │ │                       │    │
│  └─────────┬─────────┘ └─────────┬─────────┘ └───────────────────────┘    │
│            │                      │                                         │
└────────────┼───────────────────────┼─────────────────────────────────────────┘
             │                      │
             ▼                      ▼
┌─────────────────────┐  ┌─────────────────────────────────────────────────┐
│  Context Studio     │  │             Hosted in EC2 Instance (AWS)                 │
│   (IBM Cloud)       │  │  ┌─────────────────────────────────────────────┐│
│                     │  │  │      MCP Server (Python/FastMCP)            ││
│ • JSON-LD Schema    │  │  │                                             ││
│ • 8 Policy Files    │  │  │  8 Tools:                                   ││
│ • Knowledge Graph   │  │  │  • get-resource-summary                     ││
│                     │  │  │  • get-cost-trends                          ││
└─────────────────────┘  │  │  • get-cost-anomaly                         ││
                         │  │  • get-new-resources-since                  ││
                         │  │  • find-idle-resources                      ││
                         │  │  • check-compliance                         ││
                         │  │  • get-top-expensive-resources              ││
                         │  │  • get-budget-health                        ││
                         │  └─────────────────────────────────────────────┘│
                         └─────────────────────────────────────────────────┘
                                           │
                                           ▼
                         ┌─────────────────────────────────────────┐
                         │         Multi-Cloud APIs                │
                         │  ┌─────────────┬─────────────┬─────────┐│
                         │  │    AWS      │   Azure     │   GCP   ││
                         │  │  • EC2      │ • VMs       │ • CE    ││
                         │  │  • Cost Exp │ • Cost Mgmt │ • Billing││
                         │  │  • CloudWatch│ • Monitor  │ • Monitor││
                         │  │  • Config   │ • Policy    │ • Asset ││
                         │  └─────────────┴─────────────┴─────────┘│
                         └─────────────────────────────────────────┘
```

## Prerequisites

- IBM Consulting Advantage (ICA) access
- **Cloud Provider Credentials** (one or more):
  - **AWS**: EC2, Cost Explorer, CloudWatch, Config permissions
  - **Azure**: Virtual Machines, Cost Management, Monitor, Policy (optional)
  - **GCP**: Compute Engine, Billing, Cloud Monitoring, Asset Inventory (optional)
- Python 3.11+ for local development
- Git
- Bob Access to build Custom Multicloud MCP, Schema for context studio, etc.

**Note**: The solution is fully multi-cloud capable. Currently tested with AWS credentials. Azure and GCP support is code-ready and can be enabled by adding credentials.

## Complete Implementation Guide

### Phase 1: Context Studio Setup (Policies)

#### Step 1.1: Generate JSON-LD Schema

Use Bob to generate the schema:

```bash
# Prompt Bob with:
"Generate a JSON-LD schema for Multi-Cloud Infrastructure Policies with entities for:
- IdleResourcePolicy (cpuThresholdPercent, lookbackDays)
- CostAnomalyPolicy (thresholdPercent, lookbackDays)
- CompliancePolicy (ruleType, mandatoryTags)
- BudgetPolicy (warningThresholdPercent, criticalThresholdPercent)
- CloudResource (resourceId, provider, type, region, state, createdTime, tags)"
```

Save the output as `schema/multi-cloud-policies.jsonld`.

#### Step 1.2: Create 8 Policy Markdown Files

Create these files in the `policies/` directory:

1. **resource-policy.md** - Resource discovery and filtering rules
2. **cost-trends-policy.md** - Cost analysis standards
3. **anomaly-policy.md** - Anomaly detection thresholds
4. **new-resource-policy.md** - New resource tracking rules
5. **idle-resource-policy.md** - Idle resource definitions
6. **compliance-policy.md** - Tagging, encryption, access rules
7. **expensive-resource-policy.md** - Cost threshold definitions
8. **budget-policy.md** - Budget allocation and alerting

#### Step 1.3: Import to Context Studio

1. Navigate to Context Studio in ICA
2. Click "Start with a Schema" → "Create schema" → "Import schema"
3. Upload `multi-cloud-policies.jsonld`
4. Name: "Multi-Cloud Policies" → Publish
5. Click "Create a Context" → Name: "Multi-Cloud Infrastructure Context"
6. Link the schema
7. Go to "Source & Data" tab → Upload all 8 policy markdown files
8. Click "Expose as MCP" → Copy the MCP Server URL and Bearer Token

### Phase 2: Deploy MCP Server on EC2

#### Step 2.1: Launch EC2 Instance

```bash
# Launch t2.micro Ubuntu 22.04 instance
# Security Group: Allow SSH (22) and Custom TCP (8000) from 0.0.0.0/0
```

#### Step 2.2: Setup EC2

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>

# Clone repository
git clone https://github.com/Suvendu-IBM/MultiCloudInfraIntel.git
cd MultiCloudInfraIntel

# Create virtual environment
python3 -m venv mcp-env
source mcp-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (required for current testing)
aws configure
# Enter: AWS Access Key ID, Secret Key, region (ap-south-1)

# Optional: Configure Azure credentials
# az login
# az account set --subscription <subscription-id>

# Optional: Configure GCP credentials
# gcloud auth application-default login
# gcloud config set project <project-id>
```

#### Step 2.3: Run as Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/mcp-server.service
```

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

#### Step 3.1: Create Agentic App

1. Navigate to ICA Agentic App Studio
2. Click "Create an Agentic App"
3. Name: "Multi-Cloud Intelligence App"
4. Category: "IT Operations & Cloud Management"
5. Description: "Agentic AI for multi-cloud cost, resource, and compliance intelligence"

#### Step 3.2: Add MCP Servers

**Multi-Cloud MCP (Infrastructure Data):**
- Name: "Multi-Cloud MCP"
- URL: `http://<EC2-PUBLIC-IP>:8000/sse`
- Transport: Remote (HTTP/S)

**Context Studio MCP (Policies):**
- Name: "MultiCloudIntel-Policies"
- URL: (from Context Studio exposure)
- Authentication: Bearer Token (from Context Studio)

#### Step 3.3: Create Virtual Server

1. Go to "MCP Servers" → "Access MCP Gateway"
2. Go to "Virtual Server" tab → "Create Virtual Server"
3. Name: `multi-cloud-mcp-virtual-server`
4. Select ALL tools from both MCP servers (15 total tools)
5. Save

#### Step 3.4: Create Agent

```yaml
# Agent Orchestration YAML
api-version: aiis.ibm.com/v1alpha1
kind: agent-orchestration
metadata:
  name: multi-cloud-infrastructure-analyst
  platform: ica
  framework: strands
spec:
  orchestration:
    type: single
  models:
    - name: gpt-5.2
      provider: ica
      config:
        temperature: 0.2
        max-tokens: 4096
  tools:
    # Multi-Cloud MCP (8 tools)
    - name: get-resource-summary
      type: mcp
      tool-id: multi-cloud-mcp-get-resource-summary
    - name: get-cost-trends
      type: mcp
      tool-id: multi-cloud-mcp-get-cost-trends
    - name: get-cost-anomaly
      type: mcp
      tool-id: multi-cloud-mcp-get-cost-anomaly
    - name: get-new-resources-since
      type: mcp
      tool-id: multi-cloud-mcp-get-new-resources-since
    - name: find-idle-resources
      type: mcp
      tool-id: multi-cloud-mcp-find-idle-resources
    - name: check-compliance
      type: mcp
      tool-id: multi-cloud-mcp-check-compliance
    - name: get-top-expensive-resources
      type: mcp
      tool-id: multi-cloud-mcp-get-top-expensive-resources
    - name: get-budget-health
      type: mcp
      tool-id: multi-cloud-mcp-get-budget-health
    # Context Studio Policies (7 tools)
    - name: context-policies-vector-query
      type: mcp
      tool-id: multicloudintel-policies-context-broker-vector-query
    - name: context-policies-graph-query
      type: mcp
      tool-id: multicloudintel-policies-context-broker-graph-query
    - name: context-policies-hybrid-query
      type: mcp
      tool-id: multicloudintel-policies-context-broker-hybrid-query
    - name: get-context-metadata
      type: mcp
      tool-id: multicloudintel-policies-context-broker-get-context-metadata
    - name: get-context-schema
      type: mcp
      tool-id: multicloudintel-policies-context-broker-get-context-schema
    - name: context-policies-post-events
      type: mcp
      tool-id: multicloudintel-policies-context-broker-post-events
    - name: context-policies-get-context-id
      type: mcp
      tool-id: multicloudintel-policies-context-broker-get-contexts
  agents:
    - name: multi-cloud-infra-analyst
      type: supervisor
      role: Multi-Cloud Infrastructure Analyst
      instructions: |
        You are a production-grade multi-cloud infrastructure analyst.
        
        MANDATORY EXECUTION ORDER:
        1. Query Context Studio FIRST for policies
        2. Call infrastructure tools with policy values
        3. Compare results and provide actionable insights
        
        FIXED CONTEXT:
        - context_id: ctx_eeac88f77918
        - AgentPersona: multi-cloud-infrastructure-analyst
        - Default AWS region: ap-south-1
        
        Always include Tool Trace showing which tools were called.
      model: gpt-5.2
```

#### Step 3.5: Create Workflow

1. Go to "Workflow" page → "Create New Workflow"
2. Name: "MulticloudIntelFlow"
3. Add components: Chat Input → ICA Agent → Chat Output
4. Connect the components
5. Save

### Phase 4: Testing

#### Step 4.1: Test in ICA Playground

Ask these questions in sequence:

```bash
# Test 1: Policy Retrieval
"hi"

# Test 2: Resource Listing
"List all resources"

# Test 3: Idle Detection
"Find idle resources"

# Test 4: Compliance Check
"Check compliance"
```

#### Step 4.2: Expected Results

| Query | Expected Response |
|-------|-------------------|
| "hi" | Agent introduces capabilities |
| "List all resources" | Returns resources from configured cloud providers |
| "Find idle resources" | Returns idle instances with CPU utilization metrics |
| "Check compliance" | Returns tagging and encryption violations across clouds |

**Note**: Results shown are from AWS testing. With Azure/GCP credentials configured, the agent will query all three cloud providers simultaneously.

## The 8 MCP Tools

| # | Tool Name | Description | Cloud Support |
|---|-----------|-------------|---------------|
| 1 | get-resource-summary | Unified resource inventory across clouds | AWS, Azure, GCP |
| 2 | get-cost-trends | Cost trends by provider and service | AWS, Azure, GCP |
| 3 | get-cost-anomaly | Detect statistically significant cost anomalies | AWS, Azure, GCP |
| 4 | get-new-resources-since | Identify resources created after a given date | AWS, Azure, GCP |
| 5 | find-idle-resources | Detect idle or underutilized infrastructure | AWS, Azure, GCP |
| 6 | check-compliance | Check tagging, encryption, public access | AWS, Azure, GCP |
| 7 | get-top-expensive-resources | Identify highest-cost resources | AWS, Azure, GCP |
| 8 | get-budget-health | Evaluate actual vs projected spend against budget | AWS, Azure, GCP |

**All tools are multi-cloud ready**. The code supports AWS, Azure, and GCP. Currently tested with AWS credentials only.

## Context Studio Policies (8 Files)

| # | Policy File | Purpose |
|---|-------------|---------|
| 1 | resource-policy.md | Resource discovery, filtering, tagging rules |
| 2 | cost-trends-policy.md | Cost analysis standards and reporting |
| 3 | anomaly-policy.md | Anomaly detection thresholds (20% default) |
| 4 | new-resource-policy.md | New resource tracking (7-day window) |
| 5 | idle-resource-policy.md | Idle definitions (CPU <5% for 14 days) |
| 6 | compliance-policy.md | Mandatory tags, encryption, access rules |
| 7 | expensive-resource-policy.md | Cost threshold definitions (>$500/month) |
| 8 | budget-policy.md | Budget allocation and alerting (80%/100%) |

## Project Structure

```
MultiCloudInfraIntel/
├── mcp_server.py              # Main MCP server with 8 tools
├── requirements.txt           # Python dependencies
├── config.yaml                # Configuration file
├── policies/                  # 8 policy markdown files for Context Studio
│   ├── resource-policy.md
│   ├── cost-trends-policy.md
│   ├── anomaly-policy.md
│   ├── new-resource-policy.md
│   ├── idle-resource-policy.md
│   ├── compliance-policy.md
│   ├── expensive-resource-policy.md
│   └── budget-policy.md
├── schema/                    # JSON-LD schema for Context Studio
│   └── multi-cloud-policies.jsonld
├── tests/                     # Unit and integration tests
└── docs/                      # Documentation
```

## Performance Metrics

| Operation | Response Time |
|-----------|---------------|
| Resource listing | ~78 seconds |
| Idle detection | ~30 seconds |
| Compliance check | ~267 milliseconds |
| Policy retrieval | ~22 seconds |

## Troubleshooting

### MCP Server not accessible

```bash
# Check service status
sudo systemctl status mcp-server

# Check logs
sudo journalctl -u mcp-server -f

# Verify port is open
sudo netstat -tlnp | grep 8000
```

### ICA Gateway shows "Invalid Host header"

```bash
# Restart with correct host binding
python mcp_server.py --transport http --port 8000 --host 0.0.0.0
```

### No resources found from cloud providers

```bash
# Verify AWS credentials
aws sts get-caller-identity
aws ec2 describe-instances --region ap-south-1

# Verify Azure credentials (if configured)
az account show
az vm list --output table

# Verify GCP credentials (if configured)
gcloud auth list
gcloud compute instances list
```

### Enabling Multi-Cloud Support

The solution is **fully multi-cloud capable**. To enable Azure and GCP:

1. **Azure Setup**:
```bash
# Install Azure CLI
pip install azure-cli azure-mgmt-compute azure-mgmt-monitor azure-mgmt-costmanagement

# Login and set subscription
az login
az account set --subscription <subscription-id>
```

2. **GCP Setup**:
```bash
# Install GCP SDK
pip install google-cloud-compute google-cloud-monitoring google-cloud-billing

# Authenticate
gcloud auth application-default login
gcloud config set project <project-id>
```

3. **Restart MCP Server**:
```bash
sudo systemctl restart mcp-server
```

The MCP server will automatically detect and query all configured cloud providers.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Copyright © 2026. All rights reserved.

## Contact

For questions or support, please refer to the project repository or contact the development team.