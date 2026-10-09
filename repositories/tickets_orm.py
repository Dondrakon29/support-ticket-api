from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Ticket
from sqlalchemy import or_, func


def get_ticket_orm(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    return ticket

def get_tickets_orm(db: Session,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None
    ):

    query = db.query(Ticket)

    if status is not None:
        query = query.filter(Ticket.status == status)

    if priority is not None:
        query = query.filter(Ticket.priority == priority)

    if search is not None:
        query = query.filter(
            or_(
                Ticket.title.ilike(f"%{search}%"), 
                Ticket.description.ilike(f"%{search}%")
            )
        )         
    

    tickets = query.all()    

    return tickets


def create_ticket_orm(
    db: Session,
    title: str,
    description: str,
    status: str,
    priority: str,
    created_at: str
    ):

    try:

        ticket = Ticket(
            title=title,
            description=description,
            status=status,
            priority=priority,
            created_at=created_at,
            closed_at=None
        )

     
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_ticket_orm(db: Session, ticket: Ticket):

    try:
        db.delete(ticket)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise    


def update_ticket_status_orm(
    db: Session,
    ticket: Ticket,
    status: str,
    closed_at: str | None
    ):

    try:
        ticket.status = status
        ticket.closed_at = closed_at

        db.commit()
        db.refresh(ticket)

        return ticket

    except SQLAlchemyError:
        db.rollback()
        raise


def get_tickets_count_orm(db: Session):

    count = db.query(Ticket).count()
    return count


def get_tickets_count_by_status_orm(db: Session, status: str):

    count = db.query(Ticket).filter(Ticket.status == status).count()

    return count


def get_tickets_count_grouped_by_status_orm(db: Session):

    rows = db.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all()

    return rows


def get_tickets_count_grouped_by_priority_orm(db: Session):
    
    rows = db.query(Ticket.priority, func.count(Ticket.id)).group_by(Ticket.priority).all()

    return rows