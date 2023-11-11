from loguru import logger

from .myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI
from vars import weth_abi
from settings import percent_for_wrap

send_list = ''
class WrapEtherScroll(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0x5300000000000000000000000000000000000004"), abi=weth_abi)

    @check_gas
    @retry
    def wrap(self, value_in_wei=None):
        global send_list
        if value_in_wei == None:
            balance_dict = self.get_balance()
            value_in_wei = int(balance_dict["balance_wei"] * percent_for_wrap)

        balance_eth = self.w3.from_wei(value_in_wei, 'ether')
        tx_data = get_tx_data_withABI(self, value_in_wei)
        transaction = self.contract.functions.deposit().build_transaction(tx_data)

        logger.info(f'WrapEther: Wrap {"{:0.9f}".format(balance_eth)} ETH')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'WrapEther: Wrap {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}WrapEther: Wrap {"{:0.9f}".format(balance_eth)} ETH - success')

        else:
            logger.error(f'WrapEther: Wrap {"{:0.9f}".format(balance_eth)} ETH: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}WrapEther: Wrap {"{:0.9f}".format(balance_eth)} ETH - failed')

    @check_gas
    @retry
    def unwrap(self):
        global send_list
        value_in_wei = self.contract.functions.balanceOf(self.address).call()
        value_in_eth = self.w3.from_wei(value_in_wei, 'ether')
        tx_data = get_tx_data_withABI(self)
        transaction = self.contract.functions.withdraw(value_in_wei).build_transaction(tx_data)

        logger.info(f'WrapEther: unwrap {"{:0.9f}".format(value_in_eth)} ETH')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'WrapEther: unwrap {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}WrapEther: unwrap {"{:0.9f}".format(value_in_eth)} ETH - success')

        else:
            logger.error(f'WrapEther: unwrap {"{:0.9f}".format(value_in_eth)} ETH: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}WrapEther: unwrap {"{:0.9f}".format(value_in_eth)} ETH - failed')

    def main(self):
        WrapEtherScroll.wrap(self)
        sleeping_between_transactions()
        WrapEtherScroll.unwrap(self)
        sleeping_between_transactions()
        return send_list
