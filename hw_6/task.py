# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
# • Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
# • Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# • Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
#
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
from datetime import datetime
import random
from typing import List
import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, SecretStr
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128), unique=True),
                         sqlalchemy.Column("password", sqlalchemy.String(128)),
                         )

products = sqlalchemy.Table("products", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("name", sqlalchemy.String(32)),
                            sqlalchemy.Column("description", sqlalchemy.String(128)),
                            sqlalchemy.Column("price", sqlalchemy.Float(), ),
                            )

orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("users_id", sqlalchemy.ForeignKey('users.id')),
                          sqlalchemy.Column("products_id", sqlalchemy.ForeignKey('products.id')),
                          sqlalchemy.Column("date", sqlalchemy.String()),
                          sqlalchemy.Column("status", sqlalchemy.Boolean()),
                          )

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
metadata.create_all(engine)


class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=50, title='Name')
    surname: str = Field(min_length=1, max_length=50, title='Surname')
    email: EmailStr = Field(min_length=5, max_length=50, title='Email')
    password: SecretStr = Field(min_length=8, max_length=64, title='Password')


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    name: str = Field(max_length=100, title='Name')
    description: str | None = Field(max_length=1000, title='Description')
    price: float = Field(title='Price')


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    users_id: int = Field(title='User')
    products_id: int = Field(title='Product')
    date: str = Field(default=sqlalchemy.func.now(), title='Date', description="Order's date")
    status: bool = Field(default=0, title='Status', description="Order's status")


class Order(OrderIn):
    id: int


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def random_date():
    y = 2023
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return f'{y}-{m}-{d}'


@app.get("/fake_users/{count}")
async def create_fake_users(count: int):
    for i in range(1, count):
        query = users.insert().values(name=f'name_{i}'.capitalize(),
                                      surname=f'surname_{i}'.capitalize(),
                                      email=f'mail_{i}@mail.ru',
                                      password='change_me')
        await database.execute(query)
    return {'message': f'{count} fake users created'}


@app.get("/fake_products/{count}")
async def create_fake_products(count: int):
    for i in range(1, count):
        query = products.insert().values(name=f'sku_name_{i}'.capitalize(),
                                         description=f'sku_description_{i}'.capitalize(),
                                         price=i * 4.2)
        await database.execute(query)
    return {'message': f'{count} fake products created'}


@app.get("/fake_orders/{count}")
async def create_fake_orders(count: int):
    for i in range(1, count):
        query = orders.insert().values(users_id=i,
                                       products_id=i,
                                       date=datetime.strptime(f'{random_date()}', '%Y-%m-%d').date(),
                                       status=random.choice([True, False]))
        await database.execute(query)
    return {'message': f'{count} fake orders created'}


@app.get("/fake_database/{count}")
async def create_fake_database(count: int):
    await create_fake_users(count)
    await create_fake_products(count)
    await create_fake_orders(count)


@app.get('/')
async def index():
    return 'Welcome to marketplace APi'


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app.put('/users/{user_id}', response_model=User)
async def update_user(new_user: UserIn, user_id: int):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "Deleted successfully"}


# Product BLOCK
@app.get('/products/', response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get('/products/{product_id}', response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.post('/products/', response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@app.put('/products/{product_id}', response_model=Product)
async def update_product(new_product: ProductIn, product_id: int):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@app.delete('/products/{product_id}')
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Deleted successfully"}


# Orders BLOCK
@app.get('/orders/', response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get('/orders/{order_id}', response_model=Order)
async def read_product(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.put('/orders/{order_id}', response_model=Order)
async def update_order(new_order: OrderIn, order_id: int):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete('/orders/{order_id}')
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": "Deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("task:app", port=8000)
