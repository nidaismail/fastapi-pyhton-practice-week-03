from fastapi import FastAPI

app = FastAPI(title="Noor Foods Orders API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods Orders API", "doc": "/doc"}


# Practice: your first routes
# Practice Task 1 -  A health check
@app.get("/health")
def health_code() -> dict[str, str]:
    return {"status": "OK"}


# Practice Task 2 - A list
@app.get("/products")
def noor_products() -> list[dict]:
    return [
        {"name": "Product 1", "price": 200},
        {"name": "Product 2", "price": 201},
        {"name": "Product 3", "price": 202},
    ]


# the return type is list of dicts
# the docs will show endpoinsts and its schema


# Practice Task 3 - Break it

# TypeError: Failed to execute 'fetch' on 'Window': Failed to parse URL from http://127.0.0.1:8000health
# {"detail":"Not Found"}
# @app.get("health")
# def health_code() -> dict[str, str]:
#     return {"status": "OK"}
