

# ===================================== options ===================================== #

#----main-options----#
count_modules = 8                                                   # кол-во модулей которые отработают из modules, т.е если в modules 5 модулей, то отработают рандомные 2 из 5
shuffle = True                                                      # True / False. если нужно перемешать кошельки

decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел
value_eth = [0.00001, 0.00006]                                      # минимальное и максимальное кол-во ETH для свапов и ликвы

delay_wallets = [10, 20]                                            # минимальная и максимальная задержка между кошельками
delay_transactions = [10, 15]                                       # минимальная и максимальная задержка между транзакциями
waiting_gas = 30                                                    # макс значение газа при котором будет работать скрипт
RETRY_COUNT = 2                                                     # кол-во попыток при возникновении ошибок

#------bot-options------#
bot_status = False                                                  # True / False
bot_token  = ''                                                     # telegram bot token
bot_id     = 0                                                      # telegram id

#----modules-options----#

supply_scrollswap = True                                            # True / False, при False будет работать только свап

supply_skydrome = True                                              # True / False, при False будет работать только свап

supply_spaceswap = True                                             # True / False, при False будет работать только свап

percent_for_lending = 0.8                                           # процент от баланса для лендинга LayerBank
withdraw_layerbank = True                                           # True / False, при False будет работать только сапплай
collateral_layerbank = True                                         # True / False, нужен для вывода

percent_for_wrap = 0.8                                              # процент от баланса для wrap eth

orbiter_bridge = False                                              # True / False
dozapravka_orbiter = [True, 0.0005]                                 # True / False, будет работать если баланс ниже этого числа
from_chain = 'Optimism'                                             # Optimism | zkSync | Scrolll
to_chain = 'Scrolll'                                                # Optimism | zkSync | Scrolll
value_for_bridge = [0.0063, 0.0075]                                 # минимальное и максимальное кол-во ETH для бриджа через Orbiter

# =================================== end-options =================================== #


