import time
import random
from loguru import logger

from .myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI
from vars import spaceswap_abi
from settings import supply_scrollswap

send_list = ''
tokens = {
        "USDT": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "SF": "0x9DaeA97fd467d704c583BEdA2454e3DA27097b60",
    }

class ScrollSwap(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0xefeb222f8046aaa032c56290416c3192111c0085"), abi=spaceswap_abi)

    @check_gas
    @retry
    def swap(self):
        global send_list
        token = random.choice(list(tokens))

        balance_eth, balance_wei = self.get_value()
        tx_data = get_tx_data_withABI(self, balance_wei)
        deadline = int(time.time() + 10000)

        transaction = self.contract.functions.swapExactETHForTokens(0, [self.w3.to_checksum_address('0x5300000000000000000000000000000000000004'), self.w3.to_checksum_address(tokens[token])], self.address, deadline).build_transaction(tx_data)
        logger.info(f'ScrollSwap: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'ScrollSwap: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}: {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}ScrollSwap: Swap {"{:0.9f}".format(balance_eth)} ETH to {token} - success')
            return token

        else:
            logger.error(f'ScrollSwap: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}ScrollSwap: Swap {"{:0.9f}".format(balance_eth)} ETH to {token} - failed')


    @check_gas
    @retry
    def supply(self, token):
        global send_list
        if self.check_allowance(tokens[token], '0xefeb222f8046aaa032c56290416c3192111c0085') < 10:
            logger.info(f'ScrollSwap: try approve token {token}...')
            send_list += self.approve(115792089237316195423570985008687907853269984665640564039457584007913129639935, tokens[token], '0xefeb222f8046aaa032c56290416c3192111c0085')
            sleeping_between_transactions()

        balance_eth, balance_wei_eth = self.get_value()
        balance_eth = balance_eth * 0.001

        tx_data = get_tx_data_withABI(self, int(balance_wei_eth*0.001))
        deadline = int(time.time() + 10000)
        transaction = self.contract.functions.addLiquidityETH(self.w3.to_checksum_address(tokens[token]), int(balance_wei_eth * 0.001), 0, 0, self.address, deadline).build_transaction(tx_data)
        logger.info(f'ScrollSwap: Supply {"{:0.9f}".format(balance_eth)} ETH with {token}...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'ScrollSwap: Supply {"{:0.9f}".format(balance_eth)} ETH with {token} : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}ScrollSwap: Supply {"{:0.9f}".format(balance_eth)} ETH with {token} - success')

        else:
            logger.error(f'ScrollSwap: Supply {"{:0.9f}".format(balance_eth)} ETH with {token} : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}ScrollSwap: Supply {"{:0.9f}".format(balance_eth)} ETH with {token} - failed')

    def main(self):
        token = ScrollSwap.swap(self)
        sleeping_between_transactions()
        if supply_scrollswap:
            ScrollSwap.supply(self, token)
            sleeping_between_transactions()
        return send_list
