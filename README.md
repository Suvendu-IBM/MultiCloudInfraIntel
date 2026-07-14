# MultiCloud Intelligence

> An enterprise-grade Agentic AI solution for unified multi-cloud infrastructure intelligence — powered by IBM Consulting Advantage, Context Studio, and a React + FastAPI web interface.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Key Features](#key-features)
- [Business Value](#business-value)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
  - [Phase 1 — Context Studio Setup](#phase-1--context-studio-setup)
  - [Phase 2 — MCP Server Deployment](#phase-2--mcp-server-deployment)
  - [Phase 3 — ICA Agent Configuration](#phase-3--ica-agent-configuration)
  - [Phase 4 — Web Application Setup](#phase-4--web-application-setup)
- [Testing](#testing)
- [MCP Tools Reference](#mcp-tools-reference)
- [Context Studio Policies](#context-studio-policies)
- [Performance Metrics](#performance-metrics)
- [Troubleshooting](#troubleshooting)
- [Multi-Cloud Enablement](#multi-cloud-enablement)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

**MultiCloud Intelligence** is an end-to-end Agentic AI platform that gives infrastructure and FinOps teams a single natural language interface to query, analyse, and govern resources across AWS, Azure, and GCP simultaneously.

The solution combines:
- A **custom MCP server** exposing 8 multi-cloud infrastructure tools
- An **IBM Context Studio** knowledge graph enforcing governance policies
- An **ICA Agent** (15 tools, Strands runtime) orchestrated via IBM Consulting Advantage
- A **React + FastAPI web application** providing a browser-based chat interface

> **Current status**: Fully implemented and tested on AWS. Azure and GCP are code-complete and activate automatically once credentials are supplied.

---

## Problem Statement

Organizations operating across multiple cloud providers face four compounding challenges:

**1. Visibility Gap**
- No unified view of resources, costs, or compliance across AWS, Azure, and GCP
- Manual aggregation from separate consoles delays decision-making by hours or days

**2. Uncontrolled Spend**
- Idle resources consume 30–40% of cloud budgets ($17.6B wasted industry-wide annually)
- Cost anomalies are detected weeks after occurrence — too late to prevent overruns

**3. Compliance & Security Risk**
- Resources deployed without mandatory tags make cost allocation impossible
- Manual audits take days or weeks; violations are discovered reactively
- Average cost of a compliance violation: **$4.24M** *(IBM Security Report)*

**4. Operational Inefficiency**
- Engineers spend 60–70% of time on manual reporting and cloud-specific querying
- Knowledge is siloed across platforms with no common query language

---

## Solution Overview

MultiCloud Intelligence replaces manual cloud operations with a conversational AI agent that:

- Queries **AWS, Azure, and GCP simultaneously** from a single interface
- Applies **governance policies** from a Context Studio knowledge graph on every response
- Delivers **structured, actionable insights** — not raw API dumps
- Provides a **browser-based chat UI** accessible to any team member without CLI skills

### Real-World Use Cases

<details>
<summary><strong>Use Case 1 — Monthly Cost Optimization (15 min vs 4–6 hours)</strong></summary>

```
User:  "Show me idle resources across all clouds"
Agent: [Queries policies] → [Scans AWS, Azure, GCP] → [Returns 23 idle instances]
       Estimated monthly savings: $12,450

User:  "Check for cost anomalies this month"
Agent: [Detects 3 anomalies] → Azure VM costs up 45% due to new dev environment
       Recommendation: Right-size or schedule shutdown
```
</details>

<details>
<summary><strong>Use Case 2 — Compliance Audit Preparation (5 min vs 2–3 days)</strong></summary>

```
User:  "Run compliance check across all clouds"
Agent: [Applies compliance policies] → [Scans 1,247 resources]
       - 34 resources missing mandatory tags
       - 7 unencrypted S3 buckets
       - 2 publicly accessible databases
       [Generates detailed compliance report with remediation steps]
```
</details>

<details>
<summary><strong>Use Case 3 — New Resource Tracking</strong></summary>

```
User:  "Show new resources created in the last week"
Agent: [Queries all clouds] → 15 new resources found
       - 8 EC2 instances (AWS), 4 VMs (Azure), 3 Compute Engine instances (GCP)
       [Flags 5 resources without proper tagging]
```
</details>

<details>
<summary><strong>Use Case 4 — Budget Health Monitoring</strong></summary>

```
User:  "What's our budget health status?"
Agent: - AWS:   78% of budget ($234K/$300K) — On track
       - Azure: 92% of budget ($184K/$200K) — Warning threshold
       - GCP:  105% of budget ($105K/$100K) — Over budget
       [Recommends immediate cost optimization actions]
```
</details>

---

## Key Features

| Capability | Detail |
|---|---|
| **Natural Language Queries** | Ask questions in plain English — no CLI or API knowledge required |
| **Unified Multi-Cloud View** | Single interface for AWS, Azure, and GCP simultaneously |
| **Agentic AI Reasoning** | Context-aware agent applies governance policies before responding |
| **Policy Knowledge Graph** | IBM Context Studio enforces tagging, encryption, and budget rules |
| **Real-time Anomaly Detection** | Statistical analysis flags cost spikes >20% above baseline |
| **Browser Chat UI** | React + TypeScript webapp with cloud-provider selector and Markdown rendering |
| **Idle Resource Detection** | Identifies instances with CPU <5% for 14 consecutive days |
| **Compliance Monitoring** | Checks tagging, encryption, public access, backup, and logging rules |
| **Budget Tracking** | Proactive warnings at 80% utilisation; critical alerts at 100% |

---

## Business Value

### Quantitative Targets

| Metric | Baseline | Target | Method |
|---|---|---|---|
| Cloud waste reduction | — | 30–40% | Monthly idle resource cost comparison |
| Manual analysis time | 20 hrs/week | 6 hrs/week | Team surveys |
| Compliance coverage | 30% (manual) | 100% (automated) | Resources checked vs total |
| Query response time | Hours/days | <2 minutes | Performance monitoring |
| Cost savings identified | — | $50K+/month | Monthly cost reports |

### Competitive Differentiation

| Feature | This Solution | Traditional Tools |
|---|---|---|
| Natural Language Queries | ✅ Yes | ❌ No (CLI/API only) |
| Multi-Cloud Unified View | ✅ AWS, Azure, GCP | ⚠️ Single cloud focus |
| Agentic AI Reasoning | ✅ Context-aware | ❌ Rule-based only |
| Policy Knowledge Graph | ✅ Context Studio | ❌ Static configs |
| Real-time Anomaly Detection | ✅ Statistical analysis | ⚠️ Threshold-based only |
| Deployment Time | ✅ 2–3 hours | ⚠️ Days/weeks |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE — Web Application                         │
│                                                                             │
│   Browser  http://localhost:5173                                            │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  React + TypeScript (Vite)                                        │    │
│   │  Cloud selector  │  Chat window  │  Markdown rendering            │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                              │                                              │
│   FastAPI Backend  http://localhost:8001                                    │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  ICAAdapter — context injection + response extraction             │    │
│   └───────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                     POST /api/v1/run/<flow-id>   x-api-key
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               ICA LANGFLOW  (langflow.servicesessentials.ibm.com)           │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  MulticloudIntelFlow  (A2A → Strands agent runtime)               │    │
│   └───────────────────────────────────────────────────────────────────┘    │
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
└────────────┼──────────────────────┼─────────────────────────────────────────┘
             │                      │
             ▼                      ▼
┌─────────────────────┐  ┌─────────────────────────────────────────────────┐
│  Context Studio     │  │         Hosted MultiCloud MCP in EC2            │
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

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Web UI** | React 18, TypeScript, Vite 5 |
| **Backend API** | Python FastAPI, uvicorn, httpx |
| **MCP Server** | Python 3.11, FastMCP 2.14 |
| **AI Orchestration** | IBM Consulting Advantage, Strands agent runtime |
| **Workflow Engine** | IBM Langflow (A2A protocol) |
| **Policy Store** | IBM Context Studio, JSON-LD knowledge graph |
| **AWS SDK** | boto3, CloudWatch, Cost Explorer |
| **Azure SDK** | azure-identity, azure-mgmt-compute, azure-mgmt-costmanagement |
| **GCP SDK** | google-cloud-compute, google-cloud-billing, google-cloud-monitoring |
| **Infrastructure** | AWS EC2 (t2.micro), systemd service |

---

## Repository Structure

```
MultiCloudInfraIntel/
├── mcp_server.py              # Main MCP server — 8 multi-cloud tools
├── requirements.txt           # MCP server Python dependencies
├── config.yaml                # Server configuration (ports, budgets, thresholds)
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── policies/                  # Governance policy files for Context Studio
│   ├── resource-policy.md
│   ├── cost-trends-policy.md
│   ├── anomaly-policy.md
│   ├── new-resource-policy.md
│   ├── idle-resource-policy.md
│   ├── compliance-policy.md
│   ├── expensive-resource-policy.md
│   └── budget-policy.md
│
├── schema/                    # JSON-LD ontology schema for Context Studio
│   └── multi-cloud-policies.jsonld
│
├── tests/                     # Unit and integration tests
│   ├── test_mcp_server.py
│   ├── test_integration.py
│   └── validate_tools.py
│
├── scripts/                   # Utility and validation scripts
│   ├── test_aws_connection.py
│   └── test_tools_simple.py
│
├── docs/                      # Extended documentation
│   ├── Architecture.md
│   ├── PROJECT_SUMMARY.md
│   ├── IMPLEMENTATION_GUIDE.md
│   └── LOCAL_TESTING.md
│
└── webapp/                    # Browser-based chat interface
    ├── README.md              # Webapp quick start guide
    ├── backend/               # Python FastAPI backend (port 8001)
    │   ├── main.py            # FastAPI app — CORS, /api/chat, /health
    │   ├── ica_adapter.py     # ICA Langflow adapter — auth + extraction
    │   ├── requirements.txt   # Backend Python dependencies
    │   └── .env.example       # Backend environment template
    └── frontend/              # React + TypeScript frontend (port 5173)
        ├── index.html         # Vite entry point
        ├── package.json       # Node dependencies
        ├── vite.config.ts     # Vite config + /api → :8001 proxy
        ├── tsconfig.json      # TypeScript strict mode config
        └── src/
            ├── main.tsx       # React 18 createRoot entry point
            ├── App.tsx        # Root component — owns all state
            ├── App.css        # Layout + component styles
            ├── index.css      # CSS reset + CSS variables
            ├── types.ts       # Shared TypeScript types
            ├── api/
            │   └── chat.ts    # axios API client + error handling
            └── components/
                ├── CloudSelector.tsx  # Provider pill buttons
                ├── ChatWindow.tsx     # Message history + Markdown
                └── ChatInput.tsx      # Auto-resize textarea + Send
```

---

## Prerequisites

**Platform access**
- IBM Consulting Advantage (ICA) account with Agentic App Studio access
- IBM Context Studio access
- ICA Langflow workflow with a configured MulticloudIntelFlow

**Cloud credentials** (one or more)
- **AWS**: IAM permissions for EC2, Cost Explorer, CloudWatch, Config
- **Azure**: Subscription with Virtual Machines, Cost Management, Monitor, Policy
- **GCP**: Project with Compute Engine, Billing, Cloud Monitoring, Asset Inventory

**Local environment**
- Python 3.11+
- Node.js 18+
- Git

> **Note**: The solution is fully multi-cloud capable. Currently tested with AWS credentials. Azure and GCP activate automatically once credentials are provided.

---

## Quick Start

The fastest path to a running system (assumes ICA and AWS are already configured):

```bash
# 1. Clone the repository
git clone https://github.com/Suvendu-IBM/MultiCloudInfraIntel.git
cd MultiCloudInfraIntel

# 2. Configure the webapp backend
cp webapp/backend/.env.example webapp/backend/.env
# Edit webapp/backend/.env — set ICA_WORKFLOW_URL and ICA_API_KEY

# 3. Start the backend (Terminal 1)
cd webapp/backend
pip install -r requirements.txt
uvicorn main:app --port 8001 --reload

# 4. Start the frontend (Terminal 2)
cd webapp/frontend
npm install
npm run dev

# 5. Open the chat interface
# → http://localhost:5173
```

Set these two variables in `webapp/backend/.env`:

| Variable | Value | Where to find it |
|---|---|---|
| `ICA_WORKFLOW_URL` | `https://langflow.servicesessentials.ibm.com/api/v1/run/<flow-id>` | Langflow UI URL bar when flow is open |
| `ICA_API_KEY` | `sk-...` | Value after `"--headers", "x-api-key"` in your MCP server config JSON |

---

## Deployment

### Phase 1 — Context Studio Setup

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

1. **resource-policy.md** — Resource discovery and filtering rules
2. **cost-trends-policy.md** — Cost analysis standards
3. **anomaly-policy.md** — Anomaly detection thresholds
4. **new-resource-policy.md** — New resource tracking rules
5. **idle-resource-policy.md** — Idle resource definitions
6. **compliance-policy.md** — Tagging, encryption, access rules
7. **expensive-resource-policy.md** — Cost threshold definitions
8. **budget-policy.md** — Budget allocation and alerting

#### Step 1.3: Import to Context Studio

1. Navigate to Context Studio in ICA
2. Click **"Start with a Schema"** → **"Create schema"** → **"Import schema"**
3. Upload `multi-cloud-policies.jsonld`
4. Name: `Multi-Cloud Policies` → Publish
5. Click **"Create a Context"** → Name: `Multi-Cloud Infrastructure Context`
6. Link the schema
7. Go to **"Source & Data"** tab → Upload all 8 policy markdown files
8. Click **"Expose as MCP"** → Copy the MCP Server URL and Bearer Token

---

### Phase 2 — MCP Server Deployment

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

# Configure AWS credentials
aws configure
# Enter: AWS Access Key ID, Secret Key, region (ap-south-1)

# Optional: Azure credentials
# az login && az account set --subscription <subscription-id>

# Optional: GCP credentials
# gcloud auth application-default login
# gcloud config set project <project-id>
```

#### Step 2.3: Run as Systemd Service

```bash
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

---

### Phase 3 — ICA Agent Configuration

#### Step 3.1: Create Agentic App

1. Navigate to ICA Agentic App Studio
2. Click **"Create an Agentic App"**
3. Name: `Multi-Cloud Intelligence App`
4. Category: `IT Operations & Cloud Management`
5. Description: `Agentic AI for multi-cloud cost, resource, and compliance intelligence`

#### Step 3.2: Add MCP Servers

**Multi-Cloud MCP (Infrastructure Data):**
- Name: `Multi-Cloud MCP`
- URL: `http://<EC2-PUBLIC-IP>:8000/sse`
- Transport: Remote (HTTP/S)

**Context Studio MCP (Policies):**
- Name: `MultiCloudIntel-Policies`
- URL: *(from Context Studio exposure)*
- Authentication: Bearer Token *(from Context Studio)*

#### Step 3.3: Create Virtual Server

1. Go to **"MCP Servers"** → **"Access MCP Gateway"**
2. Go to **"Virtual Server"** tab → **"Create Virtual Server"**
3. Name: `multi-cloud-mcp-virtual-server`
4. Select ALL tools from both MCP servers (15 total)
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

        Always include Tool Trace showing which tools were called.
      model: gpt-5.2
```

#### Step 3.5: Create Workflow

1. Go to **"Workflow"** page → **"Create New Workflow"**
2. Name: `MulticloudIntelFlow`
3. Add components: **Chat Input** → **ICA Agent** → **Chat Output**
4. Connect the components
5. Save

---

### Phase 4 — Web Application Setup

The webapp provides a browser-based chat interface that connects directly to the ICA Langflow workflow.

**Port map — no conflicts:**

| Component | Port |
|---|---|
| MCP Server (EC2) | 8000 |
| FastAPI Backend | 8001 |
| React Frontend | 5173 |

#### Step 4.1: Configure Backend Environment

```bash
cd webapp/backend
cp .env.example .env
```

Edit `webapp/backend/.env`:

```env
ICA_WORKFLOW_URL=https://langflow.servicesessentials.ibm.com/api/v1/run/<flow-id>
ICA_API_KEY=sk-<your-x-api-key-from-mcp-config>
BACKEND_PORT=8001
CORS_ORIGINS=*
```

> **Finding the values:**
> - `ICA_WORKFLOW_URL`: Open your flow in the Langflow UI — the Flow ID is in the URL bar
> - `ICA_API_KEY`: The value after `"--headers", "x-api-key"` in your MCP server configuration JSON

**Backend environment variables:**

| Variable | Required | Default | Description |
|---|---|---|---|
| `ICA_WORKFLOW_URL` | ✅ | — | Full Langflow run URL |
| `ICA_API_KEY` | ✅ | — | `x-api-key` from MCP server config |
| `BACKEND_PORT` | ❌ | `8001` | Displayed in startup log |
| `CORS_ORIGINS` | ❌ | `*` | Comma-separated allowed origins |

#### Step 4.2: Start the Backend

```bash
cd webapp/backend
pip install -r requirements.txt
uvicorn main:app --port 8001 --reload
```

Expected output:

```
INFO  PESAMultiCloudIntel Backend starting up
INFO    Port        : 8001
INFO    CORS origins: ['*']
INFO  ICAAdapter initialised successfully.
INFO  Uvicorn running on http://127.0.0.1:8001
```

#### Step 4.3: Start the Frontend

Open a new terminal:

```bash
cd webapp/frontend
npm install
npm run dev
```

Expected output:

```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

Open **http://localhost:5173** in your browser.

#### Step 4.4: Web Application Features

- **Cloud provider selector** — All Clouds, AWS, Azure, GCP with brand colour pills
  - All Clouds `#6366f1` · AWS `#f97316` · Azure `#3b82f6` · GCP `#ef4444`
- **Markdown rendering** for AI responses — tables, code blocks, headers
- **Auto-scroll** to latest message
- **Loading indicator** (three-dot animation) during agent processing
- **Enter** to send · **Shift+Enter** for new line
- **Auto-resizing** textarea (up to 6 lines)
- User-friendly error messages on network or API failure

#### Step 4.5: Backend API Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Service information and version |
| `GET` | `/health` | Health check → `{"status": "ok"}` |
| `POST` | `/api/chat` | Send question, receive AI answer |

**Request:**

```json
{
  "question": "Find idle resources",
  "cloud_provider": "aws"
}
```

Valid `cloud_provider` values: `all` · `aws` · `azure` · `gcp`

**Response:**

```json
{
  "answer": "AI generated response in markdown...",
  "cloud_provider": "aws"
}
```

**Error codes:**

| Status | Cause |
|---|---|
| 422 | Empty question or invalid `cloud_provider` |
| 502 | ICA Workflow API returned an error |
| 500 | Unexpected server error |

**Cloud context injection** — before every ICA call the adapter appends:

| Selection | Appended text |
|---|---|
| All Clouds | "Analyze across AWS, Azure and GCP." |
| AWS | "Focus on Amazon Web Services only." |
| Azure | "Focus on Microsoft Azure only." |
| GCP | "Focus on Google Cloud Platform only." |

---

## Testing

### Run via Web Application (Recommended)

Start both webapp servers (see [Phase 4](#phase-4--web-application-setup)) and open **http://localhost:5173**. Send these queries in sequence:

```
hi
List all resources
Find idle resources
Check compliance
Show cost anomalies from the last 30 days
What are the top 10 most expensive resources?
```

> **Alternative:** Open your flow in the ICA Agentic App Studio sandbox and send the same questions directly.

### Expected Results

| Query | Expected Response |
|---|---|
| `hi` | Agent introduces capabilities |
| `List all resources` | Unified resource inventory across configured clouds |
| `Find idle resources` | Idle instances with CPU utilisation metrics |
| `Check compliance` | Tagging and encryption violations with remediation steps |
| `Cost anomalies` | Anomaly table with severity, date, and contributing providers |

> Results shown are from AWS testing. With Azure/GCP credentials configured, the agent queries all three cloud providers simultaneously.

### Unit Tests

```bash
# From project root
pytest tests/ -v
pytest tests/test_mcp_server.py -v
pytest tests/test_integration.py -v
```

---

## MCP Tools Reference

| # | Tool | Description | Cloud Support |
|---|---|---|---|
| 1 | `get-resource-summary` | Unified resource inventory across clouds | AWS, Azure, GCP |
| 2 | `get-cost-trends` | Cost trends by provider and service | AWS, Azure, GCP |
| 3 | `get-cost-anomaly` | Detect statistically significant cost anomalies | AWS, Azure, GCP |
| 4 | `get-new-resources-since` | Identify resources created after a given date | AWS, Azure, GCP |
| 5 | `find-idle-resources` | Detect idle or underutilized infrastructure | AWS, Azure, GCP |
| 6 | `check-compliance` | Check tagging, encryption, public access | AWS, Azure, GCP |
| 7 | `get-top-expensive-resources` | Identify highest-cost resources | AWS, Azure, GCP |
| 8 | `get-budget-health` | Evaluate actual vs projected spend against budget | AWS, Azure, GCP |

> All tools are **multi-cloud ready**. Currently tested with AWS credentials. Enable Azure and GCP by adding their credentials — no code changes required.

---

## Context Studio Policies

| # | Policy File | Purpose |
|---|---|---|
| 1 | `resource-policy.md` | Resource discovery, filtering, and tagging rules |
| 2 | `cost-trends-policy.md` | Cost analysis standards and reporting |
| 3 | `anomaly-policy.md` | Anomaly detection thresholds (20% default) |
| 4 | `new-resource-policy.md` | New resource tracking (7-day window) |
| 5 | `idle-resource-policy.md` | Idle resource definitions (CPU <5% for 14 days) |
| 6 | `compliance-policy.md` | Mandatory tags, encryption, and access rules |
| 7 | `expensive-resource-policy.md` | Cost threshold definitions (>$500/month) |
| 8 | `budget-policy.md` | Budget allocation and alerting (80%/100% thresholds) |

---

## Performance Metrics

| Operation | Response Time |
|---|---|
| Resource listing | ~28 seconds |
| Idle detection | ~30 seconds |
| Compliance check | ~20 seconds |
| Policy retrieval | ~22 seconds |

---

## Troubleshooting

### MCP Server not accessible

```bash
# Check service status
sudo systemctl status mcp-server

# View live logs
sudo journalctl -u mcp-server -f

# Verify port is open
sudo netstat -tlnp | grep 8000
```

### ICA Gateway shows "Invalid Host header"

```bash
# Restart with correct host binding
python mcp_server.py --transport http --port 8000 --host 0.0.0.0
```

### No resources returned from cloud providers

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

### Web application — backend fails to start

| Error | Fix |
|---|---|
| `EnvironmentError: ICA_WORKFLOW_URL not set` | Copy `.env.example` to `.env` and fill in values |
| `EnvironmentError: ICA_API_KEY not set` | Set `ICA_API_KEY` in `webapp/backend/.env` |
| `Address already in use` on port 8001 | Use `--port 8002` and update `CORS_ORIGINS` |

### Web application — requests return 502

The ICA API key may have expired. Refresh it:
1. Open `langflow.servicesessentials.ibm.com` → your flow → API tab
2. Copy the new `x-api-key` value
3. Update `ICA_API_KEY` in `webapp/backend/.env`
4. Uvicorn reloads automatically (`--reload` flag)

---

## Multi-Cloud Enablement

The MCP server is fully implemented for all three providers. To activate Azure and GCP:

**Azure:**

```bash
pip install azure-cli azure-mgmt-compute azure-mgmt-monitor azure-mgmt-costmanagement
az login
az account set --subscription <subscription-id>
```

**GCP:**

```bash
pip install google-cloud-compute google-cloud-monitoring google-cloud-billing
gcloud auth application-default login
gcloud config set project <project-id>
```

**Restart the MCP server:**

```bash
sudo systemctl restart mcp-server
```

The MCP server automatically detects and queries all configured cloud providers — no code changes required.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## License

Copyright © 2026. All rights reserved.

---

## Contact

For questions or support, please refer to the project repository or contact the development team.
