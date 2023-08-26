# * Создать веб-страницу для отображения списка пользователей.
#   Приложение должно использовать шаблонизатор Jinja для динамического формирования HTML страницы.
# * Создайте модуль приложения и настройте сервер и маршрутизацию.
# * Создайте класс User с полями id, name, email и password.
# * Создайте список users для хранения пользователей.
# * Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
#   содержать заголовок страницы, таблицу со списком пользователей и кнопку для
#   добавления нового пользователя.
# * Создайте маршрут для отображения списка пользователей (метод GET).
# * Реализуйте вывод списка пользователей через шаблонизатор Jinja.


from fastapi import FastAPI, Request
from fastapi import Form
import uvicorn
from pydantic import BaseModel, EmailStr, SecretStr
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

USERS = []


class User(BaseModel):
    id_: int
    name: str
    email: EmailStr
    password: SecretStr


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get('/users/', response_class=HTMLResponse)
async def all_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": USERS})


@app.get('/user/get_add/', response_class=HTMLResponse)
async def get_add_user(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@app.post('/user/post_add/', response_class=HTMLResponse)
async def post_add_user(request: Request, id_: int = Form(), name: str = Form(), email: EmailStr = Form(),
                        password: SecretStr = Form()):
    USERS.append(User(id_=id_, name=name, email=email, password=password))
    return templates.TemplateResponse("users.html", {"request": request, "users": USERS})


if __name__ == "__main__":
    uvicorn.run("task_6:app", port=8000, reload=True)
