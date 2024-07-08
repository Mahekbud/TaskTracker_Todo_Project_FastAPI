from fastapi import FastAPI
from src.routers.User import Users
from src.routers.Todo import Todos
from src.routers.Category import categories
from src.routers.Notification import Notifications

app = FastAPI(title="Todos_detail")


app.include_router(Users)
app.include_router(Todos)
app.include_router(categories)
app.include_router(Notifications)
