# Meme-Dex-Scanner [v1.0.0]

這個項目自動監控 Uniswap V2 和 V3 的新交易對創建，並提供相關代幣信息。

## 首次使用說明

1. 安裝依賴
   確保您已安裝 Python 3.7 或更高版本，然後運行：
   ```
   pip install -r requirements.txt
   ```

2. 設置文件
   * 創建一個 `config.ini` 文件
   * 在 `config.ini` 中填入您的 Infura WebSocket URL

3. 運行程序
   在命令行中運行：
   ```
   python scanner.py
   ```

4. 驗證
   檢查控制台輸出，確認是否正確顯示新的交易對信息

## 配置文件示例 (config.ini)
