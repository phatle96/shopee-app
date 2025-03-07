## How to run the source

- Create .env file from .env-example with your credentials

- Create a Python virtual environment by using UV package
```sh
uv venv
```

- Enable uv virtual environment
```sh
source .venv/bin/activate
```

- Install dependency
```sh
uv pip install -r requirements.txt
```

- Start API server
```sh
sh start-api.sh
```