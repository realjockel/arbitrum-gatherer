import asyncio
import timeit
from typing import Any

import numpy
import pandas as pd
from aiohttp import ClientSession
from web3 import Web3
from web3.providers.base import JSONBaseProvider

from arbitrum_gatherer.config import NODE
from arbitrum_gatherer.models import Block, Transaction
from arbitrum_gatherer.utils import init_web3_client


# asynchronous JSON RPC API request
async def async_make_request(session: Any, url: Any, method: Any, params: Any):
    base_provider: JSONBaseProvider = JSONBaseProvider()
    request_data: bytes = base_provider.encode_rpc_request(method, params)
    async with session.post(
        url, data=request_data, headers={"Content-Type": "application/json"}
    ) as response:
        content = await response.read()
    response = base_provider.decode_rpc_response(content)
    return response


async def run(node_address: str, start_block: int, end_block: int) -> list:
    tasks: list = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for number in range(start_block, end_block + 1):
            task = asyncio.ensure_future(
                # run json rpc method eth_getBlocksByNumber and also return Transactions
                async_make_request(
                    session, node_address, "eth_getBlockByNumber", [hex(number), True]
                )
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses


# async method for 1000 blocks = 3.968s
def block_gatherer_async(start_block: int = 0, end_block: int = 100000) -> list[dict]:
    # @TODO needs more robustness and retries. If it fails, we have to rerun it from start, not good
    # measure execution time
    start_time: timeit = timeit.default_timer()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(NODE, start_block, end_block))

    loop.run_until_complete(future)

    print("async: {:.3f}s".format(timeit.default_timer() - start_time))
    print("Succesfully gathered all block and tx data")
    return future.result()


# sync method for 1000 blocks = > 30s
def block_gatherer_sync(start_block: int = 0, end_block: int = 100000) -> list[dict]:
    w3: Web3 = init_web3_client()

    start_time: timeit = timeit.default_timer()
    blocks: list = [w3.eth.get_block(block) for block in range(0, 100 + 1)]

    print(len(blocks))
    print("sync: {:.3f}s".format(timeit.default_timer() - start_time))
    return blocks


# we have results as a list of dicts (from future response), transform it to pydantic
# data object for validation in Future and easier handling
# @TODO implement validation in pydantic
# @TODO make it more robust
def convert_to_block_object(block_results: list[dict]) -> list[Block]:

    blocks = [
        Block(
            number=int(block["result"].get("number"), base=16),
            hash=block["result"].get("hash"),
            parent_hash=block["result"].get("parentHash"),
            nonce=block["result"].get("nonce"),
            sha3_uncles=block["result"].get("uncles")
            if len(block["result"].get("uncles")) > 0
            else None,
            logs_bloom=block["result"].get("logsBloom"),
            transactions_root=block["result"].get("transactionsRoot"),
            state_root=block["result"].get("stateRoot"),
            receipts_root=block["result"].get("receiptsRoot"),
            miner=block["result"].get("miner"),
            difficulty=int(block["result"].get("difficulty"), base=16),
            total_difficulty=int(block["result"].get("totalDifficulty"), base=16),
            size=int(block["result"].get("size"), base=16),
            extra_data=block["result"].get("extraData"),
            gas_limit=int(block["result"].get("gasLimit"), base=16),
            gas_used=int(block["result"].get("gasUsed"), base=16),
            timestamp=int(block["result"].get("timestamp"), base=16),
            transaction_count=len(block["result"].get("transactions")),
            l1_block_number=block["result"].get("l1BlockNumber"),
            mix_hash=block["result"].get("mixHash"),
        )
        for block in block_results
    ]
    print("Converted Blocks to Pydantic Block")
    return blocks


def convert_to_transaction_object(block_results: list[dict]) -> list[Transaction]:

    # nested list comprehension. Iterating through blocks that have a transaction list > 0 Then iterating through txs
    transactions = [
        [
            Transaction(
                hash=transaction.get("hash"),
                nonce=int(transaction.get("nonce"), base=16),
                block_hash=transaction.get("blockHash"),
                block_number=int(transaction.get("blockNumber"), base=16),
                transaction_index=int(transaction.get("transactionIndex"), base=16),
                from_address=transaction.get("from"),
                to_address=transaction.get("to"),
                value=int(transaction.get("value"), base=16),
                gas=int(transaction.get("gas"), base=16),
                gas_price=int(transaction.get("gasPrice"), base=16),
                input=transaction.get("input"),
                block_timestamp=int(block["result"].get("timestamp"), base=16),
                transaction_type=transaction.get("type"),
                r=transaction.get("r"),
                s=transaction.get("s"),
                v=int(transaction.get("v"), base=16),
            )
            for transaction in block["result"].get("transactions")
        ]
        for block in block_results
        if len(block["result"].get("transactions")) > 0
    ]
    # flatten list
    transactions = [item for sublist in transactions for item in sublist]
    print("Converted tx to Pydantic Transactions")

    return transactions


def create_dataframe_from_objects(block_results: list[dict]) -> tuple[pd.DataFrame]:
    # @TODO seperate logic,  not robust
    list_of_block_objects: list[Block] = convert_to_block_object(block_results)
    list_of_transaction_objects: list[Transaction] = convert_to_transaction_object(block_results)

    df_blocks: pd.DataFrame = pd.DataFrame([block.__dict__ for block in list_of_block_objects])
    df_transactions: pd.DataFrame = pd.DataFrame(
        [tx.__dict__ for tx in list_of_transaction_objects]
    )

    df_transactions.index = df_transactions.index.astype(str)
    df_blocks.index = df_blocks.index.astype(str)
    print("Created Dataframes")
    return df_blocks, df_transactions
