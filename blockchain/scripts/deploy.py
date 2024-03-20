from brownie import Articles, accounts

def main():
    token = Articles.deploy({'from': accounts[0]})
    # print(token.sa)