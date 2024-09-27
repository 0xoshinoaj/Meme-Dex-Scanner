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

# ERC20 代幣 ABI（僅包含 name 函數）
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]

def get_token_name(address):
    try:
        token_contract = w3.eth.contract(address=address, abi=ERC20_ABI)
        return token_contract.functions.name().call()
    except Exception as e:
        print(f"Error getting token name: {e}")
        return "Unknown Token"

def handle_event(event):
    if event['address'].lower() == UNISWAP_V2_FACTORY.lower():
        token0 = '0x' + event['topics'][1][26:]
        token1 = '0x' + event['topics'][2][26:]
        pair = '0x' + event['data'][26:66]
        
        # 確定哪個是代幣，哪個是 ETH/WETH
        if token1.lower() == WETH_ADDRESS.lower():
            token_address = token0
        elif token0.lower() == WETH_ADDRESS.lower():
            token_address = token1
        else:
            # 如果兩個都不是 WETH，我們假設 token0 是主要代幣
            token_address = token0
        
        token_name = get_token_name(token_address)
        
        print(f"New Uniswap V2 Pair Created: {pair}")
        print(f"代幣名稱：{token_name}")
        print(f"代幣合約：{token_address}")
    
    elif event['address'].lower() == UNISWAP_V3_FACTORY.lower():
        token0 = '0x' + event['topics'][1][26:]
        token1 = '0x' + event['topics'][2][26:]
        fee = int(event['topics'][3], 16)
        pool = '0x' + event['data'][26:66]
        
        # 確定哪個是代幣，哪個是 ETH/WETH
        if token1.lower() == WETH_ADDRESS.lower():
            token_address = token0
        elif token0.lower() == WETH_ADDRESS.lower():
            token_address = token1
        else:
            # 如果兩個都不是 WETH，我們假設 token0 是主要代幣
            token_address = token0
        
        token_name = get_token_name(token_address)
        
        print(f"New Uniswap V3 Pool Created: {pool}")
        print(f"代幣名稱：{token_name}")
        print(f"代幣合約：{token_address}")
        print(f"Fee: {fee}")
    
    print("---")

async def subscribe_to_events():
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
                handle_event(event)
            except Exception as e:
                print(f"Error: {e}")

async def main():
    print("Starting to monitor Uniswap V2 and V3 for new pairs/pools...")
    await subscribe_to_events()

if __name__ == '__main__':
    asyncio.run(main())