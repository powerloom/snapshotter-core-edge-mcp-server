# server.py
import os
import httpx
from fastmcp import FastMCP
from typing import Optional
from mcp_models import (
    PoolMetadata,
    GetTokenPoolsResponse,
    GetEthPriceResponse,
    GetTokenBaseSnapshotsResponse,
    GetBaseSnapshotResponse,
    GetTradesSnapshotResponse,
    GetAllTradesSnapshotResponse,
    GetTokenPriceAllResponse,
    GetTradeVolumeAggResponse,
    GetPoolTradesResponse,
    GetTokenPriceSeriesResponse,
    GetDailyActiveTokensResponse,
    GetDailyActivePoolsResponse,
    HealthCheckResponse,
    GetCurrentEpochDataResponse,
    GetEpochInfoResponse,
    GetProjectLastFinalizedEpochInfoResponse,
    GetDataForProjectIdEpochIdResponse,
    GetFinalizedCidForProjectIdEpochIdResponse,
)

SNAPSHOTTER_CORE_API_URL = os.getenv(
    "SNAPSHOTTER_CORE_API_URL", "https://bds-api.powerloom.io"
)

mcp = FastMCP("SnapshotterMCP")


async def _get_pool_metadata(pool_address: str) -> PoolMetadata:
    """Get the metadata for a specific pool."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SNAPSHOTTER_CORE_API_URL}/pool/{pool_address}/metadata"
        )
        response.raise_for_status()
        data = response.json()
        return PoolMetadata.model_validate(data)

@mcp.tool
async def get_pool_metadata(pool_address: str) -> PoolMetadata:
    """Get the metadata for a specific pool including token information, fees, and factory address.
    
    Args:
        pool_address: The contract address of the liquidity pool
        
    Returns:
        PoolMetadata: Structured metadata about the pool including tokens, fees, and factory info
    """
    return await _get_pool_metadata(pool_address)

async def _get_token_pools(token_address: str) -> GetTokenPoolsResponse:
    """Get the token pools for a specific token."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/token/{token_address}/pools")
        response.raise_for_status()
        data = response.json()
        return GetTokenPoolsResponse.model_validate(data)

@mcp.tool
async def get_token_pools(token_address: str) -> GetTokenPoolsResponse:
    """Get all liquidity pools that contain a specific token.
    
    Args:
        token_address: The contract address of the token
        
    Returns:
        GetTokenPoolsResponse: Dictionary mapping pool addresses to their metadata
    """
    return await _get_token_pools(token_address)


async def _get_ethprice(block_number: Optional[int] = None) -> GetEthPriceResponse:
    """Get ETH price snapshot for a specific block number or latest finalized epoch."""
    async with httpx.AsyncClient() as client:
        if block_number is None:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/ethPrice")
        else:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/ethPrice/{block_number}")
        response.raise_for_status()
        data = response.json()
        return GetEthPriceResponse.model_validate(data)

@mcp.tool
async def get_ethprice(block_number: Optional[int] = None) -> GetEthPriceResponse:
    """Get ETH price data for a specific block number or latest finalized epoch.
    
    Args:
        block_number: Optional block number. If not provided, returns latest finalized epoch data
        
    Returns:
        GetEthPriceResponse: Structured ETH price data with epoch information and historical snapshots
    """
    return await _get_ethprice(block_number)

async def _get_token_price_pool(token_address: str, pool_address: Optional[str] = None, block_number: Optional[int] = None) -> float:
    """Get token price for a specific pool and block number."""
    async with httpx.AsyncClient() as client:
        if pool_address and block_number:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/token/price/{token_address}/{pool_address}/{block_number}")
        elif pool_address:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/token/price/{token_address}/{pool_address}")
        else:
            raise ValueError("Either pool_address or block_number must be provided.")
        response.raise_for_status()
        return response.json()

@mcp.tool
async def get_token_price_pool(token_address: str, pool_address: Optional[str] = None, block_number: Optional[int] = None) -> float:
    """Get token price for a specific pool and block number.
    
    Args:
        token_address: The contract address of the token
        pool_address: Optional pool address
        block_number: Optional block number
        
    Returns:
        float: Token price in the specified pool at the given block
    """
    return await _get_token_price_pool(token_address, pool_address, block_number)

async def _get_token_base_snapshots(token_address: str) -> GetTokenBaseSnapshotsResponse:
    """Get token base snapshots for a specific token."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/base_all_pools/{token_address}")
        response.raise_for_status()
        data = response.json()
        return GetTokenBaseSnapshotsResponse.model_validate(data)

@mcp.tool
async def get_token_base_snapshots(token_address: str) -> GetTokenBaseSnapshotsResponse:
    """Get base snapshots for a token across all pools.
    
    Args:
        token_address: The contract address of the token
        
    Returns:
        GetTokenBaseSnapshotsResponse: Complex nested snapshot data across multiple pools
    """
    return await _get_token_base_snapshots(token_address)

async def _get_base_snapshot(pool_address: str, block_number: Optional[int] = None) -> GetBaseSnapshotResponse:
    """Get base snapshot for a specific pool and block number."""
    async with httpx.AsyncClient() as client:
        if block_number:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/base/{pool_address}/{block_number}")
        else:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/base/{pool_address}")
        response.raise_for_status()
        data = response.json()
        return GetBaseSnapshotResponse.model_validate(data)

@mcp.tool
async def get_base_snapshot(pool_address: str, block_number: Optional[int] = None) -> GetBaseSnapshotResponse:
    """Get comprehensive base snapshot data for a specific pool.
    
    Args:
        pool_address: The contract address of the pool
        block_number: Optional block number. If not provided, returns latest data
        
    Returns:
        GetBaseSnapshotResponse: Detailed pool snapshot including reserves, prices, volumes, and fees
    """
    return await _get_base_snapshot(pool_address, block_number)

async def _get_trades_snapshot(pool_address: str, block_number: Optional[int] = None) -> GetTradesSnapshotResponse:
    """Get trades snapshot for a specific pool and block number."""
    async with httpx.AsyncClient() as client:
        if block_number:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/trades/{pool_address}/{block_number}")
        else:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/trades/{pool_address}")
        response.raise_for_status()
        data = response.json()
        return GetTradesSnapshotResponse.model_validate(data)

@mcp.tool
async def get_trades_snapshot(pool_address: str, block_number: Optional[int] = None) -> GetTradesSnapshotResponse:
    """Get all trades that occurred in a pool during a specific epoch.
    
    Args:
        pool_address: The contract address of the pool
        block_number: Optional block number. If not provided, returns latest epoch data
        
    Returns:
        GetTradesSnapshotResponse: All trades with detailed transaction information and historical snapshots
    """
    return await _get_trades_snapshot(pool_address, block_number)

async def _get_all_trades_snapshot(block_number: Optional[int] = None) -> GetAllTradesSnapshotResponse:
    """Get all trades snapshot for a specific block number."""
    async with httpx.AsyncClient() as client:
        if block_number:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/allTrades/{block_number}")
        else:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/snapshot/allTrades")
        response.raise_for_status()
        data = response.json()
        return GetAllTradesSnapshotResponse.model_validate(data)

@mcp.tool
async def get_all_trades_snapshot(block_number: Optional[int] = None) -> GetAllTradesSnapshotResponse:
    """Get trades snapshot data across all pools.
    
    Args:
        block_number: Optional block number. If not provided, returns latest epoch data
        
    Returns:
        GetAllTradesSnapshotResponse: Comprehensive view of trading activity across all pools
    """
    return await _get_all_trades_snapshot(block_number)

async def _get_token_price_all(token_address: str, block_number: Optional[int] = None) -> GetTokenPriceAllResponse:
    """Get all token prices for a specific token and block number."""
    async with httpx.AsyncClient() as client:
        if block_number:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/tokenPrices/all/{token_address}/{block_number}")
        else:
            response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/tokenPrices/all/{token_address}")
        response.raise_for_status()
        data = response.json()
        return GetTokenPriceAllResponse.model_validate(data)

@mcp.tool
async def get_token_price_all(token_address: str, block_number: Optional[int] = None) -> GetTokenPriceAllResponse:
    """Get token prices across all pools where the token is traded.
    
    Args:
        token_address: The contract address of the token
        block_number: Optional block number. If not provided, returns latest data
        
    Returns:
        GetTokenPriceAllResponse: Dictionary mapping pool addresses to token prices
    """
    return await _get_token_price_all(token_address, block_number)

async def _get_trade_volume_agg_all_pools(token_address: str, time_interval: int) -> GetTradeVolumeAggResponse:
    """Get trade volume aggregation for all pools for a specific token and time interval."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/tradeVolumeAllPools/{token_address}/{time_interval}")
        response.raise_for_status()
        data = response.json()
        return GetTradeVolumeAggResponse.model_validate(data)

@mcp.tool
async def get_trade_volume_agg_all_pools(token_address: str, time_interval: int) -> GetTradeVolumeAggResponse:
    """Get aggregated trade volume for a token across all pools over a time interval.
    
    Args:
        token_address: The contract address of the token
        time_interval: Time interval in seconds for aggregation
        
    Returns:
        GetTradeVolumeAggResponse: Aggregated trading volume data with time interval information
    """
    return await _get_trade_volume_agg_all_pools(token_address, time_interval)

async def _get_trade_volume_agg(pool_address: str, time_interval: int) -> GetTradeVolumeAggResponse:
    """Get trade volume aggregation for a specific pool and time interval."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/tradeVolume/{pool_address}/{time_interval}")
        response.raise_for_status()
        data = response.json()
        return GetTradeVolumeAggResponse.model_validate(data)

@mcp.tool
async def get_trade_volume_agg(pool_address: str, time_interval: int) -> GetTradeVolumeAggResponse:
    """Get aggregated trade volume for a specific pool over a time interval.
    
    Args:
        pool_address: The contract address of the pool
        time_interval: Time interval in seconds for aggregation
        
    Returns:
        GetTradeVolumeAggResponse: Aggregated trading volume data with time interval information
    """
    return await _get_trade_volume_agg(pool_address, time_interval)

async def _get_pool_trades(pool_address: str, start_timestamp: int, end_timestamp: int) -> GetPoolTradesResponse:
    """Get pool trades for a specific pool and time range."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/poolTrades/{pool_address}/{start_timestamp}/{end_timestamp}")
        response.raise_for_status()
        data = response.json()
        return GetPoolTradesResponse.model_validate(data)

@mcp.tool
async def get_pool_trades(pool_address: str, start_timestamp: int, end_timestamp: int) -> GetPoolTradesResponse:
    """Get detailed trade data from a specific pool over a time period.
    
    Args:
        pool_address: The contract address of the pool
        start_timestamp: Start timestamp for the query range
        end_timestamp: End timestamp for the query range
        
    Returns:
        GetPoolTradesResponse: List of detailed trade information including amounts, prices, and timestamps
    """
    return await _get_pool_trades(pool_address, start_timestamp, end_timestamp)

async def _get_token_price_series(token_address: str, pool_address: str, time_interval: int, step_seconds: int) -> GetTokenPriceSeriesResponse:
    """Get token price series for a specific token, pool, time interval, and step seconds."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/timeSeries/{token_address}/{pool_address}/{time_interval}/{step_seconds}")
        response.raise_for_status()
        data = response.json()
        return GetTokenPriceSeriesResponse.model_validate(data)

@mcp.tool
async def get_token_price_series(token_address: str, pool_address: str, time_interval: int, step_seconds: int) -> GetTokenPriceSeriesResponse:
    """Get time series of token prices for analysis of price trends and patterns.
    
    Args:
        token_address: The contract address of the token
        pool_address: The contract address of the pool
        time_interval: Time interval for the series
        step_seconds: Step size in seconds between data points
        
    Returns:
        GetTokenPriceSeriesResponse: Time series data with price points ordered chronologically
    """
    return await _get_token_price_series(token_address, pool_address, time_interval, step_seconds)

async def _get_daily_active_tokens(page: int = 1, size: int = 50, metadata: bool = False, time_interval: int = 86400) -> GetDailyActiveTokensResponse:
    """Get daily active tokens with pagination."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/dailyActiveTokens", params={"page": page, "size": size, "metadata": metadata, "time_interval": time_interval})
        response.raise_for_status()
        data = response.json()
        return GetDailyActiveTokensResponse.model_validate(data)

@mcp.tool
async def get_daily_active_tokens(page: int = 1, size: int = 50, metadata: bool = False, time_interval: int = 86400) -> GetDailyActiveTokensResponse:
    """Get tokens that had trading activity during a specific period with pagination.
    
    Args:
        page: Page number for pagination (default: 1)
        size: Number of items per page (default: 50)
        metadata: Whether to include token metadata (default: False)
        time_interval: Time interval in seconds (default: 86400 - 1 day)
        
    Returns:
        GetDailyActiveTokensResponse: List of active tokens with frequency and metadata, plus pagination info
    """
    return await _get_daily_active_tokens(page, size, metadata, time_interval)

async def _get_daily_active_pools(page: int = 1, size: int = 50, metadata: bool = False, time_interval: int = 86400) -> GetDailyActivePoolsResponse:
    """Get daily active pools with pagination."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/dailyActivePools", params={"page": page, "size": size, "metadata": metadata, "time_interval": time_interval})
        response.raise_for_status()
        data = response.json()
        return GetDailyActivePoolsResponse.model_validate(data)

@mcp.tool
async def get_daily_active_pools(page: int = 1, size: int = 50, metadata: bool = False, time_interval: int = 86400) -> GetDailyActivePoolsResponse:
    """Get pools that had trading activity during a specific period with pagination.
    
    Args:
        page: Page number for pagination (default: 1)
        size: Number of items per page (default: 50)
        metadata: Whether to include pool metadata (default: False)
        time_interval: Time interval in seconds (default: 86400 - 1 day)
        
    Returns:
        GetDailyActivePoolsResponse: List of active pools with frequency and metadata, plus pagination info
    """
    return await _get_daily_active_pools(page, size, metadata, time_interval)


async def _health_check() -> HealthCheckResponse:
    """Endpoint to check the health of the Snapshotter service."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/health")
        response.raise_for_status()
        data = response.json()
        return HealthCheckResponse.model_validate(data)

@mcp.tool
async def health_check() -> HealthCheckResponse:
    """Check the health status of the Snapshotter Core API service.
    
    Returns:
        HealthCheckResponse: Simple health status indicator for system monitoring
    """
    return await _health_check()

async def _get_current_epoch_data() -> GetCurrentEpochDataResponse:
    """Get the current epoch data from the protocol state contract."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/current_epoch")
        response.raise_for_status()
        data = response.json()
        return GetCurrentEpochDataResponse.model_validate(data)

@mcp.tool
async def get_current_epoch_data() -> GetCurrentEpochDataResponse:
    """Get information about the currently active epoch.
    
    Returns:
        GetCurrentEpochDataResponse: Current epoch data including begin/end times and epoch ID
    """
    return await _get_current_epoch_data()

async def _get_epoch_info(epoch_id: int) -> GetEpochInfoResponse:
    """Get epoch information for a given epoch ID."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/epoch/{epoch_id}")
        response.raise_for_status()
        data = response.json()
        return GetEpochInfoResponse.model_validate(data)

@mcp.tool
async def get_epoch_info(epoch_id: int) -> GetEpochInfoResponse:
    """Get detailed information about a specific epoch.
    
    Args:
        epoch_id: The unique identifier of the epoch
        
    Returns:
        GetEpochInfoResponse: Detailed epoch information including timestamp, block number, and epoch end
    """
    return await _get_epoch_info(epoch_id)

async def _get_project_last_finalized_epoch_info(project_id: str) -> GetProjectLastFinalizedEpochInfoResponse:
    """Get the last finalized epoch information for a given project."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/last_finalized_epoch/{project_id}")
        response.raise_for_status()
        data = response.json()
        return GetProjectLastFinalizedEpochInfoResponse.model_validate(data)

@mcp.tool
async def get_project_last_finalized_epoch_info(project_id: str) -> GetProjectLastFinalizedEpochInfoResponse:
    """Get the last finalized epoch information for a specific project.
    
    Args:
        project_id: The unique identifier of the project
        
    Returns:
        GetProjectLastFinalizedEpochInfoResponse: Last finalized epoch info with ID, timestamp, and block details
    """
    return await _get_project_last_finalized_epoch_info(project_id)

async def _get_data_for_project_id_epoch_id(project_id: str, epoch_id: int) -> GetDataForProjectIdEpochIdResponse:
    """Get data for a given project and epoch ID."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/data/{epoch_id}/{project_id}/")
        response.raise_for_status()
        data = response.json()
        return GetDataForProjectIdEpochIdResponse.model_validate(data)

@mcp.tool
async def get_data_for_project_id_epoch_id(project_id: str, epoch_id: int) -> GetDataForProjectIdEpochIdResponse:
    """Get comprehensive data for a specific project and epoch combination.
    
    Args:
        project_id: The unique identifier of the project
        epoch_id: The unique identifier of the epoch
        
    Returns:
        GetDataForProjectIdEpochIdResponse: Comprehensive snapshot data including reserves, prices, volumes, fees, and historical data
    """
    return await _get_data_for_project_id_epoch_id(project_id, epoch_id)

async def _get_finalized_cid_for_project_id_epoch_id(project_id: str, epoch_id: int) -> GetFinalizedCidForProjectIdEpochIdResponse:
    """Get finalized cid for a given project_id and epoch_id."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SNAPSHOTTER_CORE_API_URL}/cid/{epoch_id}/{project_id}/")
        response.raise_for_status()
        data = response.json()
        return GetFinalizedCidForProjectIdEpochIdResponse.model_validate(data)

@mcp.tool
async def get_finalized_cid_for_project_id_epoch_id(project_id: str, epoch_id: int) -> GetFinalizedCidForProjectIdEpochIdResponse:
    """Get the finalized IPFS CID for a specific project and epoch combination.
    
    Args:
        project_id: The unique identifier of the project
        epoch_id: The unique identifier of the epoch
        
    Returns:
        GetFinalizedCidForProjectIdEpochIdResponse: IPFS CID that can be used to retrieve finalized data from IPFS storage
    """
    return await _get_finalized_cid_for_project_id_epoch_id(project_id, epoch_id)

if __name__ == "__main__":
    import sys
    
    # Default values
    transport = "stdio"
    host = "127.0.0.1"
    port = 8000
    
    # Parse command line arguments
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--transport" and i + 1 < len(args):
            transport = args[i + 1]
            i += 2
        elif args[i] == "--host" and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        elif args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    # Run with appropriate transport
    if transport == "http":
        print(f"Starting MCP server with HTTP transport on {host}:{port}")
        mcp.run(transport="http", host=host, port=port)
    elif transport == "sse":
        print(f"Starting MCP server with SSE transport on {host}:{port}")
        mcp.run(transport="sse", host=host, port=port)
    else:
        print("Starting MCP server with STDIO transport")
        mcp.run(transport="stdio")
