from fastapi import FastAPI, HTTPException

app = FastAPI(title="Noor Foods API")
ORDERS = {
    "A101": {
        "id": "A101",
        "customer": "Noor Foods",
        "total": 4500,
        "status": "pending",
    },
    "A102": {
        "id": "A102",
        "customer": "Bilal Traders",
        "total": 12800,
        "status": "delivered",
    },
    "A103": {
        "id": "A103",
        "customer": "Karachi Crafts",
        "total": 2300,
        "status": "pending",
    },
}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods Orders API", "doc": "/docs"}


@app.get("/orders")
def list_orders() -> list[dict]:
    # return list(ORDERS.values())
    return list(ORDERS.values())


@app.get("/orders/{order_id}")
def get_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return ORDERS[order_id]


@app.get("/orders_one")
def list_orders_one(limit: int = 1) -> list[dict]:  # the argument here is limit = 3
    return list(ORDERS.values())[:limit]
