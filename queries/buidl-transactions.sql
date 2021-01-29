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
	contracts.address = LOWER('0x7b123f53421b1bf8533339bfbdc7c98aa94163db') AND
	token_txns.block_number >= contracts.block_number
ORDER BY block_number ASC
