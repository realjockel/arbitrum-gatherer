# Arbitrum Data Gatherer

End-to-End pipeline to load Arbitrum **blocks** and **transactions** to _Clickhouse_ Database.
This Pipeline gathers blocks and transactions up until the 100.000 Blockon Arbitrum. Async calls
were used because it decreases the run time by 10x. (1000 Blocks sync = 30s, 1000 Blocks asnc = 3s).

Raw JSON-RPC calls were used to collect transactions and blocks with one method `eth_getBlockByNumber)`.
This method allows to export block data and transaction bodies in one call. See https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_getblockbynumber

There is a lot to be improved. Listed in "What's Missing" below.

**Caution: Running the script truncates the table in clickhouse and refills it with the data**

## Prerequisites

To use this, please install:

1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Github account](https://github.com/)
3. [Docker](https://docs.docker.com/engine/install/)

### Setup

- Clone the GitHub repository.
- Rename `.env-example` to `.env` and replace placeholder variables with connection details
- If run locally install `poetry` , then run `poetry install` and then `poetry run main.py`
- You can also run `run.sh` to run tests and code formatting (dont forget to chmod)

- Else Run Docker Container:
- `docker build --tag arbitrum-gatherer .`
- `docker run arbitrum-gatherer`

## What's missing?

- Describted as @TODO tags in source code but:
- Secure storage of keys in vault
- CI/CD
- Tests
- Robustness
- Decoded Data
- Orchestration
- Logging
- Some Fields ( tried to follow the schema as much as possible which didnt specify fields such as 'r' , 's','v') -> but can be added at a later stage, intermediate data model includes those fields
