from fastapi import FastAPI
from routers.tickets import router as tickets_router
from routers.comments import router as comments_router
from models import Base
from database_orm import engine


app = FastAPI()

app.include_router(tickets_router)
app.include_router(comments_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Support Ticket API"}

