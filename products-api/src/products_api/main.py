from enum import Enum

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

# We use status to specify HTTP response codes using readable constants.


class Category(str, Enum):
    rice = "rice"
    oil = "oil"
    spices = "spices"
    flour = "flour"


# create New Product
# base Model is coming from pydantic
# It tells the structure and validation for incoming data
class NewProduct(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(gt=0)
    category: Category  # enum is doing category validation
    in_stock: int = Field(
        default=0, ge=0
    )  # If the client doesn't send in_stock, ge=0 ge means: greater than or equal to


class Product(NewProduct):
    id: str


# Every field is optional. Because PATCH means: Change only the fields the client sends.
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    price: int | None = Field(default=None, gt=0)
    category: Category | None = None
    in_stock: int | None = Field(default=None, ge=0)


# If the client sends invalid data, it doesn't reach your business logic. That's one of the major reasons FastAPI + Pydantic is useful.
products: dict[str, Product] = {
    "P101": Product(
        id="P101",
        name="Basmati rice 5kg",
        price=2400,
        category=Category.rice,
        in_stock=40,
    ),
    "P102": Product(
        id="P102",
        name="Cooking oil 1L",
        price=650,
        category=Category.oil,
        in_stock=0,
    ),
    "P103": Product(
        id="P103",
        name="Red chilli powder 200g",
        price=320,
        category=Category.spices,
        in_stock=120,
    ),
    "P104": Product(
        id="P104",
        name="Sella rice 10kg",
        price=4600,
        category=Category.rice,
        in_stock=15,
    ),
}
next_product_id = 105
app = FastAPI(title="Noor Foods Products API")


@app.get("/")
def root():
    return {"message": "Welcome to Noor Foods Products API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/products")
def list_products(
    category: Category | None = None,
    max_price: int | None = Query(default=None, gt=0),
    limit: int = Query(default=10, gt=0),
) -> list[Product]:
    result = list(products.values())

    if category is not None:
        result = [product for product in result if product.category == category]

    if max_price is not None:
        result = [product for product in result if product.price <= max_price]

    return result[:limit]


def find_product(product_id: str) -> Product:
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found",
        )

    return product  # Converts the dictionary into a Pydantic object.


@app.get("/products/{product_id}")
def get_product(product_id: str) -> Product:
    return find_product(product_id)


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(new_product: NewProduct) -> Product:
    global next_product_id  # This tells Python that we want to update the counter defined outside this function

    product_id = f"P{next_product_id}"  # Generate ID

    product = Product(
        id=product_id,
        **new_product.model_dump(),
    )
    # ** unpacks the dictionary into keyword arguments.
    # model_dump() converts the Pydantic NewProduct object into a dictionary

    products[product_id] = product

    next_product_id += 1

    return product


@app.patch("/products/{product_id}")
def update_product(
    product_id: str,
    product_update: ProductUpdate,
) -> Product:

    product = find_product(product_id)

    update_data = product_update.model_dump(
        exclude_unset=True
    )  # means: include only fields that the client actually provided.

    updated_product = product.model_copy(
        update=update_data
    )  # creates a copy of the existing Pydantic object with the supplied fields changed

    products[product_id] = updated_product

    return updated_product


# model_dump()	Converts Pydantic object into a dictionary
# model_copy()	Creates a copy of a Pydantic object
# model_copy(update={...})	Creates a copy with selected fields changed
@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(product_id: str) -> None:

    product = find_product(product_id)

    if product.in_stock > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete {product_id}: stock is available",
        )

    del products[product_id]

    return None