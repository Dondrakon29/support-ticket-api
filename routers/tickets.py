from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timezone
from typing import Literal
from schemas import TicketCreate, TicketStatusUpdate, TicketResponse
from repositories.tickets import get_ticket_from_db, get_tickets_from_db, create_ticket_in_db, delete_ticket_from_db, update_ticket_status_in_db



router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):

    ticket = get_ticket_from_db(ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    status: Literal["open", "in_progress", "closed"] | None = None,
    priority: Literal["low", "medium", "high"] | None = None,
    search: str | None = Query(default=None, min_length=1, max_length=100)):

    if search is not None:
        search = search.strip().lower()

    if search == "":
        search = None         

    tickets = get_tickets_from_db(status, priority, search)

    return tickets


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate):
    created_at = datetime.now(timezone.utc).isoformat()

    status = "open"

    ticket_id = create_ticket_in_db(
        ticket.title,
        ticket.description,
        status,
        ticket.priority,
        created_at
    )

    new_ticket = ticket.model_dump()
    new_ticket["id"] = ticket_id
    new_ticket["status"] = status
    new_ticket["created_at"] = created_at
    new_ticket["closed_at"] = None

    return new_ticket


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):

    deleted_rows = delete_ticket_from_db(ticket_id)

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deleted"}



@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(ticket_id: int, data: TicketStatusUpdate):
 
    if data.status == "closed":
        closed_at = datetime.now(timezone.utc).isoformat()
    else:
        closed_at = None

    changed_rows = update_ticket_status_in_db(ticket_id, data.status, closed_at)    

    if changed_rows == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")

    
    changed_ticket = get_ticket_from_db(ticket_id)

    return changed_ticket  