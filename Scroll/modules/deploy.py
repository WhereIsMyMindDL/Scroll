from loguru import logger

from .myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED
from vars import bytecode_deploy, deploy_abi

send_list = ''
class DeployContract(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)

    @check_gas
    @retry
    def deploy(self):
        global send_list
        contract = self.w3.eth.contract(abi=deploy_abi, bytecode=bytecode_deploy)
        transaction = contract.constructor().build_transaction({
            "from": self.address,
            "gasPrice": int(self.w3.eth.gas_price * 1.08),
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "value": 0,
            "gas": 0,
        })
        logger.info(f'DeployContract: Try deploy contract')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)
        if txstatus == 1:
            logger.success(f'DeployContract: Deploy contract: {self.scan + tx_hash}')
            send_list = (f'\n{SUCCESS}DeployContract: Deploy contract - success')

        else:
            logger.error(f'DeployContract: Deploy contract: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}DeployContract: Deploy contract - failed')

    def main(self):
        DeployContract.deploy(self)
        sleeping_between_transactions()
        return send_list