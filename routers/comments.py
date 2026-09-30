from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from schemas import CommentCreate, CommentResponse, CommentWithTitleResponse
from repositories.tickets import get_ticket_from_db
from repositories.comments import create_comment_in_db, get_comments_from_db, get_comments_with_ticket_title_from_db


router = APIRouter(prefix="/tickets", tags=["Comments"])


@router.post("/{ticket_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(ticket_id: int, comment: CommentCreate):

    ticket = get_ticket_from_db(ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    created_at = datetime.now(timezone.utc).isoformat()

    comment_id = create_comment_in_db(
        ticket_id,
        comment.text,
        created_at
    )

    new_comment = {
        "id": comment_id,
        "ticket_id": ticket_id,
        "text": comment.text,
        "created_at": created_at
    }

    return new_comment



@router.get("/{ticket_id}/comments", response_model=list[CommentResponse])
def get_comments(ticket_id: int):

    ticket = get_ticket_from_db(ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
 
    comments = get_comments_from_db(ticket_id)

    return comments


@router.get("/{ticket_id}/comments-with-title", response_model=list[CommentWithTitleResponse])
def get_comments_with_title(ticket_id: int):

    ticket = get_ticket_from_db(ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    comments_with_title = get_comments_with_ticket_title_from_db(ticket_id)

    return comments_with_title