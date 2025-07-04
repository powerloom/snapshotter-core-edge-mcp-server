from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, RootModel


# --- Common Models ---


class TokenMetadata(BaseModel):
    """
    Represents metadata for a cryptocurrency token.
    
    This model contains essential information about a token including its address,
    name, symbol, and decimal places used for precision in calculations.
    
    Attributes:
        address (Optional[str]): The blockchain address of the token. Can be None
            if the token address is not available or not yet assigned.
        name (str): The full name of the token (e.g., "Ethereum", "USD Coin").
        symbol (str): The short symbol/abbreviation of the token (e.g., "ETH", "USDC").
        decimals (int): The number of decimal places the token supports for
            precision in calculations and display.
    """
    address: Optional[str] = None
    name: str
    symbol: str
    decimals: int


class Epoch(BaseModel):
    """
    Represents a time epoch or block range for data snapshots.
    
    An epoch defines a specific time period or block range during which
    data snapshots are taken. This is commonly used in blockchain data
    aggregation and indexing systems.
    
    Attributes:
        begin (int): The starting block number or timestamp of the epoch.
        end (int): The ending block number or timestamp of the epoch.
        epochId (Optional[int]): Unique identifier for the epoch. Present in
            get_current_epoch_data responses but may be None in other contexts.
    """
    begin: int
    end: int
    epochId: Optional[int] = None  # epochId is present in get_current_epoch_data


class Log(BaseModel):
    """
    Represents a blockchain transaction log entry.
    
    This model captures detailed information about blockchain events and logs,
    including transaction details, block information, and event-specific data.
    Used for tracking trades, transfers, and other blockchain activities.
    
    Attributes:
        _score (int): Relevance score for search/filtering purposes.
        address (str): The contract address that emitted this log.
        blockNumber (int): The block number where this log was created.
        data (str): Raw log data in hexadecimal format.
        eventName (str): Name of the event that triggered this log.
        filterName (str): Name of the filter used to capture this log.
        logIndex (int): Index of this log within the block.
        topics (List[str]): List of topics associated with this log event.
        transactionHash (str): Hash of the transaction that created this log.
        transactionIndex (int): Index of the transaction within the block.
    """
    _score: int
    address: str
    blockNumber: int
    data: str
    eventName: str
    filterName: str
    logIndex: int
    topics: List[str]
    transactionHash: str
    transactionIndex: int


class TradeData(BaseModel):
    """
    Represents detailed data for a single trade transaction.
    
    This model contains comprehensive information about a trade including
    amounts, prices, liquidity, and calculated values. Used for analyzing
    trading activity and market movements.
    
    Attributes:
        amount0 (float): Amount of token0 involved in the trade.
        amount1 (float): Amount of token1 involved in the trade.
        block_timestamp (int): Unix timestamp when the trade occurred.
        calculated_eth_price (float): Calculated ETH price at the time of trade.
        calculated_token0_amount (float): Calculated amount of token0 in the trade.
        calculated_token1_amount (float): Calculated amount of token1 in the trade.
        calculated_trade_amount_usd (float): Total trade value calculated in USD.
        liquidity (int): Liquidity value at the time of the trade.
        recipient (str): Address receiving the traded tokens.
        sender (str): Address sending the traded tokens.
        sqrtPriceX96 (int): Square root of price in X96 format (Uniswap V3 specific).
        tick (int): Tick index representing the price position in the pool.
    """
    amount0: float
    amount1: float
    block_timestamp: int
    calculated_eth_price: float
    calculated_token0_amount: float
    calculated_token1_amount: float
    calculated_trade_amount_usd: float
    liquidity: int
    recipient: str
    sender: str
    sqrtPriceX96: int
    tick: int


class Trade(BaseModel):
    """
    Represents a complete trade transaction with log and data information.
    
    This model combines the blockchain log entry with the calculated trade data
    to provide a complete picture of a trading transaction.
    
    Attributes:
        tradeType (str): Type of trade (e.g., "swap", "mint", "burn").
        log (Log): The blockchain log entry associated with this trade.
        data (TradeData): Detailed trade data and calculations.
    """
    tradeType: str
    log: Log
    data: TradeData


class Pagination(BaseModel):
    """
    Represents pagination information for list responses.
    
    This model provides metadata about paginated results, including current page,
    page size, total count, and total pages available.
    
    Attributes:
        page (int): Current page number (1-based indexing).
        size (int): Number of items per page.
        total (int): Total number of items across all pages.
        total_pages (int): Total number of pages available.
    """
    page: int
    size: int
    total: int
    total_pages: int


# --- Uniswap Endpoints ---


class PoolMetadata(BaseModel):
    """
    Represents metadata for a Uniswap liquidity pool.
    
    This model contains information about a specific liquidity pool including
    the tokens involved, fee structure, and factory contract.
    
    Attributes:
        address (str): The contract address of the liquidity pool.
        token0 (TokenMetadata): Metadata for the first token in the pool.
        token1 (TokenMetadata): Metadata for the second token in the pool.
        fee (int): Pool fee in basis points (e.g., 3000 = 0.3%).
        factory (str): Address of the factory contract that created this pool.
    """
    address: str
    token0: TokenMetadata
    token1: TokenMetadata
    fee: int
    factory: str


class GetTokenPoolsResponse(BaseModel):
    """
    Response model for retrieving all pools containing a specific token.
    
    This response contains a dictionary mapping pool addresses to their
    metadata for all pools that include the specified token.
    
    Attributes:
        pools (Dict[str, PoolMetadata]): Dictionary mapping pool addresses
            to their metadata objects.
    """
    pools: Dict[str, PoolMetadata]


class GetEthPriceResponse(BaseModel):
    """
    Response model for retrieving ETH price data.
    
    This response contains ETH price information for a specific epoch,
    including the price data and any previous snapshots.
    
    Attributes:
        epoch (Epoch): The epoch for which this price data is valid.
        ethPrice (Dict[str, float]): Dictionary containing ETH price data.
        previousSnapshots (List[Any]): List of previous price snapshots.
            Structure varies, so using Any for flexibility.
    """
    epoch: Epoch
    ethPrice: Dict[str, float]
    previousSnapshots: List[Any]  # Assuming this can be empty or contain varied data


class GetTokenBaseSnapshotsResponse(RootModel):
    """
    Response model for retrieving base snapshots for a token across all pools.
    
    This response contains complex nested data representing snapshots
    of token data across multiple pools. The structure is highly variable
    and nested, so using Any for maximum flexibility.
    
    Attributes:
        root (Dict[str, Any]): Dictionary where keys are pool addresses and
            values are complex nested snapshot data structures.
    """
    # The key is the pool address
    root: Dict[str, Any]  # This structure is complex and nested, using Any for now



class GetBaseSnapshotResponse(BaseModel):
    """
    Response model for retrieving base snapshot data for a specific pool.
    
    This response contains comprehensive snapshot data for a pool at a specific
    epoch, including token reserves, prices, trading volumes, and fees. The data
    is organized by timestamps to track changes over time within the epoch.
    
    Attributes:
        address (str): The pool contract address.
        epoch (Epoch): The epoch information for this snapshot.
        timestamps (Dict[str, int]): Dictionary mapping timestamp identifiers
            to actual timestamp values for data points.
        token0 (str): Address of the first token in the pool.
        token1 (str): Address of the second token in the pool.
        token0Reserves (Dict[str, float]): Token0 reserves mapped by timestamp.
        token1Reserves (Dict[str, float]): Token1 reserves mapped by timestamp.
        token0ReservesUSD (Dict[str, float]): Token0 reserves in USD mapped by timestamp.
        token1ReservesUSD (Dict[str, float]): Token1 reserves in USD mapped by timestamp.
        token0Prices (Dict[str, float]): Token0 prices mapped by timestamp.
        token1Prices (Dict[str, float]): Token1 prices mapped by timestamp.
        token0PricesUSD (Dict[str, float]): Token0 prices in USD mapped by timestamp.
        token1PricesUSD (Dict[str, float]): Token1 prices in USD mapped by timestamp.
        totalTrade (float): Total trading volume for the epoch.
        totalTradeMintBurn (float): Total mint/burn volume for the epoch.
        totalFee (float): Total fees collected during the epoch.
        token0MintBurnVolume (float): Token0 mint/burn volume.
        token1MintBurnVolume (float): Token1 mint/burn volume.
        token0MintBurnVolumeUSD (float): Token0 mint/burn volume in USD.
        token1MintBurnVolumeUSD (float): Token1 mint/burn volume in USD.
        token0TradeVolume (float): Token0 trading volume.
        token1TradeVolume (float): Token1 trading volume.
        token0TradeVolumeUSD (float): Token0 trading volume in USD.
        token1TradeVolumeUSD (float): Token1 trading volume in USD.
        previousSnapshots (List[Any]): List of previous snapshot data.
            Structure varies, so using Any for flexibility.
    """
    address: str
    epoch: Epoch
    timestamps: Dict[str, int]
    token0: str
    token1: str
    token0Reserves: Dict[str, float]
    token1Reserves: Dict[str, float]
    token0ReservesUSD: Dict[str, float]
    token1ReservesUSD: Dict[str, float]
    token0Prices: Dict[str, float]
    token1Prices: Dict[str, float]
    token0PricesUSD: Dict[str, float]
    token1PricesUSD: Dict[str, float]
    totalTrade: float
    totalTradeMintBurn: float
    totalFee: float
    token0MintBurnVolume: float
    token1MintBurnVolume: float
    token0MintBurnVolumeUSD: float
    token1MintBurnVolumeUSD: float
    token0TradeVolume: float
    token1TradeVolume: float
    token0TradeVolumeUSD: float
    token1TradeVolumeUSD: float
    previousSnapshots: List[Any]  # Assuming this can be empty or contain varied data


class GetTradesSnapshotResponse(BaseModel):
    """
    Response model for retrieving trades snapshot data for a specific pool.
    
    This response contains all trades that occurred in a pool during a specific
    epoch, along with historical snapshot data for context and analysis.
    
    Attributes:
        address (str): The pool contract address.
        epoch (Epoch): The epoch information for this trades snapshot.
        trades (List[Trade]): List of all trades that occurred during the epoch.
        previousSnapshots (List[Any]): List of previous trades snapshot data.
            Structure varies, so using Any for flexibility.
    """
    address: str
    epoch: Epoch
    trades: List[Trade]
    previousSnapshots: List[Any]  # Assuming this can be empty or contain varied data


class GetAllTradesSnapshotResponse(BaseModel):
    """
    Response model for retrieving trades snapshot data across all pools.
    
    This response contains trades data for multiple pools during a specific
    epoch, organized by pool address. This provides a comprehensive view
    of trading activity across the entire protocol.
    
    Attributes:
        epoch (Epoch): The epoch information for this trades snapshot.
        tradeData (Dict[str, GetTradesSnapshotResponse]): Dictionary mapping
            pool addresses to their respective trades snapshot data.
        previousSnapshots (List[Any]): List of previous trades snapshot data.
            Structure varies, so using Any for flexibility.
    """
    epoch: Epoch
    tradeData: Dict[str, GetTradesSnapshotResponse]
    previousSnapshots: List[Any]  # Assuming this can be empty or contain varied data


class GetTokenPriceAllResponse(RootModel):
    """
    Response model for retrieving token prices across all pools.
    
    This response contains the current price of a specific token across
    all pools where it is traded. The response is structured as a simple
    mapping from pool addresses to token prices.
    
    Attributes:
        root (Dict[str, Optional[float]]): Dictionary mapping pool addresses
            to token prices. Prices may be None if the token is not traded
            in a particular pool or if price data is unavailable.
    """
    # The keys are pool addresses, values are floats or None
    root: Dict[str, Optional[float]]


class GetTradeVolumeAggResponse(BaseModel):
    """
    Response model for aggregated trade volume data.
    
    This response provides aggregated trading volume information over a
    specified time interval, useful for analyzing trading activity patterns
    and market dynamics.
    
    Attributes:
        totalTradeVolume (float): Total trading volume over the time interval.
        timeInterval (int): The time interval in seconds over which the
            volume data was aggregated.
    """
    totalTradeVolume: float
    timeInterval: int


class GetPoolTradesResponse(RootModel):
    """
    Response model for retrieving detailed trade data from a specific pool.
    
    This response contains a list of individual trades that occurred in a
    pool over a specified time period. Each trade contains detailed information
    about the transaction, including amounts, prices, and timestamps.
    
    Attributes:
        root (List[Dict[str, Any]]): List of trade objects, each containing
            detailed trade information. Using Any for flexibility due to
            complex and varied trade data structures.
    """
    # This is a list of trade details, not a single object
    root: List[Dict[str, Any]]  # Using Any for now due to nested and varied structure


class PriceSeriesEntry(BaseModel):
    """
    Model representing a single price data point in a price series.
    
    This model captures the price of a token at a specific block and time,
    forming part of a time series analysis of price movements.
    
    Attributes:
        blockNumber (int): The blockchain block number when this price was recorded.
        price (float): The token price at this point in time.
        timestamp (int): Unix timestamp when this price was recorded.
    """
    blockNumber: int
    price: float
    timestamp: int


class GetTokenPriceSeriesResponse(BaseModel):
    """
    Response model for retrieving a time series of token prices.
    
    This response contains a series of price data points for a token over
    time, allowing for analysis of price trends and patterns. The data is
    collected at regular intervals specified by the timeInterval parameter.
    
    Attributes:
        priceSeries (List[PriceSeriesEntry]): List of price data points
            ordered chronologically.
        timeInterval (int): The time interval in seconds between price
            data points.
    """
    priceSeries: List[PriceSeriesEntry]
    timeInterval: int


class ActiveToken(BaseModel):
    """
    Model representing an active token with its trading frequency and metadata.
    
    This model is used in daily active tokens responses to show which tokens
    had trading activity and how frequently they were traded.
    
    Attributes:
        token_address (str): The token contract address.
        frequency (int): Number of times this token was traded during the period.
        metadata (TokenMetadata): Detailed metadata about the token including
            name, symbol, and other relevant information.
    """
    token_address: str
    frequency: int
    metadata: TokenMetadata


class GetDailyActiveTokensResponse(BaseModel):
    """
    Response model for retrieving daily active tokens data.
    
    This response provides information about tokens that had trading activity
    during a specific day, including their trading frequency and metadata.
    The response is paginated to handle large datasets efficiently.
    
    Attributes:
        active_tokens (List[ActiveToken]): List of tokens that had trading
            activity during the period.
        pagination (Pagination): Pagination information for the response.
    """
    active_tokens: List[ActiveToken]
    pagination: Pagination


class ActivePool(BaseModel):
    """
    Model representing an active pool with its trading frequency and metadata.
    
    This model is used in daily active pools responses to show which pools
    had trading activity and how frequently they were traded. Similar to
    ActiveToken but for pool-level activity tracking.
    
    Attributes:
        pool_address (str): The pool contract address that had trading activity.
        frequency (int): Number of times this pool was traded during the period.
        metadata (PoolMetadata): Detailed metadata about the pool including
            token information, fees, and other relevant pool characteristics.
    """
    pool_address: str
    frequency: int
    metadata: PoolMetadata


class GetDailyActivePoolsResponse(BaseModel):
    """
    Response model for retrieving daily active pools data.
    
    This response provides information about pools that had trading activity
    during a specific day, including their trading frequency and metadata.
    The response is paginated to handle large datasets efficiently.
    
    Attributes:
        active_pools (List[ActivePool]): List of pools that had trading
            activity during the period.
        pagination (Pagination): Pagination information for the response.
    """
    active_pools: List[ActivePool]
    pagination: Pagination


# --- Snapshotter Core API Endpoints ---


class HealthCheckResponse(BaseModel):
    """
    Response model for the health check endpoint.
    
    This simple response indicates whether the Snapshotter Core API is
    operational and responding to requests. Used for monitoring and
    system health verification.
    
    Attributes:
        status (str): Health status of the API, typically "healthy" or
            "unhealthy" to indicate system status.
    """
    status: str


class GetCurrentEpochDataResponse(BaseModel):
    """
    Response model for retrieving current epoch data.
    
    This response provides information about the currently active epoch,
    including its time range and unique identifier. Used for understanding
    the current state of the blockchain data indexing system.
    
    Attributes:
        begin (int): The starting block number or timestamp of the current epoch.
        end (int): The ending block number or timestamp of the current epoch.
        epochId (int): Unique identifier for the current epoch.
    """
    begin: int
    end: int
    epochId: int


class GetEpochInfoResponse(BaseModel):
    """
    Response model for retrieving information about a specific epoch.
    
    This response provides detailed information about a particular epoch
    including its timing and block information. Used for epoch-specific
    data analysis and verification.
    
    Attributes:
        timestamp (int): Unix timestamp when the epoch information was recorded.
        blocknumber (int): The block number associated with this epoch.
        epochEnd (int): The ending block number or timestamp of this epoch.
    """
    timestamp: int
    blocknumber: int
    epochEnd: int


class GetProjectLastFinalizedEpochInfoResponse(BaseModel):
    """
    Response model for retrieving the last finalized epoch information for a project.
    
    This response provides information about the most recently finalized epoch
    for a specific project, including its timing and block information.
    Used for tracking project progress and data finalization status.
    
    Attributes:
        epochId (int): Unique identifier for the last finalized epoch.
        timestamp (int): Unix timestamp when the epoch was finalized.
        blocknumber (int): The block number when the epoch was finalized.
        epochEnd (int): The ending block number or timestamp of the finalized epoch.
    """
    epochId: int
    timestamp: int
    blocknumber: int
    epochEnd: int


class GetDataForProjectIdEpochIdResponse(BaseModel):
    """
    Response model for retrieving comprehensive data for a specific project and epoch.
    
    This response contains detailed snapshot data for a particular project
    and epoch combination, including token information, prices, reserves,
    trading volumes, and other metrics. This is one of the most comprehensive
    data models in the system.
    
    Attributes:
        address (str): The contract address of the pool or project.
        epoch (Epoch): Epoch information including begin/end times and epoch ID.
        previousSnapshots (List[Any]): List of previous snapshot data for
            historical comparison and trend analysis.
        timestamps (Dict[str, int]): Dictionary mapping data point identifiers
            to their corresponding timestamps.
        token0 (str): Contract address of the first token in the pool.
        token0MintBurnVolume (float): Total mint/burn volume for token0 in
            the pool's native units.
        token0MintBurnVolumeUSD (float): Total mint/burn volume for token0
            converted to USD value.
        token0Prices (Dict[str, float]): Dictionary mapping price identifiers
            to token0 prices in various denominations.
        token0PricesUSD (Dict[str, float]): Dictionary mapping price identifiers
            to token0 prices in USD.
        token0Reserves (Dict[str, float]): Dictionary mapping reserve identifiers
            to token0 reserve amounts in native units.
        token0ReservesUSD (Dict[str, float]): Dictionary mapping reserve identifiers
            to token0 reserve amounts in USD value.
        token0TradeVolume (float): Total trading volume for token0 in native units.
        token0TradeVolumeUSD (float): Total trading volume for token0 in USD value.
        token1 (str): Contract address of the second token in the pool.
        token1MintBurnVolume (float): Total mint/burn volume for token1 in
            the pool's native units.
        token1MintBurnVolumeUSD (float): Total mint/burn volume for token1
            converted to USD value.
        token1Prices (Dict[str, float]): Dictionary mapping price identifiers
            to token1 prices in various denominations.
        token1PricesUSD (Dict[str, float]): Dictionary mapping price identifiers
            to token1 prices in USD.
        token1Reserves (Dict[str, float]): Dictionary mapping reserve identifiers
            to token1 reserve amounts in native units.
        token1ReservesUSD (Dict[str, float]): Dictionary mapping reserve identifiers
            to token1 reserve amounts in USD value.
        token1TradeVolume (float): Total trading volume for token1 in native units.
        token1TradeVolumeUSD (float): Total trading volume for token1 in USD value.
        totalFee (float): Total fees collected by the pool during the epoch.
        totalTrade (float): Total trading volume across both tokens in native units.
        totalTradeMintBurn (float): Combined trading volume including mint/burn
            activities for both tokens.
    """
    address: str
    epoch: Epoch
    previousSnapshots: List[Any]
    timestamps: Dict[str, int]
    token0: str
    token0MintBurnVolume: float
    token0MintBurnVolumeUSD: float
    token0Prices: Dict[str, float]
    token0PricesUSD: Dict[str, float]
    token0Reserves: Dict[str, float]
    token0ReservesUSD: Dict[str, float]
    token0TradeVolume: float
    token0TradeVolumeUSD: float
    token1: str
    token1MintBurnVolume: float
    token1MintBurnVolumeUSD: float
    token1Prices: Dict[str, float]
    token1PricesUSD: Dict[str, float]
    token1Reserves: Dict[str, float]
    token1ReservesUSD: Dict[str, float]
    token1TradeVolume: float
    token1TradeVolumeUSD: float
    totalFee: float
    totalTrade: float
    totalTradeMintBurn: float


class GetFinalizedCidForProjectIdEpochIdResponse(RootModel):
    """
    Response model for retrieving the finalized CID (Content Identifier) for a project and epoch.
    
    This response contains the IPFS CID (Content Identifier) for finalized
    data associated with a specific project and epoch combination. The CID
    is used to retrieve the actual data from IPFS storage.
    
    Attributes:
        root (str): The IPFS CID (Content Identifier) as a string. This CID
            can be used to retrieve the finalized data from IPFS storage.
    """
    root: str  # This endpoint returns a plain string (CID)
