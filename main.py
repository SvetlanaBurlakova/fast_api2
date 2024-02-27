"""
Создать API для добавления нового пользователя в базу данных. Приложение должно иметь возможность принимать
POST запросы с данными нового пользователя и сохранять их в базу данных.
Создайте модуль приложения и настройте сервер и маршрутизацию. Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей. Создайте маршрут для добавления нового пользователя (метод POST).
Реализуйте валидацию данных запроса и ответа.
Создать API для обновления информации о пользователе в базе данных. Приложение должно иметь возможность принимать
PUT запросы с данными пользователей и обновлять их в базе данных.
Создайте модуль приложения и настройте сервер и маршрутизацию. Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей. Создайте маршрут для обновления информации о пользователе (метод PUT).
Реализуйте валидацию данных запроса и ответа.
Создать API для удаления информации о пользователе из базы данных. Приложение должно иметь возможность принимать
DELETE запросы и удалять информацию о пользователе из базы данных.
Создайте модуль приложения и настройте сервер и маршрутизацию. Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей. Создайте маршрут для удаления информации о пользователе (метод DELETE).
Реализуйте проверку наличия пользователя в списке и удаление его из списка.
Создать веб-страницу для отображения списка пользователей. Приложение должно использовать шаблонизатор Jinja для
динамического формирования HTML страницы.
Создайте модуль приложения и настройте сервер и маршрутизацию.Создайте HTML шаблон для отображения списка пользователей.
Шаблон должен содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Создайте маршрут для отображения списка пользователей (метод GET).
Реализуйте вывод списка пользователей через шаблонизатор Jinja
"""
from random import choice

from fastapi import FastAPI, Request
from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import jinja2




app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []

users.append(User(id=1, name='Alex', email='alex@mail.ru', password='password1'))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request":request, "users": users})


@app.post("/user/")
async def add_user(new_user: User):
    for user in users:
        if user.id == new_user.id:
            return {"message": "Пользователь с таким ID уже существет"}
        if user.email == new_user.email:
            return {"message": "Пользователь с таким Email уже существет"}
    users.append(new_user)
    return users


@app.put("/user/{user_id}")
async def change_user(user_id: int, new_user: User):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = new_user
            return users
    return {"message": "Пользователя с таким ID не существует"}


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return users
    return {"message": "Пользователь не найден"}

