from web3 import HTTPProvider, Web3

from arbitrum_gatherer.config import NODE


def init_web3_client() -> Web3:
    w3: Web3 = Web3(HTTPProvider(NODE))
    return w3
