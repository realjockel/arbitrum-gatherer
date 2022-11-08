echo RUNNING MYPY
poetry run mypy ./arbitrum_gatherer 
echo RUNNING flake8
poetry run flake8
echo RUNNING isort
poetry run isort ./arbitrum_gatherer
echo RUNNING black
poetry run black ./arbitrum_gatherer
echo RUNNING PYTEST with COVERAGE
poetry run pytest --cov --cov-fail-under=60