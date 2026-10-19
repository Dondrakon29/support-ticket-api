from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from database_orm import get_db
import logging
from typing import Literal
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas import CommentCreate, CommentResponse, CommentWithTitleResponse, CommentUpdate, TicketCommentCountResponse, CommentListResponse
from repositories.tickets_orm import get_ticket_orm
from repositories.comments_orm import (
    get_comments_orm, 
    create_comment_orm, 
    get_comments_with_title_orm, 
    get_comment_orm, delete_comment_orm, 
    update_comment_orm,
    get_comments_count_orm)


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/tickets", tags=["Comments"])


@router.post("/{ticket_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(ticket_id: int, comment: CommentCreate, db: Session = Depends(get_db)):

    ticket = get_ticket_orm(db, ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    created_at = datetime.now(timezone.utc).isoformat()

    try:
        new_comment = create_comment_orm(
            db,
            ticket_id,
            comment.text,
            created_at
        )

    except SQLAlchemyError:
        logger.exception("Database error while creating comment")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    return new_comment


@router.get("/{ticket_id}/comments", response_model=CommentListResponse)
def get_comments(
    ticket_id: int, 
    db: Session = Depends(get_db), 
    limit: int | None = Query(default=None, ge=1, le=100), 
    offset: int = Query(default=0, ge=0),
    sort_order: Literal["asc", "desc"] = "asc",
    sort_by: Literal["id", "created_at"] = "id",
    search: str | None = Query(default=None, min_length=1, max_length=100)
    ):

    ticket = get_ticket_orm(db, ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if search is not None:
        search = search.strip()

    if not search:
        raise HTTPException(
            status_code=400,
            detail="Search cannot be empty"
        )
 
    comments, total = get_comments_orm(db, ticket_id, limit, offset, sort_order, sort_by, search)

    has_more = len(comments) + offset < total

    return {
        "items": comments,
        "limit": limit,
        "offset": offset,
        "total": total,
        "has_more": has_more
    }


@router.get("/{ticket_id}/comments-with-title", response_model=list[CommentWithTitleResponse])
def get_comments_with_title(ticket_id: int, db: Session = Depends(get_db)):

    ticket = get_ticket_orm(db,ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    comments_with_title = get_comments_with_title_orm(db, ticket_id)

    return comments_with_title


@router.get("/{ticket_id}/comments/{comment_id}", response_model=CommentResponse)
def get_comment(
    ticket_id: int,
    comment_id: int,
    db: Session = Depends(get_db)
):

    comment = get_comment_orm(db, comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.ticket_id != ticket_id:
        raise HTTPException(status_code=404, detail="Comment not found")
        

    return comment


@router.delete("/{ticket_id}/comments/{comment_id}")
def delete_comment(
    ticket_id: int,
    comment_id: int,
    db: Session = Depends(get_db)
):

    comment = get_comment_orm(db, comment_id)
    
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.ticket_id != ticket_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    try:
        delete_comment_orm(db, comment)

    except SQLAlchemyError:
        logger.exception("Database error while deleting comment")
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    return {"message": "Comment deleted"}



@router.patch("/{ticket_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    ticket_id: int,
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db)
):

    comment = get_comment_orm(db, comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
        
    if comment.ticket_id != ticket_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    try:
        changed_comment = update_comment_orm(db, comment, data.text)

    except SQLAlchemyError:
        logger.exception("Database error while updating comment")
        
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    return changed_comment


@router.get("/{ticket_id}/comments/stats/count",response_model=TicketCommentCountResponse)
def get_comments_count(ticket_id: int, db: Session = Depends(get_db)):

    count = get_comments_count_orm(db, ticket_id)

    return {"count": count}