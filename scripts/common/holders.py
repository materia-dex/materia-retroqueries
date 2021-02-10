from google.cloud import bigquery

client = bigquery.Client()

def get_holders(token_address, date):

    query = f'''
    SELECT
            from_address,
            to_address,
            value,
            transaction_hash,
            token_txns.block_number,
            token_txns.block_timestamp
    FROM
            `bigquery-public-data.crypto_ethereum.token_transfers` AS token_txns
    JOIN
            `bigquery-public-data.crypto_ethereum.contracts` AS contracts
    ON
            (contracts.address = token_txns.token_address)
    WHERE
            contracts.address = LOWER('{token_address}') AND
            token_txns.block_number >= contracts.block_number AND
            token_txns.block_timestamp <= '{date}'
    ORDER BY block_number ASC
    '''

    holders = {}
    zero_address = '0x0000000000000000000000000000000000000000'

    for row in client.query(query):
        src, dst, val = row['from_address'], row['to_address'], int(row['value'])

        if not src in holders: holders[src] = 0
        if not dst in holders: holders[dst] = 0
        if dst != zero_address: holders[dst] += val
        if src != zero_address: holders[src] -= val

    holders = {wallet: amount for wallet, amount in holders.items() if amount > 0}
    holders = dict(sorted(holders.items(), key=lambda item: item[1], reverse=True))

    return holders
