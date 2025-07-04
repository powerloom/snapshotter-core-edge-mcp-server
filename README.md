# Snapshotter MCP Server

This is the MCP (Multi-Chain Protocol) server for the Snapshotter Core project.

## Setup

> [!NOTE]
> Use a virtual environment preferably to install dependencies.

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd snapshotter-mcp-server
    ```

2.  **Install dependencies using Poetry:**

    If you don't have Poetry installed, follow the instructions [here](https://python-poetry.org/docs/#installation).

    ```bash
    poetry install
    ```

## Running the Application

To start the server, use Uvicorn:

```bash
poetry run python -m main
```

## Running the Application with Gemini CLI

> [!NOTE]
> Activate the virtual environment before running `gemini` CLI.

```
gemini
```

Run the following command to start the server:

```
/mcp

ℹ Configured MCP servers:
 
  🟢 SnapshotterMCP - Ready (21 tools)
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

Run any natural language query on the prompt to begin with.
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

## Running Tests

To run the tests, use Pytest:

```bash
poetry run pytest
```
