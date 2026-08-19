"""SQLite database setup and core functions for Artist Manager."""

import sqlite3
from pathlib import Path

# database.py lives in app/, so the database file is stored in the project root.
DB_PATH = Path(__file__).resolve().parent.parent / "artist_manager.db"


def get_connection() -> sqlite3.Connection:
    """Open a connection to the database, with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables() -> None:
    """Create all tables if they don't already exist. Safe on every launch."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS artworks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            medium TEXT,
            dimensions TEXT,
            creation_year INTEGER,
            retail_price REAL,
            inventory_number TEXT UNIQUE,
            status TEXT DEFAULT 'In Studio',
            image_path TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS supplies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            stock_quantity INTEGER DEFAULT 0
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artwork_id INTEGER,
            customer_id INTEGER,
            sale_date TEXT,
            price REAL,
            tax_charged REAL,
            payment_method TEXT,
            FOREIGN KEY (artwork_id) REFERENCES artworks (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date TEXT,
            vendor_item TEXT,
            cost REAL,
            category TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS exhibitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exhibition_name TEXT NOT NULL,
            venue TEXT,
            entry_fee REAL,
            application_deadline TEXT,
            status TEXT DEFAULT 'Applied'
        )
        """
    )

    conn.commit()
    conn.close()


# --- Artwork functions ---


def insert_artwork(
    title,
    medium,
    dimensions,
    creation_year,
    retail_price,
    inventory_number,
    status="In Studio",
    image_path=None,
) -> int:
    """Add a new artwork. Return the new row's ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO artworks (
            title,
            medium,
            dimensions,
            creation_year,
            retail_price,
            inventory_number,
            status,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            medium,
            dimensions,
            creation_year,
            retail_price,
            inventory_number,
            status,
            image_path,
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_artworks() -> list[sqlite3.Row]:
    """Return every artwork as a list of rows."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artworks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_artwork_status(artwork_id: int, new_status: str) -> None:
    """Change an artwork's status, such as to Sold after a sale."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE artworks SET status = ? WHERE id = ?",
        (new_status, artwork_id),
    )
    conn.commit()
    conn.close()


# --- Expense functions ---


def insert_expense(
    transaction_date: str,
    vendor_item: str,
    cost: float,
    category: str,
) -> int:
    """Add a new expense and return the new row's ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO expenses (
            transaction_date,
            vendor_item,
            cost,
            category
        )
        VALUES (?, ?, ?, ?)
        """,
        (transaction_date, vendor_item, cost, category),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_expenses() -> list[sqlite3.Row]:
    """Return all expenses with the newest transaction first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, transaction_date, vendor_item, cost, category
        FROM expenses
        ORDER BY transaction_date DESC, id DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows