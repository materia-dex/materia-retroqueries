from google.cloud import bigquery
from datetime import datetime, timezone
from web3 import Web3

client = bigquery.Client()
query = open('./queries/buidl-transactions.sql', 'r').read()

result = client.query(query)

holders = {}
at_time = datetime(2021, 7, 8, 7, 0, 0, 00, tzinfo=timezone.utc)

zero_address = '0x0000000000000000000000000000000000000000'

for row in filter(lambda row: row['block_timestamp'] <= at_time, result):
    src, dst, val = row['from_address'], row['to_address'], int(row['value'])
   
    if not src in holders: holders[src] = 0
    if not dst in holders: holders[dst] = 0
    if dst != zero_address: holders[dst] += val
    if src != zero_address: holders[src] -= val

holders = {wallet: amount for wallet, amount in holders.items() if amount > 0}
holders = dict(sorted(holders.items(), key=lambda item: item[1], reverse=True))

totalSupply = 0
for holder in holders.values():
    totalSupply += holder

print(f'Total supply: {totalSupply}\nNumber of holders: {len(holders)}')

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1e9a0aeccdd6442093827b1cb6091681'))
buidl = w3.eth.contract(abi=open('./scripts/IERC20.json', 'r').read(), address=Web3.toChecksumAddress('0x7b123f53421b1bF8533339BFBdc7C98aA94163db'))

errors = 0
for i, (wallet, amount) in enumerate(holders.items()):
    print(f'{i} - Checking current amount for {wallet}: {amount}')
    if (balance := buidl.functions.balanceOf(Web3.toChecksumAddress(wallet)).call()) != amount:
        print(f'Inconsitence, should be: {balance}')
        errors += 1

print(f'Errors: {errors}/{len(holders)}')
