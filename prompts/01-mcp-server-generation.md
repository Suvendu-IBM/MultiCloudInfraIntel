# Prompt: Generate Multi-Cloud MCP Server with 8 Tools

## Context
This prompt was used to generate the initial MCP server implementation for the MultiCloudInfraIntel project - a production-grade solution for multi-cloud infrastructure intelligence and cost management.

## Original Prompt to Bob

Bob, generate a production-grade MCP server in Python using FastMCP for multi-cloud infrastructure intelligence.

## 8 Tools Required

1. **get_resource_summary** - unified resource inventory across AWS/Azure/GCP
   - Returns aggregated resource counts by provider, type, region
   - Supports filtering by tags, regions, and resource states
   - Groups resources by environment and cost center

2. **get_cost_trends** - analyze cost trends with daily/monthly granularity
   - Tracks spending patterns over time
   - Supports multiple time periods (daily, weekly, monthly)
   - Identifies cost increase/decrease trends

3. **get_cost_anomaly** - detect cost spikes using rolling 7-day average (threshold: 20%)
   - Uses statistical analysis to detect anomalies
   - Configurable threshold (default: 20% above baseline)
   - 7-day rolling average for baseline calculation

4. **get_new_resources_since** - track resources created after a specific date
   - Monitors new resource creation
   - Supports date-based filtering
   - Validates against compliance policies

5. **find_idle_resources** - identify underutilized resources (CPU <5% for 14 days)
   - Detects idle compute resources
   - CPU threshold: <5% average
   - Lookback period: 14 days
   - Supports cost optimization initiatives

6. **check_compliance** - validate tagging, encryption, public access rules
   - Enforces mandatory tags: owner, cost-center, environment
   - Validates encryption requirements
   - Checks public access configurations
   - Generates compliance violation reports

7. **get_top_expensive_resources** - rank resources by estimated monthly cost
   - Identifies top cost drivers
   - Configurable limit (default: 10 resources)
   - Supports cost optimization planning

8. **get_budget_health** - monitor spending against budgets with projections
   - Tracks budget utilization
   - Warning threshold: 80%
   - Critical threshold: 100%
   - Provides spending projections

## Technical Requirements

- **Language:** Python 3.11+
- **Framework:** FastMCP (MCP SDK)
- **Architecture:** Async/await pattern for all API calls
- **Caching:** 1-hour TTL for API responses
- **Retry Logic:** Exponential backoff for failed API calls
- **Cloud SDKs:**
  - AWS: boto3
  - Azure: azure-identity, azure-mgmt-*
  - GCP: google-cloud-compute, google-cloud-monitoring
- **Transport:** SSE (Server-Sent Events) for ICA compatibility
- **Health Check:** Built-in health check endpoint
- **Configuration:** YAML-based config file support

## Expected Output

A complete, production-ready `mcp_server.py` file with:
- All 8 tools implemented
- Multi-cloud SDK integrations
- Error handling and retry logic
- Caching layer
- Logging and monitoring
- Configuration management
- Health check endpoint

## Result

Bob successfully generated a 2000+ line production-grade MCP server with:
- ✅ All 8 tools fully implemented
- ✅ AWS, Azure, GCP integrations
- ✅ Async/await architecture
- ✅ Caching with TTL
- ✅ Exponential backoff retry
- ✅ SSE transport support
- ✅ Comprehensive error handling
- ✅ YAML configuration support

**File Generated:** `mcp_server.py` (2000+ lines)

---

**Prompt Date:** 2026-05-18  
**Bob Version:** Advanced Mode  
**Outcome:** ✅ Success - Production-ready MCP server