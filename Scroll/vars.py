import json

with open('data/ABI_ERC20.json') as file:
    ERC20_ABI = json.load(file)
with open('data/spaceswap_abi.json') as file:
    spaceswap_abi = json.load(file)
with open('data/ABI_deploy.json') as file:
    deploy_abi = json.load(file)
with open('data/bytecode_deploy.txt') as file:
    bytecode_deploy = file.read()
with open('data/skydrome_abi.json') as file:
    skydrome_abi = file.read()
with open('data/layerbank_abi.json') as file:
    layerbank_abi = file.read()
with open('data/layerbank_abi2.json') as file:
    layerbank_abi2 = file.read()
with open('data/weth_abi.json') as file:
    weth_abi = file.read()


RPC = {
    'Ethereum': 'https://rpc.ankr.com/eth',
    'Optimism': 'https://rpc.ankr.com/optimism',
    'BSC': '',
    'Gnosis': '',
    'Polygon': '',
    'Fantom': '',
    'Arbitrum': 'https://rpc.ankr.com/arbitrum',
    'Avalanche': '',
    'zkSync': 'https://zksync-era.rpc.thirdweb.com',
    'zkEVM': 'https://rpc.ankr.com/polygon_zkevm',
    'Zora': '',
    'Scrolll': 'https://1rpc.io/scroll',
}

SCANS = {
    'Ethereum': 'https://etherscan.io/tx/',
    'Optimism': 'https://optimistic.etherscan.io/tx/',
    'BSC': 'https://bscscan.com/tx/',
    'Gnosis': 'https://gnosisscan.io/tx/',
    'Polygon': 'https://polygonscan.com/tx/',
    'Fantom': 'https://ftmscan.com/tx/',
    'Arbitrum': 'https://arbiscan.io/tx/',
    'Avalanche': 'https://snowtrace.io/tx/',
    'zkSync': 'https://explorer.zksync.io/tx/',
    'zkEVM': 'https://zkevm.polygonscan.com/tx/',
    'Zora': 'https://explorer.zora.energy/tx/',
    'Scrolll': 'https://scrollscan.com/tx/',
}

CHAIN_IDS = {
    'Ethereum': 1,
    'Optimism': 10,
    'BSC': 56,
    'Gnosis': 100,
    'Polygon': 137,
    'Fantom': 250,
    'Arbitrum': 42161,
    'Avalanche': 43114,
    'zkSync': 324,
    'zkEVM': 1101,
    'Zora': 7777777,
    'Scrolll': 534352,
}

CHAIN_NAMES = {
    1: 'Ethereum',
    10: 'Optimism',
    56: 'BSC',
    100: 'Gnosis',
    137: 'Polygon',
    250: 'Fantom',
    42161: 'Arbitrum',
    43114: 'Avalanche',
    1313161554: 'Aurora',
    324: 'zkSync',
    1101: 'zkEVM',
    7777777: 'Zora',
    534352: 'Scrolll',
}
