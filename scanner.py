import requests
import time

def get_latest_pairs(chain):
    url = "https://api.dexscreener.com/latest/dex/search"
    params = {
        "q": f"{chain} new"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["pairs"]
    else:
        print(f"請求失敗: {response.status_code}")
        return None

def main():
    chains = ["ethereum", "base", "solana"]
    for chain in chains:
        print(f"獲取 {chain} 鏈上的最新交易對:")
        pairs = get_latest_pairs(chain)
        if pairs:
            for pair in pairs[:5]:  # 只顯示前5個結果
                print(f"交易對地址: {pair['pairAddress']}")
                print(f"基礎代幣: {pair['baseToken']['symbol']} ({pair['baseToken']['address']})")
                print(f"報價代幣: {pair['quoteToken']['symbol']} ({pair['quoteToken']['address']})")
                print("---")
        time.sleep(1)  # 為了遵守API速率限制

if __name__ == "__main__":
    main()