from common import get_holders
from json import dump


def main():
    
    tokens = {
        'buidl': '0x7b123f53421b1bF8533339BFBdc7C98aA94163db',
        'unifi': '0x9E78b8274e1D6a76a0dBbf90418894DF27cBCEb5'
    }

    date = '2021-01-31 16:20:00 UTC'

    reward = 10  # 10 GIL per holder
    decimals = 18  # GIL token has 18 decimals

    holders = set().union(*[set(get_holders(token_address, date).keys()) for token_address in tokens.values()])

    with open('./results/airdrop.json', 'w') as out:
        dump(dict.fromkeys(holders, hex(reward * 10 ** decimals)[2:]), out)
    

if __name__ == '__main__':
    main()
