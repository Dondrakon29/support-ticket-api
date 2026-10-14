from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Comment
from typing import Literal

def get_comments_orm(
    db: Session,
    ticket_id: int, 
    limit: int | None = None, 
    offset: int = 0, 
    sort_order: Literal["asc", "desc"] = "asc",
    sort_by: Literal["id", "created_at"] = "id"
    ):

    query = db.query(Comment).filter(Comment.ticket_id == ticket_id )

    total = query.count()

    if sort_by == "created_at":
        sort_column = Comment.created_at
    else:
        sort_column = Comment.id  

    if sort_order == "desc":
        query = query.order_by(sort_column.desc(), Comment.id.desc())
    
    else:
        query = query.order_by(sort_column.asc(), Comment.id.asc())  

    query = query.offset(offset)

    if limit is not None:
        query = query.limit(limit)

    comments = query.all()    

    return comments, total


def create_comment_orm(
    db: Session,
    ticket_id: int,
    text: str,
    created_at: str
):
    comment = Comment(
        ticket_id=ticket_id,
        text=text,
        created_at=created_at
    )

    try:
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment

    except SQLAlchemyError:
        db.rollback()
        raise


def get_comments_with_title_orm(db: Session, ticket_id: int):
    comments = db.query(Comment).filter(
        Comment.ticket_id == ticket_id
    ).all()

    result = []

    for comment in comments:
        result.append({
            "comment_id": comment.id,
            "text": comment.text,
            "created_at": comment.created_at,
            "ticket_title": comment.ticket.title
        })

    return result


def get_comment_orm(db: Session, comment_id: int):

    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    return comment


def delete_comment_orm(db: Session,comment: Comment):

    try:
        db.delete(comment)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

def update_comment_orm(db: Session, comment: Comment, text: str):
    
    try:
        comment.text = text

        db.commit()
        db.refresh(comment)

        return comment

    except SQLAlchemyError:

        db.rollback()
        raise


def get_comments_count_orm(db: Session, ticket_id: int):

    count = db.query(Comment).filter(Comment.ticket_id == ticket_id).count()

    return count

    
