import asyncio
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

async def test_all_endpoints():
    print("--- Testing All Endpoints ---")

    # Helper function to run and print results
    async def run_test(func_name_str, func, *args, model=None, **kwargs):
        print(f"\nTesting {func_name_str}...")
        try:
            result = await func(*args, **kwargs)
            print(f"{func_name_str} response: {result}")
            if model:
                parsed_result = model.parse_obj(result)
                print(f"{func_name_str} parsed successfully.")
                # You can add assertions here to validate the parsed_result further
        except httpx.HTTPStatusError as e:
            print(f"Error testing {func_name_str}: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An unexpected error occurred during {func_name_str} test: {e}")

    # Uniswap Endpoints
    await run_test("get_pool_metadata", _get_pool_metadata, model=PoolMetadata, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3")
    await run_test("get_token_pools", _get_token_pools, model=GetTokenPoolsResponse, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48")
    await run_test("get_ethprice", _get_ethprice, model=GetEthPriceResponse)
    await run_test("get_ethprice_block", _get_ethprice, model=GetEthPriceResponse, block_number=22844810)
    await run_test("get_token_price_pool_with_block", _get_token_price_pool, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48", pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3", block_number=22844810)
    await run_test("get_token_price_pool_no_block", _get_token_price_pool, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48", pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3")
    await run_test("get_token_base_snapshots", _get_token_base_snapshots, model=GetTokenBaseSnapshotsResponse, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48")
    await run_test("get_base_snapshot_with_block", _get_base_snapshot, model=GetBaseSnapshotResponse, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3", block_number=22844810)
    await run_test("get_base_snapshot_no_block", _get_base_snapshot, model=GetBaseSnapshotResponse, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3")
    await run_test("get_trades_snapshot_with_block", _get_trades_snapshot, model=GetTradesSnapshotResponse, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3", block_number=22844810)
    await run_test("get_trades_snapshot_no_block", _get_trades_snapshot, model=GetTradesSnapshotResponse, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3")
    await run_test("get_all_trades_snapshot_with_block", _get_all_trades_snapshot, model=GetAllTradesSnapshotResponse, block_number=22844810)
    await run_test("get_all_trades_snapshot_no_block", _get_all_trades_snapshot, model=GetAllTradesSnapshotResponse)
    await run_test("get_token_price_all_with_block", _get_token_price_all, model=GetTokenPriceAllResponse, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48", block_number=22844810)
    await run_test("get_token_price_all_no_block", _get_token_price_all, model=GetTokenPriceAllResponse, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48")
    await run_test("get_trade_volume_agg_all_pools", _get_trade_volume_agg_all_pools, model=GetTradeVolumeAggResponse, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48", time_interval=86400)
    await run_test("get_trade_volume_agg", _get_trade_volume_agg, model=GetTradeVolumeAggResponse, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3", time_interval=86400)
    await run_test("get_pool_trades", _get_pool_trades, model=GetPoolTradesResponse, pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3", start_timestamp=1751615578, end_timestamp=1751619178)
    await run_test("get_token_price_series", _get_token_price_series, model=GetTokenPriceSeriesResponse, token_address="0xe0B7AD7F8F26e2b00C8b47b5Df370f15F90fCF48", pool_address="0x7E75b6876a9feE811EC67B55385BA5A1491D11f3", time_interval=86400, step_seconds=3600)
    await run_test("get_daily_active_tokens", _get_daily_active_tokens, model=GetDailyActiveTokensResponse, page=1, size=10, metadata=True)
    await run_test("get_daily_active_pools", _get_daily_active_pools, model=GetDailyActivePoolsResponse, page=1, size=10, metadata=True)

    # Snapshotter Core API Endpoints
    await run_test("health_check", _health_check, model=HealthCheckResponse)
    await run_test("get_current_epoch_data", _get_current_epoch_data, model=GetCurrentEpochDataResponse)
    await run_test("get_epoch_info", _get_epoch_info, model=GetEpochInfoResponse, epoch_id=22844810)
    await run_test("get_project_last_finalized_epoch_info", _get_project_last_finalized_epoch_info, model=GetProjectLastFinalizedEpochInfoResponse, project_id="baseSnapshot:0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b:UNISWAPV3")
    await run_test("get_data_for_project_id_epoch_id", _get_data_for_project_id_epoch_id, model=GetDataForProjectIdEpochIdResponse, project_id="baseSnapshot:0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b:UNISWAPV3", epoch_id=22844810)
    await run_test("get_finalized_cid_for_project_id_epoch_id", _get_finalized_cid_for_project_id_epoch_id, model=GetFinalizedCidForProjectIdEpochIdResponse, project_id="baseSnapshot:0xc7bBeC68d12a0d1830360F8Ec58fA599bA1b0e9b:UNISWAPV3", epoch_id=22844810)

if __name__ == "__main__":
    asyncio.run(test_all_endpoints())