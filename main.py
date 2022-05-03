#!/usr/bin/env python
import os
import json

def create_account(w3):
    account = w3.eth.account.create("how to create account eth")
    print("address", account._address)
    print("private_key", account._private_key)
    return account

def erc20_token(w3, address="0x7f45F13FAED6803b9a4CaB5dBF8E54EDDB73a752"):
    abi = '''[
        {"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},
        {"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
        {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
        {"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
        {"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},
        {"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
        {"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
        {"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
        {"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},
        {"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
        {"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
        {"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
        {"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},
        {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"}
    ]'''
    jtt = w3.eth.contract(address=address, abi=json.loads(abi))
    return jtt

if __name__ == '__main__':
    private_key = os.getenv('MASTER_PRIVATE_KEY', '')
    from web3 import Web3, EthereumTesterProvider, WebsocketProvider
    from web3.middleware import geth_poa_middleware
    provider_url = 'wss://rinkeby.infura.io/ws/v3/deecb0e96a594af4b541f39e86757cf0'
    provider = WebsocketProvider(provider_url)
    w3 = Web3(provider)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.isConnected())
    master_wallet = '0x39D7170f8f3553e392cE7b486c1f16Df69172bec'
    client_wallet = '0xA2307aAfDb75E52DbbAdf8cD94B63b9176ac4Ecb'
    master_private_key = ''
    print(w3.eth.get_balance(master_wallet))
    jtt = erc20_token(w3)
    print(jtt.functions.totalSupply().call())
    print(jtt.functions.name().call())
    print(jtt.functions.symbol().call())
    print(jtt.functions.decimals().call())
    print(jtt.functions.balanceOf(master_wallet).call())
    trans_meta = {
        'chainId': 4,
        'gas':70000,
        'nonce': w3.eth.getTransactionCount(master_wallet)
    }
    txn = jtt.functions.transfer(client_wallet, 0x01).buildTransaction(trans_meta)
    signed_txn = w3.eth.account.signTransaction(txn, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(master_wallet, jtt.functions.balanceOf(master_wallet).call())
    print(client_wallet, jtt.functions.balanceOf(client_wallet).call())
