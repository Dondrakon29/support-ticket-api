from pydantic import BaseModel, Field
from typing import Literal

class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    priority: Literal["low", "medium", "high"]


class TicketStatusUpdate(BaseModel):
    status: Literal["open", "in_progress", "closed"]


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class TicketResponse(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    status: Literal["open", "in_progress", "closed"]
    priority: Literal["low", "medium", "high"]
    created_at: str
    closed_at: str | None = None      


class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    text: str
    created_at: str


class CommentWithTitleResponse(BaseModel):
    comment_id: int
    text: str
    created_at: str
    ticket_title: str