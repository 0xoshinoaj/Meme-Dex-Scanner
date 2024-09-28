import asyncio
from uniswap_monitor import monitor_uniswap, parse_event
from token_info import get_token_info
from web3 import Web3

VERSION = "1.0.0"

# WETH 地址（以太坊主網）
WETH_ADDRESS = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

async def handle_new_pair(event):
    parsed_event = parse_event(event)
    if parsed_event:
        if parsed_event[0] == 'V2':
            version, token0, token1, pair = parsed_event
            if token0.lower() == WETH_ADDRESS.lower():
                non_weth_token, weth_token = token1, token0
            else:
                non_weth_token, weth_token = token0, token1
            
            name, symbol = get_token_info(Web3.to_checksum_address(non_weth_token))
            print(f"Uniswap V2 新交易對：{symbol} / WETH ({name})")
            print(f"交易對合約：{pair}")
            print(f"{symbol}合約：{non_weth_token}")
        elif parsed_event[0] == 'V3':
            version, token0, token1, pool, fee = parsed_event
            if token0.lower() == WETH_ADDRESS.lower():
                non_weth_token, weth_token = token1, token0
            else:
                non_weth_token, weth_token = token0, token1
            
            name, symbol = get_token_info(Web3.to_checksum_address(non_weth_token))
            print(f"Uniswap V3 新交易對：{symbol} / WETH ({name})")
            print(f"交易對合約：{pool}")
            print(f"{symbol}合約：{non_weth_token}")
            print(f"費用：{fee/10000}%")
        print("---")

async def main():
    print("開始監控 Uniswap V2 和 V3 的新交易對...")
    await monitor_uniswap(handle_new_pair)

if __name__ == '__main__':
    asyncio.run(main())