
.PHONY: deps
deps:
	@pip3 install -r requirements/base.txt

.PHONY:test-env
test-env:
	@pip3 install -r requirements/test.txt

.PHONY:dev-env
dev-env: test-env
	@pip3 install -r requirements/dev.txt

.PHONY: test
test:
	@python -m unittest

.PHONY: coverage
coverage:
	@coverage run -m unittest discover
	@coverage report

.PHONY: lint
lint:
	@flake8 --config=.flake8.cfg .

.PHONY: docker-image
docker-image:
	@docker build -t wsm .

.PHONY: db-init
db-init:
	@docker run --rm -it -v "${CURDIR}/db:/db" \
	-e "PGPASSWORD=${DB_PASSWORD}" \
	postgres:11-alpine \
	psql -f /db/check_result.sql \
	-h "${PG_HOST}" \
	-p "${PG_PORT}" \
	-U "${PG_USER}" \
	-d "${DB_NAME}"
