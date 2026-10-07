from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, timezone
from typing import Literal
from sqlalchemy.orm import Session
from database_orm import get_db
from schemas import TicketCreate, TicketStatusUpdate, TicketResponse, TicketCountResponse, TicketStatusCountsResponse, TicketPriorityCountsResponse
from repositories.tickets_orm import (
    get_ticket_orm, 
    get_tickets_orm, 
    create_ticket_orm, 
    delete_ticket_orm, 
    update_ticket_status_orm, 
    get_tickets_count_orm,
    get_tickets_count_by_status_orm,
    get_tickets_count_grouped_by_status_orm,
    get_tickets_count_grouped_by_priority_orm)



router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = get_ticket_orm(db, ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    status: Literal["open", "in_progress", "closed"] | None = None,
    priority: Literal["low", "medium", "high"] | None = None,
    search: str | None = Query(default=None, min_length=1, max_length=100),
    db: Session = Depends(get_db)
    ):

    if search is not None:
        search = search.strip().lower()

    if search == "":
        search = None         

    tickets = get_tickets_orm(db, status, priority, search)

    return tickets


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    created_at = datetime.now(timezone.utc).isoformat()

    status = "open"

    new_ticket = create_ticket_orm(
    db,
    ticket.title,
    ticket.description,
    status,
    ticket.priority,
    created_at
    )

    return new_ticket


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = get_ticket_orm(db, ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    delete_ticket_orm(db, ticket)

    return {"message": "Ticket deleted"}



@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(ticket_id: int, data: TicketStatusUpdate, db: Session = Depends(get_db)):
 
    if data.status == "closed":
        closed_at = datetime.now(timezone.utc).isoformat()
    else:
        closed_at = None

    ticket = get_ticket_orm(db, ticket_id) 

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    
    changed_ticket = update_ticket_status_orm(
        db,
        ticket,
        data.status,
        closed_at
    )

    return changed_ticket  


@router.get("/stats/count", response_model=TicketCountResponse)
def get_tickets_count(db: Session = Depends(get_db)):

    count = get_tickets_count_orm(db)

    return {"count": count}


@router.get("/stats/count/{status}", response_model=TicketCountResponse)
def get_tickets_count_by_status(
    status: Literal["open", "in_progress", "closed"],
    db: Session = Depends(get_db)
):

    count = get_tickets_count_by_status_orm(db, status)

    return {"count": count}



@router.get("/stats/statuses", response_model=TicketStatusCountsResponse)
def get_ticket_status_counts(db: Session = Depends(get_db)):

    rows = get_tickets_count_grouped_by_status_orm(db)

    result = {
    "open": 0,
    "in_progress": 0,
    "closed": 0
}

    for status, count in rows:
        result[status] = count

    return result


@router.get("/stats/priorities", response_model=TicketPriorityCountsResponse)
def get_ticket_priority_counts(db: Session = Depends(get_db)):

    rows = get_tickets_count_grouped_by_priority_orm(db)

    result = {
    "high": 0,
    "medium": 0,
    "low": 0
}

    for priority, count in rows:
        result[priority] = count

    return result 