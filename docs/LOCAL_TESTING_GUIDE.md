# Local Testing Guide for Multi-Cloud Infrastructure Intelligence MCP Server

## Overview
This guide helps you test the MCP server locally before deploying it to production or hosting it remotely.

## Prerequisites ✓
- [x] Python 3.11+ installed (You have Python 3.13.9)
- [x] All dependencies installed (fastmcp, boto3, azure, google-cloud packages)
- [x] AWS credentials configured (Account: 041129025979, User: infraintel)

## Testing Workflow

### 1. Quick Connection Test (COMPLETED ✓)
```bash
python test_aws_connection.py
```

**Results:**
- ✓ AWS Authentication: Working
- ✓ EC2 Access: Working (17 regions available)
- ✓ S3 Access: Working (0 buckets)
- ⚠ Cost Explorer: Needs to be enabled in AWS Console
- ⚠ CloudWatch: Minor API parameter issue (non-critical)
- ✓ MCP Server Import: Working

### 2. Test Individual MCP Tools

Create a test script to call individual tools:

```python
# test_tools.py
import asyncio
from mcp_server import MultiCloudIntelligenceServer

async def test_tools():
    server = MultiCloudIntelligenceServer()
    
    # Test 1: Get Resource Summary
    print("\n=== Testing get_resource_summary ===")
    result = await server.get_resource_summary(cloud_provider="aws")
    print(f"Found {len(result)} resources")
    
    # Test 2: Get Cost Trends (last 7 days)
    print("\n=== Testing get_cost_trends ===")
    from datetime import datetime, timedelta
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    try:
        result = await server.get_cost_trends(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        print(f"Retrieved cost data: {len(result)} data points")
    except Exception as e:
        print(f"Cost trends test: {e}")
    
    # Test 3: Check Compliance
    print("\n=== Testing check_compliance ===")
    result = await server.check_compliance(rule_type="tagging")
    print(f"Compliance check complete: {len(result)} violations found")

if __name__ == "__main__":
    asyncio.run(test_tools())
```

Run it:
```bash
python test_tools.py
```

### 3. Run MCP Server Locally (stdio mode)

**Option A: Direct Python Execution**
```bash
python mcp_server.py --transport stdio
```

This starts the server in stdio mode, which is perfect for:
- Testing with Claude Desktop locally
- Debugging tool responses
- Validating JSON-RPC communication

**Option B: HTTP Mode (for web testing)**
```bash
python mcp_server.py --transport http --port 8000
```

Then test with curl:
```bash
# Health check
curl http://localhost:8000/health

# Test a tool (example)
curl -X POST http://localhost:8000/tools/get_resource_summary \
  -H "Content-Type: application/json" \
  -d '{"cloud_provider": "aws"}'
```

### 4. Run Existing Test Suite

```bash
# Run all unit tests
pytest tests/test_mcp_server.py -v

# Run integration tests (requires cloud credentials)
pytest tests/test_integration.py -v -m integration

# Run with coverage report
pytest tests/ --cov=mcp_server --cov-report=html

# Validate all tools
python tests/validate_tools.py
```

### 5. Interactive Testing with Python REPL

```python
# Start Python REPL
python

# Import and test
import asyncio
from mcp_server import MultiCloudIntelligenceServer

server = MultiCloudIntelligenceServer()

# Test AWS authentication
print(server.aws_auth.is_authenticated())

# Test getting resources
result = asyncio.run(server.get_resource_summary(cloud_provider="aws"))
print(f"Resources found: {len(result)}")
```

## Common Testing Scenarios

### Scenario 1: Test with Mock Data (No Cloud Access)
```python
# Create a test with mocked AWS responses
import pytest
from unittest.mock import Mock, patch

@patch('boto3.client')
def test_with_mock(mock_boto):
    # Mock EC2 client
    mock_ec2 = Mock()
    mock_ec2.describe_instances.return_value = {
        'Reservations': []
    }
    mock_boto.return_value = mock_ec2
    
    # Test your code
    server = MultiCloudIntelligenceServer()
    result = asyncio.run(server.get_resource_summary())
    assert isinstance(result, list)
```

### Scenario 2: Test Specific AWS Region
```python
# Test resources in a specific region
result = await server.get_resource_summary(
    cloud_provider="aws",
    region="us-east-1"
)
```

### Scenario 3: Test Error Handling
```python
# Test with invalid parameters
try:
    result = await server.get_cost_trends(
        start_date="invalid-date",
        end_date="2024-01-01"
    )
except Exception as e:
    print(f"Expected error: {e}")
```

## Debugging Tips

### Enable Debug Logging
```bash
python mcp_server.py --log-level DEBUG
```

### Check Logs
```bash
# View recent logs
cat logs/mcp_server.log

# Follow logs in real-time
tail -f logs/mcp_server.log
```

### Inspect Cache
```python
from mcp_server import CacheManager

cache = CacheManager()
print(f"Cache entries: {len(cache.cache)}")
print(f"Cache keys: {list(cache.cache.keys())}")
```

## Performance Testing

### Test Response Times
```python
import time
import asyncio
from mcp_server import MultiCloudIntelligenceServer

async def benchmark():
    server = MultiCloudIntelligenceServer()
    
    start = time.time()
    result = await server.get_resource_summary()
    elapsed = time.time() - start
    
    print(f"Response time: {elapsed:.2f}s")
    print(f"Resources: {len(result)}")

asyncio.run(benchmark())
```

### Test Cache Performance
```python
# First call (no cache)
start = time.time()
result1 = await server.get_resource_summary()
time1 = time.time() - start

# Second call (cached)
start = time.time()
result2 = await server.get_resource_summary()
time2 = time.time() - start

print(f"First call: {time1:.2f}s")
print(f"Cached call: {time2:.2f}s")
print(f"Speedup: {time1/time2:.1f}x")
```

## Known Issues & Workarounds

### Issue 1: Cost Explorer Access Denied
**Problem:** `AccessDeniedException` when calling Cost Explorer API

**Solution:**
1. Go to AWS Console → Billing → Cost Explorer
2. Click "Enable Cost Explorer"
3. Wait 24 hours for data to populate
4. Ensure IAM user has `ce:GetCostAndUsage` permission

**Workaround for testing:**
```python
# Skip cost tests if not enabled
try:
    result = await server.get_cost_trends(...)
except Exception as e:
    if "AccessDeniedException" in str(e):
        print("Cost Explorer not enabled, skipping...")
```

### Issue 2: No Resources Found
**Problem:** Empty results when testing

**Possible causes:**
- No resources in the specified region
- IAM permissions insufficient
- Wrong cloud provider selected

**Debug:**
```python
# Check authentication
print(f"AWS Auth: {server.aws_auth.is_authenticated()}")

# Try different region
result = await server.get_resource_summary(region="us-west-2")

# Check IAM permissions
import boto3
sts = boto3.client('sts')
print(sts.get_caller_identity())
```

## Testing Checklist

Before deploying to production:

- [ ] All dependencies installed
- [ ] AWS credentials working
- [ ] At least one tool tested successfully
- [ ] Error handling verified
- [ ] Cache working correctly
- [ ] Logs being written
- [ ] Configuration file valid
- [ ] Unit tests passing
- [ ] Integration tests passing (if applicable)
- [ ] Performance acceptable (<5s response time)

## Next Steps After Local Testing

1. **Configure for Production**
   - Review and update `config.yaml`
   - Set appropriate cache TTL
   - Configure budget thresholds
   - Set compliance rules

2. **Security Hardening**
   - Use IAM roles instead of access keys
   - Enable MFA on AWS account
   - Rotate credentials regularly
   - Review IAM permissions (least privilege)

3. **Deployment Options**
   - Docker container
   - Kubernetes deployment
   - AWS Lambda (serverless)
   - EC2 instance
   - Cloud Run (GCP)

4. **Monitoring Setup**
   - CloudWatch metrics
   - Application logs
   - Error tracking
   - Performance monitoring

## Quick Reference Commands

```bash
# Test AWS connection
python test_aws_connection.py

# Run MCP server (stdio)
python mcp_server.py --transport stdio

# Run MCP server (HTTP)
python mcp_server.py --transport http --port 8000

# Run tests
pytest tests/ -v

# Check health
curl http://localhost:8000/health

# View logs
tail -f logs/mcp_server.log

# Check Python version
python --version

# List installed packages
pip list | grep -E "fastmcp|boto3|azure|google"
```

## Support

If you encounter issues:
1. Check the logs in `logs/mcp_server.log`
2. Review AWS IAM permissions
3. Verify credentials with `aws sts get-caller-identity`
4. Test individual components with Python REPL
5. Check the README.md for detailed documentation

## Summary

Your current status:
- ✓ Environment ready
- ✓ AWS authenticated
- ✓ Dependencies installed
- ✓ MCP server importable
- ⚠ Cost Explorer needs enabling (optional)
- Ready for local testing!

**Recommended next step:** Run the MCP server in stdio mode and test with a simple tool call.