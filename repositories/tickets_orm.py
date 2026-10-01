from sqlalchemy.orm import Session
from models import Ticket
from sqlalchemy import or_


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