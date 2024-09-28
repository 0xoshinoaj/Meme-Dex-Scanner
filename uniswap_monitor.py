import asyncio
import json
import websockets
from web3 import Web3
import configparser

# 讀取配置
config = configparser.ConfigParser()
config.read('config.ini')

# 使用 WebSocket 連接（替換為您的 Infura WebSocket URL）
WS_URL = config['INFURA']['WS_URL']

# Uniswap V2 和 V3 工廠合約地址
UNISWAP_V2_FACTORY = config['UNISWAP']['V2_FACTORY']
UNISWAP_V3_FACTORY = config['UNISWAP']['V3_FACTORY']

# 事件簽名
PAIR_CREATED_EVENT_SIGNATURE = config['EVENTS']['PAIR_CREATED']
POOL_CREATED_EVENT_SIGNATURE = config['EVENTS']['POOL_CREATED']

# 初始化 Web3 連接
w3 = Web3(Web3.WebsocketProvider(WS_URL))

# WETH 地址（以太坊主網）
WETH_ADDRESS = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

async def monitor_uniswap(callback):
    async with websockets.connect(WS_URL) as ws:
        subscribe_message = {
            "id": 1,
            "method": "eth_subscribe",
            "params": ["logs", {
                "address": [UNISWAP_V2_FACTORY, UNISWAP_V3_FACTORY],
                "topics": [[PAIR_CREATED_EVENT_SIGNATURE, POOL_CREATED_EVENT_SIGNATURE]]
            }]
        }
        await ws.send(json.dumps(subscribe_message))
        subscription_response = await ws.recv()
        print(f"Subscription response: {subscription_response}")

        while True:
            try:
                message = await ws.recv()
                event = json.loads(message)['params']['result']
                await callback(event)
            except Exception as e:
                print(f"Error: {e}")

def parse_event(event):
    if event['address'].lower() == UNISWAP_V2_FACTORY.lower():
        token0 = '0x' + event['topics'][1][26:]
        token1 = '0x' + event['topics'][2][26:]
        pair = '0x' + event['data'][26:66]
        return 'V2', token0, token1, pair
    elif event['address'].lower() == UNISWAP_V3_FACTORY.lower():
        token0 = '0x' + event['topics'][1][26:]
        token1 = '0x' + event['topics'][2][26:]
        fee = int(event['topics'][3], 16)
        pool = '0x' + event['data'][26:66]
        return 'V3', token0, token1, pool, fee
    return None