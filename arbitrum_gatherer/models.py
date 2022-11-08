from typing import Any, Dict, Optional

from pydantic import BaseModel, PositiveInt, constr


class Block(BaseModel):
    number: int
    hash: str
    parent_hash: str
    nonce: str
    sha3_uncles: Optional[str] = None
    logs_bloom: str
    transactions_root: str
    state_root: str
    receipts_root: str
    miner: str
    difficulty: int
    total_difficulty: int
    size: int
    extra_data: str
    gas_limit: int
    gas_used: int
    timestamp: int
    transaction_count: int
    l1_block_number: Optional[str] = None
    mix_hash: str

    class Config:
        validate_assignment = True


class Transaction(BaseModel):
    hash: str
    nonce: int
    block_hash: str
    block_number: int
    transaction_index: int
    from_address: str
    to_address: Optional[str] = None
    value: int
    gas: int
    gas_price: int
    input: str
    block_timestamp: PositiveInt
    transaction_type: str
    r: str
    s: str
    v: int

    class Config:
        validate_assignment = True
