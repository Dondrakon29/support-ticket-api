from database import get_connection, row_to_comment

def create_comment_in_db(ticket_id, text, created_at):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO comments (
            ticket_id,
            text,
            created_at
        )
        VALUES (?, ?, ?)
    """, (
        ticket_id,
        text,
        created_at,
    ))

    comment_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return comment_id   



def get_comments_from_db(ticket_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, ticket_id, text, created_at
        FROM comments
        WHERE ticket_id = ?
    """, (ticket_id,))

    rows = cursor.fetchall()

    connection.close()

    comments = []

    for row in rows:
        comment = row_to_comment(row)
        comments.append(comment)

    return comments



def get_comments_with_ticket_title_from_db(ticket_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT comments.id, comments.text, comments.created_at, tickets.title
        FROM comments
        JOIN tickets
            ON comments.ticket_id = tickets.id
        WHERE comments.ticket_id = ?
    """, (ticket_id,))     

    rows = cursor.fetchall()

    connection.close()

    result = []

    for row in rows:
        comments_with_title = {
            "comment_id": row[0],
            "text": row[1],
            "created_at": row[2],
            "ticket_title": row[3]
        }

        result.append(comments_with_title)

    return result