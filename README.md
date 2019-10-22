# supertyper

Uni programming project

## Getting started

1. Install `pipenv`.

```bash
$ pip install pipenv
```

2. Install dependencies (Choose either commands).

```bash
# Install default dependencies
$ pipenv install

# Or install default + dev dependencies
$ pipenv install --dev
```

3. Start `pipenv` shell to isolate the environment and load the required dependencies.

```bash
$ pipenv shell
```

4. Once the shell is started, run `reqtexts.py` to retreive paragraphs to be typed.

```bash
(supertyper-hash) $ py reqtexts.py
```

5. Finally, run `__main__.py` to start game.

```bash
(supertyper-hash) $ py __main__.py
```

## Development

The project uses `pylint` for linting and `autopep8` for formatting.

## License

MIT
