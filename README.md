# Borrower API

## Install

```shell
pip install -r src/requirements.txt
```

For init database, in addition

```shell
pip install -r init/requirements.txt
```

## Init database

```shell
python init/create_and_load.py
```

# Run api

```shell
cd src
```

For dev

```shell
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

go to 

http://localhost:8000/docs


