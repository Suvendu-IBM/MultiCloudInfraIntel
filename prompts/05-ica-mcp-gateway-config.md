# Prompt: ICA MCP Gateway Configuration

## Context
This prompt was used to create the configuration guide for integrating the MCP server with ICA (Intelligent Cloud Assistant) through the MCP Gateway, enabling AI agents to access the 8 tools via SSE transport.

## Original Prompt to Bob

Bob, create a comprehensive configuration guide for connecting the Multi-Cloud MCP Server to ICA through the MCP Gateway using SSE transport. Include server configuration, gateway setup, and tool registration.

## Configuration Requirements

### MCP Server Configuration

**Server Settings:**
- **Transport:** SSE (Server-Sent Events)
- **Port:** 8000
- **Protocol:** HTTP/HTTPS
- **Endpoint:** `/sse`
- **Health Check:** `/health`
- **Authentication:** API key or OAuth2

### ICA MCP Gateway Setup

**Gateway Components:**
1. **MCP Gateway Service** - Routes requests to MCP servers
2. **Tool Registry** - Registers available tools
3. **Authentication Layer** - Secures access
4. **Load Balancer** - Distributes requests
5. **Monitoring** - Tracks usage and performance

### Tool Registration

**8 Tools to Register:**
1. `get_resource_summary` - Resource inventory
2. `get_cost_trends` - Cost trend analysis
3. `get_cost_anomaly` - Anomaly detection
4. `get_new_resources_since` - New resource tracking
5. `find_idle_resources` - Idle resource detection
6. `check_compliance` - Compliance validation
7. `get_top_expensive_resources` - Expensive resource ranking
8. `get_budget_health` - Budget monitoring

## Technical Requirements

- **MCP Protocol:** 1.0+
- **Transport:** SSE (Server-Sent Events)
- **Authentication:** API key or OAuth2
- **TLS/SSL:** Required for production
- **Health Checks:** Every 30 seconds
- **Timeout:** 30 seconds per request
- **Retry Logic:** 3 attempts with exponential backoff

## Configuration Files

### 1. MCP Server Config (`config.yaml`)

```yaml
server:
  port: 8000
  transport: sse
  endpoint: /sse
  health_check: /health
  log_level: INFO
  cache_ttl: 3600

authentication:
  type: api_key
  header: X-API-Key
  
clouds:
  aws:
    enabled: true
    default_region: ap-south-1
  azure:
    enabled: true
  gcp:
    enabled: true

monitoring:
  idle_cpu_threshold: 5
  idle_lookback_days: 14
  cost_anomaly_threshold: 20
  cost_anomaly_lookback: 30
```

### 2. ICA Gateway Config (`gateway.yaml`)

```yaml
gateway:
  name: multi-cloud-intelligence
  version: 1.0.0
  
mcp_servers:
  - name: multi-cloud-mcp
    url: http://localhost:8000/sse
    transport: sse
    health_check: http://localhost:8000/health
    timeout: 30
    retry_attempts: 3
    
tools:
  - name: get_resource_summary
    server: multi-cloud-mcp
    description: Get unified resource inventory
    
  - name: get_cost_trends
    server: multi-cloud-mcp
    description: Analyze cost trends
    
  - name: get_cost_anomaly
    server: multi-cloud-mcp
    description: Detect cost anomalies
    
  - name: get_new_resources_since
    server: multi-cloud-mcp
    description: Track new resources
    
  - name: find_idle_resources
    server: multi-cloud-mcp
    description: Find idle resources
    
  - name: check_compliance
    server: multi-cloud-mcp
    description: Check compliance
    
  - name: get_top_expensive_resources
    server: multi-cloud-mcp
    description: Get expensive resources
    
  - name: get_budget_health
    server: multi-cloud-mcp
    description: Monitor budget health

authentication:
  type: api_key
  validation_endpoint: /auth/validate
```

## Setup Steps

### Step 1: Start MCP Server

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AZURE_SUBSCRIPTION_ID=your_subscription
export GCP_PROJECT_ID=your_project

# Start server
python mcp_server.py --config config.yaml
```

### Step 2: Configure ICA Gateway

```bash
# Install ICA Gateway
npm install -g @ica/gateway

# Configure gateway
ica-gateway config set gateway.yaml

# Start gateway
ica-gateway start
```

### Step 3: Register Tools

```bash
# Register all 8 tools
ica-gateway register-tools gateway.yaml

# Verify registration
ica-gateway list-tools
```

### Step 4: Test Connection

```bash
# Test health check
curl http://localhost:8000/health

# Test tool invocation
ica-gateway test-tool get_resource_summary
```

## Validation Checklist

- [ ] MCP server running on port 8000
- [ ] SSE endpoint accessible at `/sse`
- [ ] Health check responding at `/health`
- [ ] ICA Gateway configured
- [ ] All 8 tools registered
- [ ] Authentication working
- [ ] Cloud credentials configured
- [ ] Test tool invocations successful
- [ ] Error handling working
- [ ] Logging enabled
- [ ] Monitoring active

## SSE Transport Details

**Why SSE?**
- Real-time streaming of results
- Long-running operations support
- Progress updates during execution
- Compatible with ICA architecture
- Firewall-friendly (HTTP-based)

**SSE Message Format:**
```
event: tool_start
data: {"tool": "get_resource_summary", "request_id": "123"}

event: tool_progress
data: {"progress": 50, "message": "Scanning AWS resources"}

event: tool_result
data: {"result": {...}, "status": "success"}

event: tool_end
data: {"request_id": "123", "duration_ms": 1234}
```

## Security Considerations

1. **API Key Management**
   - Rotate keys every 90 days
   - Use environment variables
   - Never commit keys to git

2. **TLS/SSL**
   - Required for production
   - Use valid certificates
   - Enforce HTTPS

3. **Cloud Credentials**
   - Use IAM roles when possible
   - Least privilege principle
   - Audit access regularly

4. **Network Security**
   - Firewall rules
   - VPC/VNet isolation
   - Private endpoints

## Monitoring and Logging

**Metrics to Track:**
- Tool invocation count
- Response times
- Error rates
- Cache hit rates
- Cloud API calls
- Cost per request

**Logging:**
- Request/response logs
- Error logs
- Audit logs
- Performance logs

## Troubleshooting

**Common Issues:**

1. **Connection Refused**
   - Check server is running
   - Verify port 8000 is open
   - Check firewall rules

2. **Authentication Failed**
   - Verify API key
   - Check authentication config
   - Review gateway logs

3. **Tool Not Found**
   - Verify tool registration
   - Check gateway config
   - Restart gateway

4. **Timeout Errors**
   - Increase timeout setting
   - Check cloud API latency
   - Review server logs

## Result

Bob successfully created a comprehensive ICA MCP Gateway configuration guide with:
- ✅ Complete server configuration
- ✅ Gateway setup instructions
- ✅ Tool registration process
- ✅ SSE transport configuration
- ✅ Security best practices
- ✅ Monitoring and logging setup
- ✅ Troubleshooting guide

**Guide Created:** ICA MCP Gateway configuration documentation

## Key Features

- **Production-Ready:** Enterprise-grade configuration
- **Secure:** Authentication and TLS/SSL
- **Scalable:** Load balancing and caching
- **Monitored:** Comprehensive logging and metrics
- **Reliable:** Health checks and retry logic

## Integration Architecture

```
┌─────────────────┐
│   ICA Agent     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP Gateway    │
│  (Port 8080)    │
└────────┬────────┘
         │ SSE
         ▼
┌─────────────────┐
│  MCP Server     │
│  (Port 8000)    │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
  ┌───┐    ┌────┐   ┌────┐   ┌────┐
  │AWS│    │Azure│  │GCP │   │Cache│
  └───┘    └────┘   └────┘   └────┘
```

---

**Prompt Date:** 2026-05-19  
**Bob Version:** Advanced Mode  
**Outcome:** ✅ Success - Complete ICA MCP Gateway configuration