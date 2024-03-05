"""
○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
id товара (FOREIGN KEY), дата заказа и статус заказа.
"""

from datetime import date
from typing import List

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class UserIn(BaseModel):
    username: str = Field(min_length=2)
    lastname: str = Field(min_length=2)
    email: EmailStr = Field(max_length=128)
    password: str = Field(max_length=32)
    #order = relationship("Order", uselist=False, back_populates="Order")


class User(UserIn):
    id: int


class ItemIn(BaseModel):
    title: str = Field(min_length=2, max_length=32)
    description: str = Field(min_length=2, max_length=128)
    price: float = Field(min=0)


class Item(ItemIn):
    id: int
    #order = relationship("Order", uselist=False, back_populates="Order")


class OrderIn(BaseModel):
    order_date: date = Field()
    status: str = Field(max_length=128)
    user_id: int = Field(ForeignKey('user.id'))
    item_id: int = Field(ForeignKey('item.id'))


class Order(OrderIn):
    id: int
