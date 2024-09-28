from web3 import Web3
import json
import configparser

# 讀取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 使用 Infura 或其他以太坊節點提供商的 URL
INFURA_URL = config['ETHEREUM']['INFURA_URL']

# 初始化 Web3 實例
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ERC20 ABI（僅包含 name 和 symbol 函數）
ERC20_ABI = json.loads('''[
    {"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}
]''')

def get_token_info(contract_address):
    try:
        # 將地址轉換為校驗和格式
        checksum_address = Web3.to_checksum_address(contract_address)
        
        # 創建合約實例
        contract = w3.eth.contract(address=checksum_address, abi=ERC20_ABI)
        
        # 調用合約函數
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        
        return name, symbol
    except Exception as e:
        print(f"獲取代幣信息時發生錯誤: {str(e)}")
        return "Unknown", "Unknown"