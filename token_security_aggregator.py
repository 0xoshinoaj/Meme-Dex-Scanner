from token_security.checker1 import Checker1
#from token_security.checker2 import Checker2
#from token_security.checker3 import Checker3
#from token_security.checker4 import Checker4

class TokenSecurityAggregator:
    def __init__(self):
        self.checkers = [
            Checker1(),
            #Checker2(),
            #Checker3(),
            #Checker4()
        ]

    def aggregate_security_info(self, contract_address):
        results = {}
        for checker in self.checkers:
            try:
                results[checker.name] = checker.check_security(contract_address)
            except Exception as e:
                results[checker.name] = {"status": "ERROR", "risks": [str(e)]}
        return results

def check_token_security(contract_address):
    aggregator = TokenSecurityAggregator()
    return aggregator.aggregate_security_info(contract_address)

# 如果直接運行此文件，可以添加一個簡單的測試
if __name__ == "__main__":
    test_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # DAI token address
    result = check_token_security(test_address)
    print(f"Security check results for {test_address}:")
    for checker_name, info in result.items():
        if info:
            print(f"{checker_name}: Status - {info.get('status', 'UNKNOWN')}, Risks - {info.get('risks', 'N/A')}")
            print("Details:")
            for key, value in info.get('info', {}).items():
                print(f"- {key}: {value}")
        else:
            print(f"{checker_name}: Failed to retrieve information")