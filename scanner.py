import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random

def get_new_pairs():
    url = "https://dexscreener.com/new-pairs?rankBy=pairAge&order=asc&chainIds=ethereum"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    return response

def parse_new_pairs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pairs = []
    
    pair_elements = soup.select('a.ds-dex-table-row-new')
    
    for element in pair_elements:
        token_cell = element.select_one('.ds-dex-table-row-col-token')
        if token_cell:
            pair_no = token_cell.select_one('.ds-dex-table-row-badge-pair-no').text
            chain_icon = token_cell.select_one('.ds-dex-table-row-chain-icon')
            chain = chain_icon['title'] if chain_icon else "Unknown"
            dex_icon = token_cell.select_one('.ds-dex-table-row-dex-icon')
            dex = dex_icon['title'] if dex_icon else "Unknown"
            dex_version = token_cell.select_one('.ds-dex-table-row-badge-label').text
            base_token = token_cell.select_one('.ds-dex-table-row-base-token-symbol').text
            quote_token = token_cell.select_one('.ds-dex-table-row-quote-token-symbol').text
            token_name = token_cell.select_one('.ds-dex-table-row-base-token-name-text').text
            
            pair = {
                "pair_no": pair_no,
                "chain": chain,
                "dex": f"{dex} {dex_version}",
                "base_token": base_token,
                "quote_token": quote_token,
                "token_name": token_name,
                "pair": f"{base_token}/{quote_token}",
                "link": "https://dexscreener.com" + element['href']
            }
            pairs.append(pair)
    
    return pairs

def main():
    max_retries = 3
    for i in range(max_retries):
        response = get_new_pairs()
        if response.status_code == 200:
            pairs = parse_new_pairs(response.text)
            print(f"找到 {len(pairs)} 個以太坊主網上的新交易對：")
            for pair in pairs:
                print(f"排名: {pair['pair_no']}")
                print(f"代幣名稱: {pair['token_name']}")
                print(f"交易對: {pair['pair']}")
                print(f"鏈: {pair['chain']}")
                print(f"DEX: {pair['dex']}")
                print(f"鏈接: {pair['link']}")
                print("---")
            break
        else:
            print(f"請求失敗。狀態碼：{response.status_code}")
            if i < max_retries - 1:
                wait_time = random.uniform(5, 10)
                print(f"等待 {wait_time:.2f} 秒後重試...")
                time.sleep(wait_time)
            else:
                print("已達到最大重試次數，程序退出。")

if __name__ == "__main__":
    main()