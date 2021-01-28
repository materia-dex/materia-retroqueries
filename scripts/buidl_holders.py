from google.cloud import bigquery
from datetime import datetime, timezone

client = bigquery.Client()
query = open('./queries/buidl-transactions.sql', 'r').read()

result = client.query(query)

holders = {}
at_time = datetime(2021, 1, 28, 16, 20, 00, 000, tzinfo=timezone.utc)

for row in filter(lambda row: row['block_timestamp'] <= at_time, result):
    src, dst, val = row['from_address'], row['to_address'], int(row['value'])
    
    if src in holders:
        holders[src] -= val
    if dst in holders:
        holders[dst] += val
    else:
        holders[dst] = val

print(holders)
