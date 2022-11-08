from arbitrum_gatherer.services import block_gatherer_async, block_gatherer_sync


def test_block_gatherer_sync():
    blocks = block_gatherer_sync(start_block=0, end_block=2)
    assert len(blocks) == 2


def test_block_gatherer_async():
    blocks = block_gatherer_async(start_block=0, end_block=100)
    assert len(blocks) == 100
