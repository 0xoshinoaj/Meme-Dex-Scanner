from token_security.base_checker import BaseSecurityChecker
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定義顏色常量
GREEN = "\033[32m"
RED = "\033[31m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_RED = "\033[91m"
RESET = "\033[0m"

class Checker1(BaseSecurityChecker):
    def __init__(self):
        super().__init__("Honeypot.is")
        self.risk_translations = {
            "A high amount of users can not sell their tokens. This is likely a honeypot.": "大量用戶無法出售他們的代幣。這很可能是一個蜜罐。",
            "Unknown risk": "未知風險",
            # 添加更多翻譯...
        }

    def check_security(self, contract_address):
        url = f"https://honeypot.is/ethereum?address={contract_address}"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                
                page.wait_for_selector('#titlePanel-heading', timeout=30000)
                
                status_element = page.query_selector('#titlePanel-heading')
                status = status_element.inner_text().strip() if status_element else "UNKNOWN"
                
                error_message_element = page.query_selector('p.leading-1.font-bebasNeue.text-pinkLight.text-xl')
                error_message = error_message_element.inner_text().strip() if error_message_element else ""
                
                browser.close()
            
            risk_message = error_message or "Unknown risk"
            translated_risk = self.translate_risk(risk_message)
            status_color = GREEN if status == "PASSED" else RED
            risk_color = BRIGHT_GREEN if status == "PASSED" else BRIGHT_RED
            return {
                "status": f"{status_color}{'通過' if status == 'PASSED' else '不通過'}{RESET}",
                "risks": [f"{risk_color}無風險{RESET}"] if status == "PASSED" else [f"{risk_color}{translated_risk}{RESET}"]
            }
        except Exception as e:
            logger.error(f"Unexpected error when checking {contract_address}: {str(e)}")
            return self._error_response(f"Unexpected error: {str(e)}")

    def _error_response(self, message):
        return {
            "status": f"{RED}不通過{RESET}",
            "risks": [f"{BRIGHT_RED}{message}{RESET}"]
        }

    def translate_risk(self, risk):
        return self.risk_translations.get(risk, risk)

if __name__ == "__main__":
    checker = Checker1()
    # 測試一個代幣地址
    result = checker.check_security("0x35f3262ac0749a15f18ad0d959e3298121cf9b56")
    print(f"{result['status']} {' '.join(result['risks'])}")