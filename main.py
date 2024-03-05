"""
Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
содержать информацию о доступных товарах, их описаниях и ценах. Таблица
пользователи должна содержать информацию о зарегистрированных
пользователях магазина. Таблица заказы должна содержать информацию о
заказах, сделанных пользователями.
○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
имя, фамилия, адрес электронной почты и пароль.
○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
название, описание и цена.
○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
заказа.
Создайте модели pydantic для получения новых данных и
возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через
создание маршрутов, REST API (итого 15 маршрутов).
○ Чтение всех
○ Чтение одного
○ Запись
○ Изменение
○ Удаление
"""
import random
from datetime import datetime
from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from model import UserIn, User, Item, ItemIn, Order, OrderIn
import aiosqlite
from faker import Faker


DATABASE_URL = "sqlite:///mydatabase.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String(32)),
    sqlalchemy.Column("lastname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(32))
)
items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.Float)
)
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("item_id", sqlalchemy.Integer, ForeignKey("items.id"), nullable=False),
    sqlalchemy.Column("order_date", sqlalchemy.Date),
    sqlalchemy.Column("status", sqlalchemy.String(128))
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(username=user.username, lastname=user.lastname, email=user.email,
                                  password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.post("/items/", response_model=Item)
async def create_item(item: ItemIn):
    query = items.insert().values(title=item.title, description=item.description, price=item.price)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id, item_id=order.item_id, order_date=order.order_date,
                                   status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.post("/fake_users/{count}")
async def create_fake_users(count: int):
    for i in range(count):
        query = users.insert().values(username=f'username{i}', lastname=f'lastname{i}', email=f'lastname{i}@mail.com',
                                      password=f'password{i}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.post("/fake_items/{count}")
async def create_fake_items(count: int):
    for i in range(count):
        query = items.insert().values(title=f'title{i}', description=f'description{i}', price=random.random()*100)
        await database.execute(query)
    return {'message': f'{count} fake items create'}



@app.post("/fake_orders/{count}")
async def create_fake_orders(count: int):
    for i in range(count):
        query = orders.insert().values(user_id=random.randint(1, count), item_id=random.randint(1, count),
                                       order_date=datetime.now(), status=f'status{i}')
        await database.execute(query)
    return {'message': f'{count} fake orders create'}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/items/", response_model=List[Item])
async def read_items():
    query = items.select()
    return await database.fetch_all(query)


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.get("/items/{item_id}", response_model=Item)
async def read_user(item_id: int):
    query = items.select().where(items.c.id == item_id)
    return await database.fetch_one(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, new_item: ItemIn):
    query = items.update().where(items.c.id == item_id).values(**new_item.dict())
    await database.execute(query)
    return {**new_item.dict(), "id": item_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_item(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {'message': 'Item deleted'}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}


if __name__ == '__main__':
    uvicorn.run(app)
