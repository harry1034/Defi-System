import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    usdc_contract = Contract('0x96Eaf2cc9fD7f4693d8287F6531234ddd220fEef')
    defi_contract = Contract('0xBA237c88271e30989784528db033b157996e3FdF')
    
    print(f"Before function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")
    usdc_contract.approve(defi_contract, 10000, {"from": account})
    defi_contract.depositToken(10000, {"from": account})

    print(f"After function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")
    
    defi_contract.withdraw(100, {"from": account})
    

    print(f"Current balance after Withdraw usdc token deposit balance is {defi_contract.depositBalance(account)}")
