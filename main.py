import arbitrum_gatherer.database as db
from arbitrum_gatherer.services import (
    block_gatherer_async,
    create_dataframe_from_objects,
)

if __name__ == "__main__":

    # create tables if not existing
    db.create_transaction_table()
    db.create_block_table()

    # let's truncate the table in each run
    # Caution: Not good...
    # @TODO: Remove the truncate and allow specifying it via arguments/env file
    db.truncate_tables("blocks_raw")
    db.truncate_tables("transactions_raw")

    # conerts pydantic intermediate data model to dataframe
    # @TODO dangerous to run it in one batch... not robust.
    blocks = block_gatherer_async(start_block=0, end_block=100000)
    df_blocks, df_transactions = create_dataframe_from_objects(blocks)

    # insert dataframes to table
    db.insert_into_table(df=df_blocks, table="blocks_raw")
    db.insert_into_table(df=df_transactions, table="transactions_raw")
