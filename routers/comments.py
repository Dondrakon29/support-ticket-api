from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from database_orm import get_db
from sqlalchemy.orm import Session
from schemas import CommentCreate, CommentResponse, CommentWithTitleResponse, CommentUpdate
from repositories.comments_orm import get_comments_orm, create_comment_orm, get_comments_with_title_orm, get_comment_orm, delete_comment_orm, update_comment_orm
from repositories.tickets_orm import get_ticket_orm


router = APIRouter(prefix="/tickets", tags=["Comments"])


@router.post("/{ticket_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(ticket_id: int, comment: CommentCreate, db: Session = Depends(get_db)):

    ticket = get_ticket_orm(db, ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    created_at = datetime.now(timezone.utc).isoformat()

    new_comment = create_comment_orm(
    db,
    ticket_id,
    comment.text,
    created_at
)

    return new_comment


@router.get("/{ticket_id}/comments", response_model=list[CommentResponse])
def get_comments(ticket_id: int, db: Session = Depends(get_db)):

    ticket = get_ticket_orm(db, ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
 
    comments = get_comments_orm(db, ticket_id)

    return comments


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

    delete_comment_orm(db, comment)

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


    changed_comment = update_comment_orm(db, comment, data.text)

    return changed_comment

