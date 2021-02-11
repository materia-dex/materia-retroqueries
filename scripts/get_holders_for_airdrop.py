from common import get_holders
from json import dump


def main():
    
    tokens = {
        'buidl': '0x7b123f53421b1bF8533339BFBdc7C98aA94163db',
        'unifi': '0x9E78b8274e1D6a76a0dBbf90418894DF27cBCEb5',
        'arte': '0x34612903Db071e888a4dADcaA416d3EE263a87b9',
        'usd': '0x44086035439E676c02D411880FcCb9837CE37c57'
    }

    date = '2021-01-31 04:20:00 UTC'

    reward = 99  # 10 GIL per holder
    decimals = 18  # GIL token has 18 decimals

    holders = set().union(*[set(get_holders(token_address, date).keys()) for token_address in tokens.values()])

    with open('./results/airdrop.json', 'w') as out:
        dump(dict.fromkeys(holders, hex(reward * 10 ** decimals)[2:]), out)
    

if __name__ == '__main__':
    main()
