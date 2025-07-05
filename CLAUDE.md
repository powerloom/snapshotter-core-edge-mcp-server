# Powerloom Snapshotter Core Edge MCP Server - Codebase Analysis

## Overview

The Powerloom Snapshotter Core Edge MCP Server is a Model Context Protocol (MCP) server that provides natural language access to Powerloom's blockchain data API, specifically for Uniswap V3 pools and trading data.

## Architecture

### Technology Stack
- **Language**: Python 3.10+
- **Framework**: FastMCP (MCP framework built on FastAPI)
- **HTTP Client**: httpx for async API calls
- **Data Validation**: Pydantic for model validation
- **Testing**: pytest with pytest-asyncio
- **Package Management**: Poetry

### Project Structure
```
snapshotter-core-edge-mcp-server/
├── README.md               # Documentation and usage instructions
├── pyproject.toml         # Poetry configuration and dependencies
├── poetry.lock            # Locked dependencies
├── main.py               # Main server implementation with MCP tools
├── mcp_models.py         # Pydantic models for API responses
├── test_api_endpoints.py # Test suite for all endpoints
└── openapi.json          # OpenAPI specification (generated)
```

### Key Components

1. **MCP Server Implementation (`main.py`)**
   - Implements 21 MCP tools wrapping Snapshotter Core API endpoints
   - Dual-function pattern: private HTTP function + public MCP tool
   - Default API URL: `https://bds-api.powerloom.io`

2. **Data Models (`mcp_models.py`)**
   - Comprehensive Pydantic models for all API responses
   - Models for tokens, pools, trades, epochs, and snapshots
   - Strong typing and validation throughout

3. **Available MCP Tools** (21 total)
   - Pool & token metadata queries
   - Trading data and volume aggregation
   - Price tracking and time series
   - Active tokens/pools monitoring
   - System health and epoch information

## Code Quality Analysis

### Strengths ⭐⭐⭐⭐⭐
- Excellent documentation with comprehensive docstrings
- Strong type safety using Pydantic models
- Consistent implementation patterns across all endpoints
- Full test coverage for all API endpoints
- Clean separation of concerns

### Areas for Improvement ⭐⭐⭐

1. **Critical Bug**: Logic error in `_get_token_price_pool` function
   - Doesn't handle case where only `block_number` is provided
   - Validation logic needs fixing

2. **Performance Issues**:
   - No connection pooling (creates new httpx client per request)
   - No caching for frequently accessed data
   - Missing timeout configurations

3. **Error Handling**:
   - Basic error handling with `raise_for_status()`
   - No custom error messages or recovery strategies
   - Missing context for API failures

4. **Security Considerations**:
   - No authentication mechanism
   - No rate limiting protection
   - Basic URL construction without extra validation

## Recommendations

### High Priority
1. **Fix the validation bug** in `_get_token_price_pool`:
   ```python
   # Current logic misses the case where only block_number is provided
   if not pool_address and not block_number:
       raise ValueError("Either pool_address or block_number must be provided.")
   ```

2. **Implement connection pooling**:
   ```python
   # Create a shared client instance
   async with httpx.AsyncClient() as client:
       # Reuse for all requests
   ```

3. **Add retry logic** for network resilience

### Medium Priority
1. Add caching layer for immutable data (pool metadata, historical data)
2. Implement structured logging for debugging
3. Add timeout configurations for HTTP requests
4. Improve error messages with context

### Low Priority
1. Add API key support if available
2. Implement rate limiting
3. Use Pydantic Settings for configuration management
4. Add metrics/monitoring capabilities

## Usage Instructions

### Running the Server

The server now supports multiple transport modes:

#### STDIO Transport (Default)
For use with Claude Desktop or other MCP clients:
```bash
# Install dependencies
poetry install --no-root

# Start the server
poetry run python -m main
```

#### HTTP Transport
To run as a web server accessible over the network:
```bash
poetry run python -m main --transport http --port 8052
```

#### SSE Transport
For Server-Sent Events compatibility:
```bash
poetry run python -m main --transport sse --port 8052
```

#### Command Line Options
- `--transport`: Transport mode (`stdio`, `http`, or `sse`). Default: `stdio`
- `--host`: Host to bind to when using HTTP/SSE transport. Default: `127.0.0.1`
- `--port`: Port to bind to when using HTTP/SSE transport. Default: `8000`

### Adding to Claude Desktop
Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "powerloom-snapshotter": {
      "command": "/path/to/python",
      "args": ["-m", "main"],
      "cwd": "/path/to/snapshotter-core-edge-mcp-server"
    }
  }
}
```

### Using with HTTP Transport
When running in HTTP mode, you can connect to the server programmatically:

```python
from fastmcp import Client

async with Client("http://localhost:8052/mcp/") as client:
    result = await client.call_tool("get_pool_metadata", {
        "pool_address": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
    })
```

### Using with Gemini CLI

Gemini CLI can connect to MCP servers via STDIO transport. Configure it in `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "powerloom": {
      "command": "poetry",
      "args": ["run", "python", "-m", "main"],
      "cwd": "/path/to/snapshotter-core-edge-mcp-server"
    }
  }
}
```

Or use the full Python path:

```json
{
  "mcpServers": {
    "powerloom": {
      "command": "/path/to/.pyenv/versions/mcp/bin/python",
      "args": ["-m", "main"],
      "cwd": "/path/to/snapshotter-core-edge-mcp-server"
    }
  }
}
```

Then in Gemini CLI:
```
> /mcp

ℹ Configured MCP servers:
 
  🟢 powerloom - Ready (21 tools)
  
> get pool metadata for 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640

> show me the most active tokens today
```

## Use Cases

This MCP server enables:
- Natural language queries for blockchain data
- AI-powered DeFi analytics and monitoring
- Automated trading analysis
- Research on Uniswap V3 pools
- Integration with AI assistants for blockchain insights

## Architecture Insights

The codebase implements a clean adapter pattern that:
- Wraps REST API into MCP tools
- Provides strong typing for blockchain/DeFi data
- Focuses on Uniswap V3 liquidity analytics
- Uses epoch-based data organization for consistency
- Integrates with IPFS for decentralized storage

### Transport Modes (NEW)

The server now supports three transport modes:

1. **STDIO Transport**
   - Default mode for Claude Desktop integration
   - Communication via standard input/output
   - Best for local development and desktop applications

2. **HTTP Transport**
   - RESTful API server mode
   - Enables network access and remote connections
   - Ideal for web applications and microservices
   - Accessible at `http://host:port/mcp/`

3. **SSE Transport**
   - Server-Sent Events for real-time communication
   - Legacy support for older MCP clients
   - Useful for streaming data scenarios

### Recent Updates

- **2025-07-05**: Added multi-transport support (STDIO, HTTP, SSE)
- **2025-07-05**: Fixed command-line argument parsing
- **2025-07-05**: Updated documentation for all transport modes

---
*Last analyzed: 2025-07-05*