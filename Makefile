install:
	pipenv install
release:
	pipenv run lint
	pipenv run test
	pipenv lock -r > requirements.txt
start:
	pipenv run start

.PHONY: install start release
