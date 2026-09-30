from fastapi import FastAPI
from routers.tickets import router as tickets_router
from routers.comments import router as comments_router
from database import setup_database


app = FastAPI()

app.include_router(tickets_router)
app.include_router(comments_router)

setup_database()


@app.get("/")
def read_root():
    return {"message": "Support Ticket API"}

