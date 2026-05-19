# Local Testing Guide

## Prerequisites

- Python 3.11+
- AWS credentials configured
- Git

## Quick Start

```bash
# Clone repository
git clone https://github.com/Suvendu-IBM/MultiCloudInfraIntel.git
cd MultiCloudInfraIntel

# Setup virtual environment
python3 -m venv mcp-env
source mcp-env/bin/activate  # Linux/Mac
# or mcp-env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure AWS
aws configure

# Run server
python mcp_server.py --transport http --port 8000
```

## Testing the MCP Server

### Test 1: SSE Connection

```bash
curl -N http://localhost:8000/sse
```

Expected Output:

```
event: endpoint
data: /messages/?session_id=xxx...
```

### Test 2: List Tools

```bash
# Get session ID from SSE output, then:
curl -X POST "http://localhost:8000/messages/?session_id=YOUR_SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```

Expected Output: 8 tools listed.

### Test 3: Get Resources

```bash
curl -X POST "http://localhost:8000/messages/?session_id=YOUR_SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get-resource-summary","arguments":{}},"id":2}'
```

## Testing with Python Script

```python
# test_mcp.py
import requests
import json

BASE_URL = "http://localhost:8000"

# Get session ID
response = requests.get(f"{BASE_URL}/sse", stream=True)
session_id = None
for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if 'session_id=' in line_str:
            session_id = line_str.split('session_id=')[1]
            print(f"Session ID: {session_id}")
            break

if session_id:
    # List tools
    resp = requests.post(
        f"{BASE_URL}/messages/?session_id={session_id}",
        json={"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}
    )
    tools = resp.json().get('result', {}).get('tools', [])
    print(f"Found {len(tools)} tools")
    for tool in tools:
        print(f"  - {tool.get('name')}")
```

## Testing All 8 Tools

```python
# test_all_tools.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def get_session_id():
    response = requests.get(f"{BASE_URL}/sse", stream=True)
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if 'session_id=' in line_str:
                return line_str.split('session_id=')[1]
    return None

def call_tool(session_id, tool_name, args):
    resp = requests.post(
        f"{BASE_URL}/messages/?session_id={session_id}",
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": tool_name, "arguments": args}, "id": 1}
    )
    return resp.json()

session_id = get_session_id()
print(f"Session: {session_id}")

# Test get-resource-summary
result = call_tool(session_id, "get-resource-summary", {})
print("Resources:", json.dumps(result, indent=2)[:500])

# Test get-cost-trends
result = call_tool(session_id, "get-cost-trends", {"start_date": "2026-04-01", "end_date": "2026-05-01"})
print("Cost Trends:", json.dumps(result, indent=2)[:500])
```

## Expected Results

| Tool | Expected Output |
|------|-----------------|
| get-resource-summary | List of EC2 instances |
| get-cost-trends | Daily cost data |
| get-cost-anomaly | Detected spikes |
| get-new-resources-since | Resources after cutoff |
| find-idle-resources | Idle instances with CPU |
| check-compliance | Violations |
| get-top-expensive-resources | Top 10 by cost |
| get-budget-health | Budget status |

## Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| AWS auth error | `aws configure` |
| Port in use | Change port: `--port 8001` |