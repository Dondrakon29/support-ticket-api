import sqlite3


def get_connection():
    connection = sqlite3.connect("tickets.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def setup_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL,
            closed_at TEXT
        )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (ticket_id)
            REFERENCES tickets(id)
            ON DELETE CASCADE
    )
""")

    connection.commit()
    connection.close()


def row_to_ticket(row):

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "status": row[3],
        "priority": row[4],
        "created_at": row[5],
        "closed_at": row[6]
    }


def row_to_comment(row):

    if row is None:
            return None

    return {
        "id": row[0],
        "ticket_id": row[1],
        "text": row[2],
        "created_at": row[3]
    }




