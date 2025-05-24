from ticket_gen import generate_ticket_code
import sqlite3
import datetime

DB_PATH = "tickets.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_code TEXT UNIQUE,
        phone TEXT,
        method TEXT,
        entry_time TEXT,
        exit_time TEXT,
        synced INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def log_entry(phone=None, method="ticketless"):
    init_db()
    t = datetime.datetime.now().isoformat()
    ticket_code = generate_ticket_code()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tickets (ticket_code, phone, method, entry_time) VALUES (?, ?, ?, ?)",
              (ticket_code, phone, method, t))
    conn.commit()
    conn.close()
    return ticket_code

def log_exit(phone_or_ticket):
    init_db()
    t = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, ticket_code FROM tickets WHERE (phone=? OR ticket_code=?) AND exit_time IS NULL",
        (phone_or_ticket, phone_or_ticket)
    )
    row = c.fetchone()
    if row:
        tid = row[1]
        c.execute("UPDATE tickets SET exit_time=? WHERE ticket_code=?", (t, tid))
        conn.commit()
        conn.close()
        return tid
    conn.close()
    return None