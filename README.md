# Powerloom Snapshotter Core Edge MCP Server

A Model Context Protocol (MCP) server that provides natural language access to Powerloom's blockchain data API, specifically for Uniswap V3 pools and trading data.

## Overview

This MCP server acts as a bridge between AI assistants (like Claude) and the Powerloom Snapshotter Core API, enabling natural language queries for blockchain analytics, DeFi data, and Uniswap V3 liquidity pool information.

## Features

- 🔧 **21 MCP Tools** for comprehensive blockchain data access
- 🌐 **Multiple Transport Modes**: STDIO, HTTP, and SSE
- 📊 **Real-time & Historical Data**: Access current and past blockchain states
- 🔍 **Pool Analytics**: Detailed Uniswap V3 pool metadata and trading data
- 💰 **Price Tracking**: Token prices across pools with time series support
- 📈 **Volume Aggregation**: Trading volume analytics and aggregations
- 🏛️ **IPFS Integration**: Access to finalized data stored on IPFS

## Available Tools

### Pool & Token Information
- `get_pool_metadata` - Get metadata for a specific pool
- `get_token_pools` - Get all pools containing a specific token
- `get_token_base_snapshots` - Get base snapshots for a token across all pools

### Price Data
- `get_ethprice` - Get ETH price data
- `get_token_price_pool` - Get token price in a specific pool
- `get_token_price_all` - Get token prices across all pools
- `get_token_price_series` - Get time series of token prices

### Trading Data
- `get_trades_snapshot` - Get trades for a specific pool
- `get_all_trades_snapshot` - Get trades across all pools
- `get_pool_trades` - Get detailed trade data over time range
- `get_trade_volume_agg` - Get aggregated trade volume
- `get_trade_volume_agg_all_pools` - Get trade volume across all pools

### Analytics & Monitoring
- `get_daily_active_tokens` - Get tokens with recent trading activity
- `get_daily_active_pools` - Get pools with recent trading activity
- `get_base_snapshot` - Get comprehensive pool snapshot data

### System & Epoch Tools
- `health_check` - Check API health status
- `get_current_epoch_data` - Get current epoch information
- `get_epoch_info` - Get specific epoch details
- `get_project_last_finalized_epoch_info` - Get last finalized epoch
- `get_data_for_project_id_epoch_id` - Get project data for epoch
- `get_finalized_cid_for_project_id_epoch_id` - Get IPFS CID

## Setup

> [!NOTE]
> Use a virtual environment preferably to install dependencies.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/powerloom/snapshotter-core-edge-mcp-server.git
    cd snapshotter-core-edge-mcp-server
    ```

2. **Install dependencies using Poetry:**

    If you don't have Poetry installed, follow the instructions [here](https://python-poetry.org/docs/#installation).

    ```bash
    poetry install --no-root
    ```

## Running the Application

The server supports multiple transport modes:

### STDIO Transport (Default)
For use with Claude Desktop or other MCP clients:

```bash
poetry run python -m main
```

### HTTP Transport
To run as an HTTP server:

```bash
poetry run python -m main --transport http --port 8052
```

Access the server at: `http://localhost:8052/mcp/`

### SSE Transport (Server-Sent Events)
For compatibility with SSE clients:

```bash
poetry run python -m main --transport sse --port 8052
```

### Command Line Options
- `--transport`: Transport mode (`stdio`, `http`, or `sse`). Default: `stdio`
- `--host`: Host to bind to when using HTTP/SSE transport. Default: `127.0.0.1`
- `--port`: Port to bind to when using HTTP/SSE transport. Default: `8000`

## Integration with Claude Desktop

Add to your Claude Desktop configuration (`~/.claude/settings.json`):

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

## Programmatic Usage (HTTP Mode)

When running in HTTP mode, you can connect programmatically:

```python
from fastmcp import Client
import asyncio

async def main():
    async with Client("http://localhost:8052/mcp/") as client:
        # Get pool metadata
        result = await client.call_tool("get_pool_metadata", {
            "pool_address": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
        })
        print(result)
        
        # Get token prices
        prices = await client.call_tool("get_token_price_all", {
            "token_address": "0x6982508145454ce325ddbe47a25d4ec3d2311933"
        })
        print(prices)

asyncio.run(main())
```

## Example Usage with Natural Language

### Using with Gemini CLI

1. **Configure Gemini CLI** to use the MCP server by adding to `~/.gemini/settings.json`:

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

   Or if you prefer using the full Python path:

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

2. **Start Gemini CLI**:

   ```bash
   gemini
   ```

3. **Check MCP server status**:

   ```
   > /mcp

   ℹ Configured MCP servers:
    
     🟢 powerloom - Ready (21 tools)
       - get_pool_metadata
       - get_token_pools
       - get_ethprice
       - get_token_price_pool
       - get_token_base_snapshots
       - get_base_snapshot
       - get_trades_snapshot
       - get_all_trades_snapshot
       - get_token_price_all
       - get_trade_volume_agg_all_pools
       - get_trade_volume_agg
       - get_pool_trades
       - get_token_price_series
       - get_daily_active_tokens
       - get_daily_active_pools
       - health_check
       - get_current_epoch_data
       - get_epoch_info
       - get_project_last_finalized_epoch_info
       - get_data_for_project_id_epoch_id
       - get_finalized_cid_for_project_id_epoch_id
   ```

4. **Run natural language queries**:

   ```
   > get token prices across all pools for PEPE token 0x6982508145454ce325ddbe47a25d4ec3d2311933

   > show me the most active trading pools in the last 24 hours

   > get trading volume for USDC-ETH pool over the last week

   > check the health status of the Powerloom API

   > get detailed trade history for pool 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640
   ```

### Example Session

Here's a complete example session showing the MCP server in action:

```
> get token prices across all pools for token 0x6982508145454ce325ddbe47a25d4ec3d2311933

 ╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  get_token_price_all (SnapshotterMCP MCP Server) {"token_address":"0x6982508145454ce325ddbe47a25d4ec3d2311933"}                         │
 │                                                                                                                                           │
 │    {                                                                                                                                      │
 │      "0x11950d141EcB863F01007AdD7D1A342041227b58": 9.804585475736871e-6,                                                                  │
 │      "0xF239009A101B6B930A527DEaaB6961b6E7deC8a6": 9.721573281781315e-6                                                                   │
 │    }                                                                                                                                      │
 ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ The token prices for 0x6982508145454ce325ddbe47a25d4ec3d2311933 across all pools are:
   - 0x11950d141EcB863F01007AdD7D1A342041227b58: 9.804585475736871e-6
   - 0xF239009A101B6B930A527DEaaB6961b6E7deC8a6: 9.721573281781315e-6

> show pool information for each of the pools reported above

 ╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  get_pool_metadata (SnapshotterMCP MCP Server) {"pool_address":"0x11950d141EcB863F01007AdD7D1A342041227b58"}                            │
✦ Here is the pool information for the requested addresses:


  Pool Address: 0x11950d141EcB863F01007AdD7D1A342041227b58
   - Token0:
       - Address: 0x6982508145454Ce325dDbE47a25d4ec3d2311933
       - Name: Pepe
       - Symbol: PEPE
       - Decimals: 18
   - Token1:
       - Address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
       - Name: Wrapped Ether
       - Symbol: WETH
       - Decimals: 18
   - Fee: 3000
   - Factory: 0x1F98431c8aD98523631AE4a59f267346ea31F984


  Pool Address: 0xF239009A101B6B930A527DEaaB6961b6E7deC8a6
   - Token0:
       - Address: 0x6982508145454Ce325dDbE47a25d4ec3d2311933
       - Name: Pepe
       - Symbol: PEPE
       - Decimals: 18
   - Token1:
       - Address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
       - Name: Wrapped Ether
       - Symbol: WETH
       - Decimals: 18
   - Fee: 10000
   - Factory: 0x1F98431c8aD98523631AE4a59f267346ea31F984
```

### Gemini CLI Features

- **Natural Language Interface**: Ask questions in plain English
- **Multiple Tool Support**: If multiple MCP servers expose tools with the same name, they'll be prefixed (e.g., `powerloom__get_pool_metadata`)
- **Auto-completion**: Gemini CLI provides suggestions as you type
- **Tool Confirmation**: For safety, Gemini CLI asks for confirmation before executing tools (can be disabled with `trust: true` in config)

## Running Tests

To run the tests, use Pytest:

```bash
poetry run pytest
```

## Environment Variables

- `SNAPSHOTTER_CORE_API_URL`: Override the default API URL (default: `https://bds-api.powerloom.io`)

## Architecture

The server implements a clean adapter pattern:
- Wraps Powerloom's REST API into MCP tools
- Provides strong typing with Pydantic models
- Focuses on Uniswap V3 liquidity analytics
- Uses epoch-based data organization
- Integrates with IPFS for decentralized storage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Join the Powerloom Discord community
- Check the documentation at [powerloom.io](https://powerloom.io)