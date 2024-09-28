from token_security_aggregator import check_token_security

def test_token_security():
    # 已知的代幣合約地址列表
    test_contracts = [
        "0x2De1218C31a04E1040fC5501b89e3A58793b3DDF",  # 蜜罐合約
        "0x2a1274400cd05bb658ba07d1ef597e79d5caff3a",  # 3AC
        #"0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
        # 添加更多您想測試的代幣合約地址
    ]

    for contract in test_contracts:
        print(f"\n代幣合約: {contract}")
        security_info = check_token_security(contract)
        
        for checker_name, result in security_info.items():
            status = result.get('status', '不通過')
            risks = ', '.join(result.get('risks', ['無風險']))
            print(f"{checker_name}: {status} {risks}")

if __name__ == "__main__":
    test_token_security()