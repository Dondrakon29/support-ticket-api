from database import get_connection, row_to_ticket


def get_ticket_from_db(ticket_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, description, status, priority, created_at, closed_at
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))

    row = cursor.fetchone()

    connection.close()

    return row_to_ticket(row)


def get_tickets_from_db(status: str | None = None, priority: str | None = None, search: str | None = None):
    connection = get_connection()
    cursor = connection.cursor()

    conditions = []
    params = []

    if status is not None:
        conditions.append("status = ?")
        params.append(status)

    if priority is not None:
        conditions.append("priority = ?")
        params.append(priority)

    if search is not None:
        conditions.append("(title LIKE ? OR description LIKE ?)")
        params.append(f"%{search}%")
        params.append(f"%{search}%")   

    where_clause = " AND ".join(conditions)

    if conditions:
        where_clause = "WHERE " + where_clause

    query = f"""
        SELECT id, title, description, status, priority, created_at, closed_at
        FROM tickets
        {where_clause}
    """

    cursor.execute(query, params)

    rows = cursor.fetchall()

    connection.close()

    tickets = []

    for row in rows:
        ticket = row_to_ticket(row)
        tickets.append(ticket)

    return tickets



def create_ticket_in_db(title, description, status, priority, created_at):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            title,
            description,
            status,
            priority,
            created_at,
            closed_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        status,
        priority,
        created_at,
        None
    ))

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return ticket_id 



def delete_ticket_from_db(ticket_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tickets
        WHERE id = ?
    """, (ticket_id,))

    deleted_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted_rows



def update_ticket_status_in_db(ticket_id, status, closed_at):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?, closed_at = ?
        WHERE id = ?
    """, (status, closed_at, ticket_id))

    changed_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return changed_rows