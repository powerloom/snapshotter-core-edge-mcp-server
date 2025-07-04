import pytest
import httpx
from main import (
    _get_pool_metadata,
    _get_token_pools,
    _get_ethprice,
    _get_token_price_pool,
    _get_token_base_snapshots,
    _get_base_snapshot,
    _get_trades_snapshot,
    _get_all_trades_snapshot,
    _get_token_price_all,
    _get_trade_volume_agg_all_pools,
    _get_trade_volume_agg,
    _get_pool_trades,
    _get_token_price_series,
    _get_daily_active_tokens,
    _get_daily_active_pools,
    _health_check,
    _get_current_epoch_data,
    _get_epoch_info,
    _get_project_last_finalized_epoch_info,
    _get_data_for_project_id_epoch_id,
    _get_finalized_cid_for_project_id_epoch_id,
)
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

# Uniswap Endpoints
@pytest.mark.asyncio
async def test_get_pool_metadata():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    result = await _get_pool_metadata(pool_address=pool_address)
    assert PoolMetadata.model_validate(result)

@pytest.mark.asyncio
async def test_get_token_pools():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    result = await _get_token_pools(token_address=token_address)
    assert GetTokenPoolsResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_ethprice():
    result = await _get_ethprice()
    assert GetEthPriceResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_ethprice_block():
    block_number = 22844810
    result = await _get_ethprice(block_number=block_number)
    assert GetEthPriceResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_token_price_pool_with_block():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    block_number = 22844810
    result = await _get_token_price_pool(token_address=token_address, pool_address=pool_address, block_number=block_number)
    assert isinstance(result, float)

@pytest.mark.asyncio
async def test_get_token_price_pool_no_block():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    result = await _get_token_price_pool(token_address=token_address, pool_address=pool_address)
    assert isinstance(result, float)

@pytest.mark.asyncio
async def test_get_token_base_snapshots():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    result = await _get_token_base_snapshots(token_address=token_address)
    assert GetTokenBaseSnapshotsResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_base_snapshot_with_block():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    block_number = 22844810
    result = await _get_base_snapshot(pool_address=pool_address, block_number=block_number)
    assert GetBaseSnapshotResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_base_snapshot_no_block():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    result = await _get_base_snapshot(pool_address=pool_address)
    assert GetBaseSnapshotResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_trades_snapshot_with_block():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    block_number = 22844810
    result = await _get_trades_snapshot(pool_address=pool_address, block_number=block_number)
    assert GetTradesSnapshotResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_trades_snapshot_no_block():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    result = await _get_trades_snapshot(pool_address=pool_address)
    assert GetTradesSnapshotResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_all_trades_snapshot_with_block():
    block_number = 22844810
    result = await _get_all_trades_snapshot(block_number=block_number)
    assert GetAllTradesSnapshotResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_all_trades_snapshot_no_block():
    result = await _get_all_trades_snapshot()
    assert GetAllTradesSnapshotResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_token_price_all_with_block():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    block_number = 22844810
    result = await _get_token_price_all(token_address=token_address, block_number=block_number)
    assert GetTokenPriceAllResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_token_price_all_no_block():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    result = await _get_token_price_all(token_address=token_address)
    assert GetTokenPriceAllResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_trade_volume_agg_all_pools():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    time_interval = 86400
    result = await _get_trade_volume_agg_all_pools(token_address=token_address, time_interval=time_interval)
    assert GetTradeVolumeAggResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_trade_volume_agg():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    time_interval = 86400
    result = await _get_trade_volume_agg(pool_address=pool_address, time_interval=time_interval)
    assert GetTradeVolumeAggResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_pool_trades():
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    start_timestamp = 1751615578
    end_timestamp = 1751619178
    result = await _get_pool_trades(pool_address=pool_address, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
    assert GetPoolTradesResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_token_price_series():
    token_address = "0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48"
    pool_address = "0x7E75b6876a9feE811EC67B55385BA5A1491D11f3"
    time_interval = 86400
    step_seconds = 3600
    result = await _get_token_price_series(token_address=token_address, pool_address=pool_address, time_interval=time_interval, step_seconds=step_seconds)
    assert GetTokenPriceSeriesResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_daily_active_tokens():
    page = 1
    size = 10
    metadata = True
    result = await _get_daily_active_tokens(page=page, size=size, metadata=metadata)
    assert GetDailyActiveTokensResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_daily_active_pools():
    page = 1
    size = 10
    metadata = True
    result = await _get_daily_active_pools(page=page, size=size, metadata=metadata)
    assert GetDailyActivePoolsResponse.model_validate(result)

# Snapshotter Core API Endpoints
@pytest.mark.asyncio
async def test_health_check():
    result = await _health_check()
    assert HealthCheckResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_current_epoch_data():
    result = await _get_current_epoch_data()
    assert GetCurrentEpochDataResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_epoch_info():
    epoch_id = 22844810
    result = await _get_epoch_info(epoch_id=epoch_id)
    assert GetEpochInfoResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_project_last_finalized_epoch_info():
    project_id = "baseSnapshot:0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b:UNISWAPV3"
    result = await _get_project_last_finalized_epoch_info(project_id=project_id)
    assert GetProjectLastFinalizedEpochInfoResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_data_for_project_id_epoch_id():
    project_id = "baseSnapshot:0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b:UNISWAPV3"
    epoch_id = 22844810
    result = await _get_data_for_project_id_epoch_id(project_id=project_id, epoch_id=epoch_id)
    assert GetDataForProjectIdEpochIdResponse.model_validate(result)

@pytest.mark.asyncio
async def test_get_finalized_cid_for_project_id_epoch_id():
    project_id = "baseSnapshot:0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b:UNISWAPV3"
    epoch_id = 22844810
    result = await _get_finalized_cid_for_project_id_epoch_id(project_id=project_id, epoch_id=epoch_id)
    assert GetFinalizedCidForProjectIdEpochIdResponse.model_validate(result)
