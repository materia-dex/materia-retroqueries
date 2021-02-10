from web3 import Web3
from os.path import dirname, join
from common import get_holders

def main():
    date = '2200-12-25 15:30:00 UTC'
    holders = get_holders('0x7b123f53421b1bF8533339BFBdc7C98aA94163db', date)

    totalSupply = 0
    for holder in holders.values():
        totalSupply += holder

    print(f'Total supply: {totalSupply}\nNumber of holders: {len(holders)}')

    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1e9a0aeccdd6442093827b1cb6091681'))
    buidl = w3.eth.contract(abi=open(join(dirname(__file__), './common/IERC20.json'), 'r').read(), address=Web3.toChecksumAddress('0x7b123f53421b1bF8533339BFBdc7C98aA94163db'))

    errors = 0
    for i, (wallet, amount) in enumerate(holders.items()):
        print(f'{i} - Checking current amount for {wallet}: {amount}')
        if (balance := buidl.functions.balanceOf(Web3.toChecksumAddress(wallet)).call()) != amount:
            print(f'Inconsitence, should be: {balance}')
            errors += 1

    print(f'Errors: {errors}/{len(holders)}')

if __name__ == '__main__':
    main()
