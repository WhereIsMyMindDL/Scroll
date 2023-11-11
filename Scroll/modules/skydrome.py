from loguru import logger
import time
import random

from .myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI
from vars import skydrome_abi
from .wrapether import WrapEtherScroll
from settings import supply_skydrome

send_list = ''
tokens = {
    "USDT": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
    "DAI": "0xcA77eB3fEFe3725Dc33bccB54eDEFc3D9f764f97",
    "USDC": "0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4",
}

class Skydrome(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0xaa111c62cdeef205f70e6722d1e22274274ec12f"), abi=skydrome_abi)

    @check_gas
    @retry
    def swap(self):
        global send_list
        balance_eth, balance_wei = self.get_value()
        tx_data = get_tx_data_withABI(self, balance_wei)
        deadline = int(time.time() + 100000)
        token = random.choice(list(tokens))
        if token == "USDC":
            transaction = self.contract.functions.swapExactETHForTokens(0, [[self.w3.to_checksum_address('0x5300000000000000000000000000000000000004'), self.w3.to_checksum_address(tokens[token]), False]], self.address, deadline).build_transaction(tx_data)
        else:
            transaction = self.contract.functions.swapExactETHForTokens(0, [[self.w3.to_checksum_address('0x5300000000000000000000000000000000000004'), self.w3.to_checksum_address("0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4"), True], [self.w3.to_checksum_address('0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4'), self.w3.to_checksum_address(tokens[token]), True]], self.address, deadline).build_transaction(tx_data)

        logger.info(f'Skydrome: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'Skydrome: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}: {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}Skydrome: Swap {"{:0.9f}".format(balance_eth)} ETH to {token} - success')
            return token
        else:
            logger.error(f'Skydrome: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}Skydrome: Swap {"{:0.9f}".format(balance_eth)} ETH to {token} - failed')

    @check_gas
    @retry
    def supply(self, token):
        global send_list
        if self.check_allowance(tokens[token], '0xaa111c62cdeef205f70e6722d1e22274274ec12f') < 10:
            logger.info(f'Skydrome: try approve token {token}...')
            send_list += self.approve(115792089237316195423570985008687907853269984665640564039457584007913129639935,tokens[token], '0xaa111c62cdeef205f70e6722d1e22274274ec12f')
            sleeping_between_transactions()
        if self.check_allowance('0x5300000000000000000000000000000000000004', '0xaa111c62cdeef205f70e6722d1e22274274ec12f') < 10:
            logger.info(f'Skydrome: try approve token WETH...')
            send_list += self.approve(115792089237316195423570985008687907853269984665640564039457584007913129639935,'0x5300000000000000000000000000000000000004', '0xaa111c62cdeef205f70e6722d1e22274274ec12f')
            sleeping_between_transactions()

        balance_dict_weth = self.get_balance('0x5300000000000000000000000000000000000004')
        balance_dict_token = self.get_balance(tokens[token])

        tx_data = get_tx_data_withABI(self)
        deadline = int(time.time() + 10000)
        transaction = self.contract.functions.addLiquidity(self.w3.to_checksum_address(tokens[token]), self.w3.to_checksum_address('0x5300000000000000000000000000000000000004'), False, int(balance_dict_token["balance_wei"]*0.7), int(balance_dict_weth["balance_wei"]*0.7), 0, 0, self.address, deadline).build_transaction(tx_data)
        logger.info(f'Skydrome: Supply {"{:0.9f}".format(balance_dict_weth["balance"])} WETH')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'Skydrome: Supply {"{:0.9f}".format(balance_dict_weth["balance"])} WETH : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}Skydrome: Supply {"{:0.9f}".format(balance_dict_weth["balance"])} WETH - success')

        else:
            logger.error(f'Skydrome: Supply {"{:0.9f}".format(balance_dict_weth["balance"])} WETH : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}Skydrome: Supply {"{:0.9f}".format(balance_dict_weth["balance"])} WETH - failed')

    def main(self):
        token = Skydrome.swap(self)
        sleeping_between_transactions()
        if supply_skydrome:
            balance_eth, balance_wei = self.get_value()
            WrapEtherScroll(id=self.id, private_key=self.private_key, proxy=self.proxy, rpc="Scrolll").wrap(value_in_wei=balance_wei)
            time.sleep(20)
            Skydrome.supply(self, token)
            sleeping_between_transactions()
        return send_list
