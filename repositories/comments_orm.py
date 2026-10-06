from sqlalchemy.orm import Session
from models import Comment

def get_comments_orm(db: Session, ticket_id: int):
    comments = db.query(Comment).filter(Comment.ticket_id == ticket_id ).all()

    return comments


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

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


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

    db.delete(comment)
    db.commit()

    