# Multi-Cloud Infrastructure Intelligence MCP Server

Production-grade enterprise MCP server for multi-cloud infrastructure intelligence supporting AWS, Azure, and GCP with real API integrations.

## Features

- **8 Production-Grade Tools** for infrastructure intelligence and cost management
- **Multi-Cloud Support**: AWS, Azure, and GCP with unified API
- **Real API Integrations**: Direct integration with cloud provider APIs
- **Intelligent Caching**: 1-hour TTL cache to reduce API calls
- **Graceful Degradation**: Works with partial cloud credentials
- **Comprehensive Error Handling**: Exponential backoff and retry logic
- **Type-Safe**: Full type hints throughout
- **Production-Ready**: Structured logging, configuration management, health checks

## Requirements

- Python 3.11 or higher
- Cloud provider credentials (at least one of AWS, Azure, or GCP)
- FastMCP framework

## Installation

### 1. Clone or Download

```bash
cd MultiCloudInfraIntel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Cloud Credentials

#### AWS

**Option 1: AWS CLI (Recommended)**
```bash
aws configure
```

**Option 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

#### Azure

**Option 1: Azure CLI (Recommended)**
```bash
az login
```

**Option 2: Environment Variables**
```bash
export AZURE_SUBSCRIPTION_ID=your_subscription_id
export AZURE_TENANT_ID=your_tenant_id
export AZURE_CLIENT_ID=your_client_id
export AZURE_CLIENT_SECRET=your_client_secret
```

#### GCP

**Option 1: Application Default Credentials (Recommended)**
```bash
gcloud auth application-default login
```

**Option 2: Service Account Key**
```bash
export GCP_PROJECT_ID=your_project_id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 4. Configure Server

Edit `config.yaml` to customize:
- Budget thresholds per team
- Compliance rules (mandatory tags)
- Monitoring thresholds
- Cache TTL

### 5. Run the Server

**For HTTP transport (ICA/web connections):**
```bash
python mcp_server.py --transport http --port 8000
```

**For stdio transport (local Claude Desktop):**
```bash
python mcp_server.py --transport stdio
```

**With custom configuration:**
```bash
python mcp_server.py --config custom-config.yaml --log-level DEBUG
```

## The 8 Tools

### 1. get_resource_summary

Get a unified view of all resources across connected clouds.

**Parameters:**
- `cloud_provider` (optional): Filter by provider (aws, azure, gcp)
- `region` (optional): Filter by region
- `resource_type` (optional): Filter by type (ec2, vm, instance)

**Example:**
```python
{
  "cloud_provider": "aws",
  "region": "us-east-1",
  "resource_type": "ec2"
}
```

### 2. get_cost_trends

Analyze cost trends across all clouds with daily or monthly granularity.

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `granularity` (optional): DAILY or MONTHLY (default: DAILY)

**Example:**
```python
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "granularity": "DAILY"
}
```

### 3. get_cost_anomaly

Detect cost spikes using rolling 7-day average analysis.

**Parameters:**
- `threshold_percent` (optional): Percentage above average to flag (default: 20%)
- `lookback_days` (optional): Days to analyze (default: 30)

**Example:**
```python
{
  "threshold_percent": 20,
  "lookback_days": 30
}
```

### 4. get_new_resources_since

Track resources created after a specific date.

**Parameters:**
- `cutoff_date` (required): Date in YYYY-MM-DD format

**Example:**
```python
{
  "cutoff_date": "2024-01-01"
}
```

### 5. find_idle_resources

Identify underutilized resources based on CPU metrics.

**Parameters:**
- `cpu_threshold_percent` (optional): CPU threshold (default: 5%)
- `days_lookback` (optional): Days to analyze (default: 14)

**Example:**
```python
{
  "cpu_threshold_percent": 5,
  "days_lookback": 14
}
```

### 6. check_compliance

Validate resources against compliance rules.

**Parameters:**
- `rule_type` (required): encryption | tagging | public_access
- `tag_key` (optional): Specific tag to check (for tagging rule)

**Example:**
```python
{
  "rule_type": "tagging",
  "tag_key": "owner"
}
```

**Compliance Rules:**
- **encryption**: Checks EBS volumes, Azure disks, GCP persistent disks
- **tagging**: Validates mandatory tags (owner, cost-center, environment)
- **public_access**: Detects publicly accessible S3 buckets, Azure storage, GCP buckets

### 7. get_top_expensive_resources

Rank resources by estimated monthly cost.

**Parameters:**
- `limit` (optional): Number of resources to return (default: 10)
- `start_date` (optional): Start date for cost calculation
- `end_date` (optional): End date for cost calculation

**Example:**
```python
{
  "limit": 10
}
```

### 8. get_budget_health

Monitor spending against budgets with projections.

**Parameters:**
- `team_name` (optional): Team name to check budget for
- `budget_amount` (optional): Override budget amount

**Example:**
```python
{
  "team_name": "engineering",
  "budget_amount": 5000
}
```

**Status Values:**
- `on_track`: Projected spend < 80% of budget
- `at_risk`: Projected spend 80-100% of budget
- `over`: Projected spend > 100% of budget

## Health Check

Check server and cloud connection status:

```bash
curl http://localhost:8000/health
```

## Configuration

### config.yaml Structure

```yaml
server:
  port: 8000
  log_level: INFO
  cache_ttl: 3600

clouds:
  aws:
    default_region: us-east-1
    enabled: true
  azure:
    enabled: true
  gcp:
    enabled: true

budgets:
  default: 1000
  teams:
    engineering: 5000
    data_science: 3000

compliance:
  mandatory_tags:
    - owner
    - cost-center
    - environment
  encryption_required: true
  public_access_allowed: false

monitoring:
  idle_cpu_threshold: 5
  idle_lookback_days: 14
  cost_anomaly_threshold: 20
  cost_anomaly_lookback: 30
```

## Testing

### Run Unit Tests

```bash
pytest tests/test_mcp_server.py -v
```

### Run Integration Tests

```bash
pytest tests/test_integration.py -v
```

### Validate All Tools

```bash
python tests/validate_tools.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastMCP Server                           │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ AWS Auth     │  │ Azure Auth   │  │ GCP Auth     │     │
│  │ Manager      │  │ Manager      │  │ Manager      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Cache Layer (1-hour TTL)                   │  │
│  └──────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Resource     │  │ Cost         │  │ Compliance   │     │
│  │ Tools        │  │ Tools        │  │ Tools        │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
    ┌────────┐        ┌────────┐        ┌────────┐
    │  AWS   │        │ Azure  │        │  GCP   │
    │  APIs  │        │  APIs  │        │  APIs  │
    └────────┘        └────────┘        └────────┘
```

## Error Handling

The server implements comprehensive error handling:

- **Exponential Backoff**: Automatic retry with 1s, 2s, 4s, 8s, 16s delays
- **Rate Limiting Detection**: Detects 429/throttling errors
- **Timeout Protection**: 30-second timeout per API call
- **Graceful Degradation**: Missing cloud credentials return empty results with warnings

## Performance

- **Caching**: 1-hour TTL reduces redundant API calls
- **Async Operations**: All API calls use async/await pattern
- **Parallel Execution**: Multi-cloud queries run concurrently
- **Efficient Filtering**: Client-side filtering reduces data transfer

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use IAM roles** when running on cloud instances
3. **Rotate credentials** regularly
4. **Use least-privilege** access policies
5. **Enable MFA** on cloud accounts
6. **Monitor API usage** for anomalies

## Troubleshooting

### No resources returned

- Check cloud credentials are configured correctly
- Verify the cloud provider is enabled in config.yaml
- Check logs for authentication errors

### Cost data not available

- AWS: Ensure Cost Explorer API is enabled
- Azure: Verify Cost Management permissions
- GCP: Check Cloud Billing API is enabled

### High API costs

- Increase cache TTL in config.yaml
- Reduce polling frequency
- Use resource filters to limit scope

## Development

### Code Style

```bash
black mcp_server.py
flake8 mcp_server.py
mypy mcp_server.py
```

### Adding New Tools

1. Add method to `MultiCloudIntelligenceServer` class
2. Register tool with `@mcp.tool()` decorator
3. Add tests to `tests/test_mcp_server.py`
4. Update documentation

## License

Copyright © 2024. All rights reserved.

## Support

For issues, questions, or contributions, please refer to the project repository.

## Version History

- **1.0.0** (2024-01-20): Initial production release
  - 8 core tools implemented
  - Multi-cloud support (AWS, Azure, GCP)
  - Caching and error handling
  - Comprehensive documentation