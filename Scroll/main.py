from loguru import logger
import random

from modules.orbiter import OrbiterBridge
from modules.myaccount import Account
from help import send_list, send_message, sleeping_between_wallets, intro, outro
from settings import bot_status, count_modules, shuffle, orbiter_bridge, dozapravka_orbiter, from_chain, to_chain
from modules.spaseswap import SpaceSwap
from modules.deploy import DeployContract
from modules.skydrome import Skydrome
from modules.scrollswap import ScrollSwap
from modules.wrapether import WrapEtherScroll
from modules.layerbank import LayerBank

modules = [LayerBank, ScrollSwap, DeployContract, SpaceSwap, Skydrome, WrapEtherScroll]       # LayerBank, ScrollSwap, DeployContract, SpaceSwap, Skydrome, WrapEtherScroll



def main():
    with open('proxies.txt', 'r') as file:  # login:password@ip:port в файл proxy.txt
        proxies = [row.strip() for row in file]
    with open('wallets.txt', 'r') as file:
        wallets = [row.strip() for row in file]

    intro(wallets)
    count_wallets = len(wallets)

    if len(proxies) == 0:
        proxies = [None] * len(wallets)
    if len(proxies) != len(wallets):
        logger.error('Proxies count doesn\'t match wallets count. Add proxies or leave proxies file empty')
        return

    data = [(wallets[i], proxies[i]) for i in range(len(wallets))]

    if shuffle:
        random.shuffle(data)

    for idx, (private_key, proxy) in enumerate(data, start=1):


        account = Account(idx, private_key, proxy, "Scrolll")
        print(f'{idx}/{count_wallets} : {account.address}\n')
        send_list.append(f'{account.id}/{count_wallets} : [{account.address}]({"https://debank.com/profile/" + account.address})')
        random.shuffle(modules)

        try:
            balance = account.get_balance()
            if orbiter_bridge:
                send_list.append(OrbiterBridge(account.id, account.private_key, account.proxy, from_chain).bridge(from_chain=from_chain, to_chain=to_chain))

            if balance["balance"] < dozapravka_orbiter[1] and dozapravka_orbiter[0]:
                logger.info(f'Insufficient balance: {balance["balance"]} ETH, deposit with orbiter...')
                send_list.append(OrbiterBridge(account.id, account.private_key, account.proxy, from_chain).bridge(from_chain=from_chain, to_chain=to_chain))

            for count, module in enumerate(modules, start=1):
                if count_modules == count:
                    break
                send_list.append(module(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc="Scrolll").main())

        except Exception as e:
            logger.error(f'{idx}/{count_wallets} Failed: {str(e)}')
            sleeping_between_wallets()

        if bot_status == True:
            if account.id == count_wallets:
                send_list.append(f'\nSubscribe: https://t.me/CryptoMindYep')
            send_message(send_list)
            send_list.clear()

        if idx != count_wallets:
            sleeping_between_wallets()
            print()


    outro()
main()