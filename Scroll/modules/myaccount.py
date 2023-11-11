import time
from help import sign_and_send_transaction, SUCCESS, FAILED, get_tx_data_withABI
from loguru import logger
from vars import RPC, SCANS, CHAIN_NAMES, ERC20_ABI
from web3 import Web3
import random
from settings import value_eth, decimal_places

send_list = ''
class Account:
    def __init__(self, id, private_key, proxy, rpc):
        self.private_key = private_key
        self.proxy = proxy
        self.id = id

        if self.proxy != None:
            self.w3 = Web3(Web3.HTTPProvider(RPC[rpc], request_kwargs={"proxies": {'https': "http://" + self.proxy, 'http': "http://" + self.proxy}}))

        self.w3 = Web3(Web3.HTTPProvider(RPC[rpc]))
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address
        self.scan = SCANS[CHAIN_NAMES[self.w3.eth.chain_id]]

    def wait_balance(self, value, rpc):
        x = 0
        self.w3 = Web3(Web3.HTTPProvider(RPC[rpc]))
        while x < 4:
            balance = self.get_balance()
            if balance["balance_wei"] >= value * 0.8:
                logger.info(f'Balance: {balance["balance"]} {balance["symbol"]}')
                print()
                return True
            else:
                logger.info(f'Balance: {balance["balance"]} {balance["symbol"]} wait deposit...')
                time.sleep(45)
                x += 1
        return False

    def get_value(self):
        balance_eth = round(random.uniform(value_eth[0], value_eth[1]), decimal_places)
        balance_wei = int(self.w3.to_wei(balance_eth, 'ether'))
        return balance_eth, balance_wei

    def get_contract(self, contract_address, abi=None):
        contract_address = Web3.to_checksum_address(contract_address)

        if abi is None:
            abi = ERC20_ABI

        contract = self.w3.eth.contract(address=contract_address, abi=abi)

        return contract

    def get_balance(self, contract_address: str = 'native'):
        if contract_address == 'native':
            balance_wei = self.w3.eth.get_balance(self.address)
            balance_eth = balance_wei / 10 ** 18
            return {"balance_wei": balance_wei, "balance": balance_eth, "symbol": 'ETH', "decimal": 18}

        contract_address = Web3.to_checksum_address(contract_address)
        contract = self.get_contract(contract_address)

        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(self.address).call()

        balance = balance_wei / 10 ** decimal

        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    def check_allowance(self, token_address, contract_address):
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = contract.functions.allowance(self.address, contract_address).call()

        return amount_approved

    def approve(self, amount, token_address, contract_address):
        global send_list
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)

        allowance_amount = self.check_allowance(token_address, contract_address)

        if amount > allowance_amount or amount == 0:

            approve_amount = 2 ** 128

            tx_data = get_tx_data_withABI(self)

            transaction = contract.functions.approve(
                contract_address,
                approve_amount
            ).build_transaction(tx_data)

            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            balance_dict = Account.get_balance(self, token_address)
            if txstatus == 1:
                logger.success(f'Token: Approve {approve_amount} {balance_dict["symbol"]} : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}Token: Approve {approve_amount} {balance_dict["symbol"]} - success')
                return send_list

            else:
                logger.error(f'Token: Approve {approve_amount} {balance_dict["symbol"]} : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}Token: Approve {approve_amount} {balance_dict["symbol"]} - failed')
                return send_list
