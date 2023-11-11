from loguru import logger

from .myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI
from vars import layerbank_abi, layerbank_abi2
from settings import percent_for_lending, collateral_layerbank, withdraw_layerbank

send_list = ''
class LayerBank(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0xec53c830f4444a8a56455c6836b5d2aa794289aa"), abi=layerbank_abi)

    @check_gas
    @retry
    def supply(self):
            global send_list
            balance_dict = self.get_balance()
            balance_wei = int(balance_dict["balance_wei"] * percent_for_lending)
            balance_eth = int(balance_dict["balance"] * percent_for_lending)
            tx_data = get_tx_data_withABI(self, balance_wei)
            transaction = self.contract.functions.supply(self.w3.to_checksum_address('0x274C3795dadfEbf562932992bF241ae087e0a98C'), balance_wei).build_transaction(tx_data)

            logger.info(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH - success')

            else:
                logger.error(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH - failed')

    @check_gas
    @retry
    def collateral(self):
        global send_list
        tx_data = get_tx_data_withABI(self)
        transaction = self.contract.functions.enterMarkets([self.w3.to_checksum_address('0x274C3795dadfEbf562932992bF241ae087e0a98C')]).build_transaction(tx_data)
        logger.info(f'LayerBank: Try enable collateral...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)
        if txstatus == 1:
            logger.success(f'LayerBank: Collateral enable : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}LayerBank: Collateral enable - success')
            return True

        else:
            logger.error(f'LayerBank: Collateral enable : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}LayerBank: Collateral enable - failed')

    @check_gas
    @retry
    def withdraw(self):
            global send_list
            tx_data = get_tx_data_withABI(self)
            contract = self.get_contract('0x274C3795dadfEbf562932992bF241ae087e0a98C', layerbank_abi2)
            value_in_wei = contract.functions.underlyingBalanceOf(self.address).call()
            value_in_eth = self.w3.from_wei(value_in_wei, 'ether')

            transaction = self.contract.functions.redeemUnderlying(self.w3.to_checksum_address('0x274C3795dadfEbf562932992bF241ae087e0a98C'), value_in_wei).build_transaction(tx_data)
            logger.info(f'LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH - success')
            else:
                logger.error(f'LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH - failed')

    def main(self):
        LayerBank.supply(self)
        sleeping_between_transactions()
        if collateral_layerbank:
            LayerBank.collateral(self)
            sleeping_between_transactions()
        if withdraw_layerbank:
            LayerBank.withdraw(self)
            sleeping_between_transactions()
        return send_list