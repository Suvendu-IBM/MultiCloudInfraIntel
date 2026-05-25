# Multi-Cloud Infrastructure Intelligence Architecture

## 1. Purpose

This document describes the end-to-end architecture of the Multi-Cloud Infrastructure Intelligence solution. It explains how [`ICA`](README.md), [`Context Studio`](README.md), the custom [`mcp_server.py`](mcp_server.py), cloud-provider APIs, policies, and deployment components work together to provide natural-language infrastructure intelligence across AWS, Azure, and GCP.

It replaces the incomplete architecture draft with a structured reference for solution design, implementation, deployment, and operations.

## 2. Architecture Goals

The architecture is designed to achieve the following goals:

- Provide a unified intelligence layer across AWS, Azure, and GCP
- Expose infrastructure analysis capabilities through MCP tools
- Separate runtime data retrieval from policy and governance knowledge
- Enable natural-language interactions through an ICA-hosted agent
- Support extensibility for additional policies, tools, and cloud providers
- Allow practical deployment with current AWS-first validation and multi-cloud-ready code

## 3. Solution Scope

The current repository implements a production-style MCP server in [`mcp_server.py`](mcp_server.py) and a policy knowledge base in [`policies/`](policies/). The broader solution combines:

- **User interaction layer** in ICA Playground / ICA Agentic App Studio
- **Agent orchestration layer** using an ICA agent and workflow
- **Policy knowledge layer** hosted in Context Studio
- **Operational intelligence layer** exposed through the custom MCP server
- **Cloud integration layer** for AWS, Azure, and GCP APIs
- **Configuration, testing, and documentation assets** in this repository

The implementation is already multi-cloud by design, while the currently validated path is AWS-first because the repository notes that live testing has primarily been done with AWS credentials.

## 4. High-Level Architecture

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              User / Analyst                                 │
│                    Natural-language questions in ICA                        │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                   ICA Agentic App Studio / Playground                       │
│                                                                              │
│  Multi-Cloud Infrastructure Analyst Agent                                    │
│  - interprets user intent                                                    │
│  - retrieves policy context                                                  │
│  - invokes MCP tools                                                         │
│  - synthesizes findings and recommendations                                  │
└──────────────────────────────────────────────────────────────────────────────┘
                         │                                  │
                         ▼                                  ▼
┌───────────────────────────────────┐     ┌───────────────────────────────────┐
│ Context Studio MCP Exposure       │     │ Multi-Cloud MCP Server            │
│                                   │     │ [`mcp_server.py`](mcp_server.py)  │
│ - JSON-LD schema                  │     │ - 8 operational tools             │
│ - policy markdown documents       │     │ - provider clients                │
│ - semantic / graph retrieval      │     │ - normalization logic             │
│ - governance thresholds           │     │ - compliance and cost analysis    │
└───────────────────────────────────┘     └───────────────────────────────────┘
                                                          │
                                                          ▼
                            ┌────────────────────────────────────────────────┐
                            │ Cloud Provider APIs                            │
                            │ - AWS                                          │
                            │ - Azure                                        │
                            │ - GCP                                          │
                            └────────────────────────────────────────────────┘
```

## 5. Major Components

### 5.1 ICA User and Agent Layer

The user interacts with the solution through ICA. The agent is configured in ICA Agentic App Studio and acts as the reasoning layer between user intent, policy retrieval, and operational tool execution.

Responsibilities:

- Accept natural-language prompts such as cost, compliance, inventory, and optimization questions
- Decide when policy context is required before operational analysis
- Invoke policy MCP tools and infrastructure MCP tools in the correct sequence
- Generate concise findings, root-cause explanations, and recommended actions
- Present a unified answer instead of raw API responses

This layer is described in [`README.md`](README.md) and summarized in [`docs/PROJECT_SUMMARY.md`](docs/PROJECT_SUMMARY.md).

### 5.2 Context Studio Policy Layer

Context Studio stores governance and operating policies as structured knowledge. The repository contains the source policy content under [`policies/`](policies/) and the JSON-LD schema in [`schema/policies.jsonld`](schema/policies.jsonld).

Responsibilities:

- Store policy definitions for cost trends, anomalies, compliance, budgets, and idle resources
- Provide retrievable business and governance context to the ICA agent
- Maintain semantic consistency through the JSON-LD schema
- Support vector, graph, or hybrid policy lookups before runtime analysis

Key repository assets:

- [`policies/resource-policy.md`](policies/resource-policy.md)
- [`policies/cost-trends-policy.md`](policies/cost-trends-policy.md)
- [`policies/anomaly-policy.md`](policies/anomaly-policy.md)
- [`policies/new-resource-policy.md`](policies/new-resource-policy.md)
- [`policies/idle-resource-policy.md`](policies/idle-resource-policy.md)
- [`policies/compliance-policy.md`](policies/compliance-policy.md)
- [`policies/expensive-resource-policy.md`](policies/expensive-resource-policy.md)
- [`policies/budget-policy.md`](policies/budget-policy.md)
- [`schema/policies.jsonld`](schema/policies.jsonld)

### 5.3 Multi-Cloud MCP Server Layer

The custom MCP server is implemented in [`mcp_server.py`](mcp_server.py). It is the operational core of the solution and exposes the infrastructure intelligence tools consumed by the ICA agent.

Responsibilities:

- Host MCP endpoints over HTTP/SSE
- Connect to supported cloud providers
- Normalize provider-specific resource and cost data into a common shape
- Execute inventory, trend, anomaly, compliance, idle-resource, and budget analyses
- Return structured results for agent consumption

This layer is configuration-driven through [`config.yaml`](config.yaml) and environment variables.

### 5.4 Cloud Provider Integration Layer

The MCP server integrates with three cloud ecosystems:

- **AWS** using [`boto3`](mcp_server.py:43)
- **Azure** using Azure management SDKs such as [`DefaultAzureCredential`](mcp_server.py:51) and related clients
- **GCP** using Google Cloud Python clients such as [`compute_v1`](mcp_server.py:62)

Responsibilities:

- Authenticate to cloud accounts
- Fetch runtime resource metadata
- Query usage, billing, monitoring, and governance sources
- Return provider-specific details to server-side normalization logic

### 5.5 Configuration Layer

Configuration is managed by the [`Config`](mcp_server.py:194) class in [`mcp_server.py`](mcp_server.py). Default values are loaded from [`config.yaml`](config.yaml) when available, with environment-variable fallback for secrets and provider settings.

Configuration areas include:

- Server port, timeout, logging, cache TTL
- Enabled cloud providers and regions
- Azure and GCP credential references
- Budget defaults and alert thresholds
- Compliance policy defaults
- Monitoring thresholds for idle detection and anomaly detection

### 5.6 Documentation and Testing Layer

The repository also contains operational and validation assets that support the architecture:

- [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md)
- [`docs/LOCAL_TESTING.md`](docs/LOCAL_TESTING.md)
- [`docs/PROJECT_SUMMARY.md`](docs/PROJECT_SUMMARY.md)
- [`tests/test_mcp_server.py`](tests/test_mcp_server.py)
- [`tests/test_integration.py`](tests/test_integration.py)
- [`tests/validate_tools.py`](tests/validate_tools.py)
- [`scripts/test_aws_connection.py`](scripts/test_aws_connection.py)
- [`scripts/test_tools_simple.py`](scripts/test_tools_simple.py)

## 6. Runtime Interaction Model

### 6.1 End-to-End Request Flow

A typical request follows this sequence:

1. User asks a natural-language question in ICA.
2. ICA agent interprets the intent.
3. Agent retrieves relevant policy context from Context Studio.
4. Agent invokes one or more MCP tools from the custom server.
5. MCP server authenticates to relevant cloud providers.
6. Cloud-provider data is collected and normalized.
7. Tool results are returned to the agent.
8. Agent combines operational evidence with policy context.
9. Final answer is generated with findings, rationale, and recommendations.

### 6.2 Logical Sequence Diagram

```text
User
  │
  │ "Find idle resources across all clouds"
  ▼
ICA Agent
  │
  ├── query Context Studio MCP for idle-resource policy
  │
  ├── invoke MCP tool: find-idle-resources
  │
  ▼
Multi-Cloud MCP Server
  │
  ├── query AWS / Azure / GCP monitoring and inventory APIs
  ├── apply configured thresholds
  ├── normalize and rank idle candidates
  │
  ▼
ICA Agent
  │
  ├── combine policy + runtime evidence
  └── present savings estimate and remediation options
  ▼
User
```

## 7. MCP Tool Architecture

The solution exposes 8 operational tools through the custom MCP server. These are the primary runtime interfaces used by the ICA agent.

| Tool | Purpose | Typical Output |
|------|---------|----------------|
| `get-resource-summary` | Unified inventory across clouds | Resource counts, breakdowns, normalized resource list |
| `get-cost-trends` | Historical spend analysis | Time-series cost by provider/service |
| `get-cost-anomaly` | Cost spike detection | Anomalous services, dates, deviations |
| `get-new-resources-since` | Change tracking | Recently created resources |
| `find-idle-resources` | Waste detection | Underutilized resources and savings estimates |
| `check-compliance` | Governance validation | Violations, severities, remediation guidance |
| `get-top-expensive-resources` | Cost hotspot analysis | High-cost resources ranked by spend |
| `get-budget-health` | Budget status and forecast | Budget consumed, projected spend, recommendations |

These tool definitions are referenced in [`README.md`](README.md) and implemented in [`mcp_server.py`](mcp_server.py).

## 8. Policy Architecture

The policy layer is intentionally separated from the operational tool layer.

### 8.1 Why Policies Are Externalized

Separating policies from code provides:

- Easier updates to thresholds and governance logic
- Reusable knowledge for multiple workflows
- Better explainability because answers can cite policy intent
- Lower operational risk than embedding every rule in code
- A path to non-developer policy maintenance in Context Studio

### 8.2 Policy Categories in This Repository

The repository contains policy documents for:

- Resource discovery and filtering
- Cost trend analysis
- Cost anomaly thresholds
- New resource tracking windows
- Idle resource thresholds
- Compliance rules for tags, encryption, and access
- Expensive resource thresholds
- Budget alert thresholds

### 8.3 Policy-to-Tool Mapping

| Policy Document | Primary Runtime Tool(s) |
|----------------|-------------------------|
| [`policies/resource-policy.md`](policies/resource-policy.md) | `get-resource-summary` |
| [`policies/cost-trends-policy.md`](policies/cost-trends-policy.md) | `get-cost-trends` |
| [`policies/anomaly-policy.md`](policies/anomaly-policy.md) | `get-cost-anomaly` |
| [`policies/new-resource-policy.md`](policies/new-resource-policy.md) | `get-new-resources-since` |
| [`policies/idle-resource-policy.md`](policies/idle-resource-policy.md) | `find-idle-resources` |
| [`policies/compliance-policy.md`](policies/compliance-policy.md) | `check-compliance` |
| [`policies/expensive-resource-policy.md`](policies/expensive-resource-policy.md) | `get-top-expensive-resources` |
| [`policies/budget-policy.md`](policies/budget-policy.md) | `get-budget-health` |

## 9. Data Architecture

### 9.1 Core Data Normalization

The MCP server normalizes provider-specific data into shared Python data structures. The visible examples include:

- [`ResourceSummary`](mcp_server.py:100)
- [`CostTrend`](mcp_server.py:125)
- [`ComplianceViolation`](mcp_server.py:144)
- [`BudgetHealth`](mcp_server.py:165)

This normalization is critical because AWS, Azure, and GCP each return different payload structures, terminology, and service taxonomies.

### 9.2 Normalized Data Characteristics

Normalized objects typically standardize:

- resource identifiers
- provider names
- service or resource type
- region or location
- lifecycle state
- creation timestamps
- tags or labels
- recommendations and severity metadata

### 9.3 Control and Knowledge Data

In addition to operational data, the architecture manages:

- policy content in markdown
- JSON-LD schema definitions
- configuration values in [`config.yaml`](config.yaml)
- environment-based credentials
- logs and runtime diagnostics

## 10. Deployment Architecture

### 10.1 Current Deployment Model

The documented deployment model hosts the custom MCP server on an AWS EC2 instance while ICA and Context Studio remain managed platform components.

```text
┌───────────────────────────┐
│ ICA / Context Studio      │
│ Managed IBM platform      │
└─────────────┬─────────────┘
              │
              │ MCP over HTTP/SSE
              ▼
┌───────────────────────────┐
│ AWS EC2 Instance          │
│ Multi-Cloud MCP Server    │
│ Python + FastMCP          │
└─────────────┬─────────────┘
              │
              ├──────────────► AWS APIs
              ├──────────────► Azure APIs
              └──────────────► GCP APIs
```

### 10.2 Runtime Hosting Responsibilities

The EC2-hosted MCP runtime is responsible for:

- running the Python process
- exposing the MCP endpoint
- holding cloud SDK dependencies
- managing credential access
- logging runtime activity
- handling tool execution requests

### 10.3 Service Management

The implementation guide documents a systemd-based service model for the MCP server in [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md). That design supports:

- automatic restart on failure
- boot-time startup
- standard Linux service observability
- compatibility with lightweight single-instance deployments

### 10.4 Alternative Future Hosting

The broader roadmap in project documents suggests later movement toward more production-ready managed hosting options. This may include:

- IBM Cloud Code Engine
- container-based deployment
- stronger isolation for secrets and traffic management
- scalable stateless replicas behind a load balancer

## 11. Security Architecture

### 11.1 Security Principles

The solution should operate with the following architectural principles:

- least-privilege access to cloud-provider APIs
- separation of secrets from source code
- externalized policy management
- auditable operational logs
- constrained public exposure of the MCP endpoint
- environment-specific configuration

### 11.2 Credential Handling

The repository architecture shows that credentials are expected through provider-native methods and environment variables rather than being hardcoded in source:

- AWS credentials via local AWS configuration / IAM role
- Azure values from environment variables such as [`AZURE_SUBSCRIPTION_ID`](mcp_server.py:229)
- GCP values from environment variables such as [`GCP_PROJECT_ID`](mcp_server.py:236)

### 11.3 Recommended Security Controls

For production use, the architecture should include:

- IAM role-based access for the EC2 host
- HTTPS termination in front of MCP endpoints
- network restrictions for inbound access
- secret storage outside plaintext files
- audit logging and retention controls
- controlled bearer-token handling for Context Studio connections

## 12. Scalability and Performance Architecture

### 12.1 Performance Characteristics

The project documents currently report approximate operational timings in [`README.md`](README.md) and [`docs/PROJECT_SUMMARY.md`](docs/PROJECT_SUMMARY.md):

- resource listing around 78 seconds
- idle detection around 30 seconds
- compliance checks around 267 milliseconds
- policy retrieval around 22 seconds

These values reflect current implementation behavior and should be treated as practical benchmarks, not guaranteed SLAs.

### 12.2 Scalability Considerations

The architecture is designed to scale functionally before it scales operationally:

- new tools can be added to the MCP server
- new policies can be added to Context Studio
- more cloud accounts can be onboarded through credentials and config
- providers can be queried independently and aggregated centrally

Operational scaling opportunities include:

- parallel provider queries
- asynchronous tool execution
- response caching
- stateless horizontal scaling of the MCP server
- splitting high-latency cost-analysis workflows from lighter inventory queries

### 12.3 Bottlenecks to Watch

Potential bottlenecks include:

- cloud API rate limits
- latency of cost and monitoring APIs
- serialized provider calls
- large account inventories
- token/context overhead in agent responses

## 13. Resilience and Error Handling

### 13.1 Error Domains

The architecture must handle failures across multiple layers:

- cloud authentication failures
- cloud API throttling or timeouts
- partial provider availability
- policy retrieval failures
- invalid tool parameters
- MCP transport issues
- agent orchestration failures

### 13.2 Resilience Strategy

A resilient implementation should aim for:

- partial results when one provider fails
- retriable handling of transient provider errors
- clear validation errors for bad input
- logging of tool execution failures
- fallbacks when policy retrieval is unavailable
- bounded request timeouts and safe defaults

The source already includes timeout, monitoring, and configuration constructs in [`Config`](mcp_server.py:194), which support this direction.

## 14. Observability Architecture

### 14.1 Logging

The MCP server initializes Python logging using [`logging.basicConfig()`](mcp_server.py:71). At minimum, the architecture supports:

- application log emission
- error tracking
- startup/runtime diagnostics
- operational inspection through service logs when hosted on Linux

### 14.2 Recommended Telemetry

A production-quality observability design should include:

- request-level tool invocation logs
- tool latency metrics
- cloud-provider error counts
- cache hit/miss visibility
- authentication failure monitoring
- infrastructure host metrics
- user query tracing across policy and tool calls

### 14.3 Tool Trace Visibility

The ICA agent design in [`README.md`](README.md) emphasizes showing a tool trace to the user. Architecturally, this improves:

- explainability
- debugging
- auditability
- trust in AI-generated infrastructure findings

## 15. Example Workflows

### 15.1 Cost Spike Investigation

1. User asks why cloud cost increased.
2. Agent retrieves anomaly policy from Context Studio.
3. Agent invokes `get-cost-anomaly`.
4. Agent may invoke `get-new-resources-since` and `get-top-expensive-resources`.
5. MCP server correlates cost changes with recent infrastructure changes.
6. Agent returns root cause and remediation suggestions.

### 15.2 Idle Resource Optimization

1. User asks for cost-saving opportunities.
2. Agent retrieves idle-resource policy.
3. Agent invokes `find-idle-resources`.
4. Optional follow-up calls check budget or ownership context.
5. Agent returns prioritized savings opportunities.

### 15.3 Compliance Review

1. User asks for compliance posture.
2. Agent retrieves compliance policy.
3. Agent invokes `check-compliance`.
4. MCP server evaluates tags, encryption, and exposure conditions.
5. Agent summarizes violations by severity and remediation path.

## 16. Repository-to-Architecture Mapping

| Repository Asset | Architectural Role |
|------------------|--------------------|
| [`mcp_server.py`](mcp_server.py) | Core MCP runtime, tool host, provider integration, normalization |
| [`config.yaml`](config.yaml) | Runtime defaults and operational configuration |
| [`policies/`](policies/) | Business and governance knowledge base |
| [`schema/policies.jsonld`](schema/policies.jsonld) | Structured schema for policy semantics |
| [`README.md`](README.md) | Solution overview, setup, tool inventory, deployment narrative |
| [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) | Deployment and integration steps |
| [`docs/PROJECT_SUMMARY.md`](docs/PROJECT_SUMMARY.md) | Executive summary and value framing |
| [`tests/`](tests/) | Validation of MCP behavior and integrations |
| [`scripts/`](scripts/) | Local testing and cloud connectivity support |

## 17. Current State and Gaps

### 17.1 What Is Already Implemented

The repository clearly provides:

- a substantial custom MCP server implementation
- multi-cloud-aware SDK integrations
- configuration defaults for AWS, Azure, and GCP
- policy files for major use cases
- implementation and local testing guides
- tests and helper scripts
- ICA/Context Studio integration guidance

### 17.2 What Remains Environment-Dependent

Some architecture elements are designed but depend on deployment configuration rather than code alone:

- live Azure credential setup
- live GCP credential setup
- ICA-side agent and workflow provisioning
- Context Studio publication and MCP exposure
- production-grade ingress, TLS, and secret management
- runtime scaling beyond a single host

## 18. Architectural Strengths

This solution’s architecture is strong in the following ways:

- **Clear separation of concerns** between policy knowledge and runtime cloud analysis
- **Provider abstraction** through normalized tool outputs
- **Practical implementation path** with current AWS-first deployment guidance
- **Extensibility** for new tools, policies, and cloud providers
- **AI-friendly integration** through MCP and ICA orchestration
- **Governance-aware design** by retrieving business rules before analysis

## 19. Recommended Next Architecture Improvements

To make the architecture more production-ready, the next improvements should be:

1. Add HTTPS and authenticated ingress in front of the MCP server
2. Introduce structured telemetry and request correlation IDs
3. Implement stronger caching for repeated cost and inventory queries
4. Parallelize provider-specific fetches where safe
5. Containerize the MCP runtime for easier deployment portability
6. Add explicit architecture diagrams for security and network topology
7. Expand testing for Azure and GCP live integrations
8. Formalize SLOs for high-latency operations

## 20. Conclusion

The Multi-Cloud Infrastructure Intelligence architecture combines an ICA-hosted reasoning agent, a Context Studio policy knowledge layer, and a custom operational MCP server to deliver unified cloud intelligence across AWS, Azure, and GCP.

The repository’s strongest architectural pattern is the separation between **policy retrieval** and **runtime infrastructure analysis**. That design enables explainable, governable, and extensible natural-language operations for cost optimization, compliance monitoring, inventory visibility, and infrastructure investigation.

---
**Document Version:** 2.0  
**Last Updated:** May 2026  
**Status:** Updated and completed  
**Classification:** Internal Use
