# wsm: Web Site Monitor

## Prerequisites
 - `docker`
 - `make`
 - `python 3.5`

## Notes 
I've chosen to use docker as a unit of deployment. Just to build and run
the app in a container only `docker` and `make` will be enough.

`Makefile` is an entry point for all automations and major operations. It contains self-descriptive semantic targets.

## Testing
```bash
# run once to install all necessary dependencies to run tests
make test-env

make test  # runs all the tests

make coverage  # generates and prints coverage report
```

## Run

### Fully locally (aka dev env)
```bash
$ make docker-image
$ docker-compose up

# in another shell
$ make dev-check

# in another shell
$ make dev-consume
```

### Prod
1. Make sure there is a `ssl` subdirectory in the current dir and it contains valid kafka ssl certificates
2. `cfg.prod.json` points to the right kafka and db instances

```bash
$ docker run --rm -it -v $(pwd)/ssl:/ssl wsm --config=cfg.prod.json check

# in another shell
$ docker run --rm -it -v $(pwd)/ssl:/ssl -e 'DB_PASSWORD=<PASSORD>' wsm --config=cfg.prod.json consume
```
