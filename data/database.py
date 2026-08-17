from pathlib import Path
import sqlite3


# Find the folder containing database.py
BASE_DIR = Path(__file__).resolve().parent

# Create the data folder if it does not exist
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Full path to the SQLite database file
DB_PATH = DATA_DIR / "artist_manager.db"


def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(DB_PATH)

    # Allows database rows to be accessed by column name
    connection.row_factory = sqlite3.Row

    # Enforce foreign-key relationships
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def add_test_artwork() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO artworks (
                title,
                medium,
                dimensions,
                creation_year,
                retail_price,
                inventory_number,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Sunset Study",
                "Oil on Canvas",
                "24 x 36 inches",
                2026,
                1200.00,
                "ART-0001",
                "In Studio",
            ),
        )

        connection.commit()

    print("Test artwork added successfully.")

def create_tables() -> None:
    """
    Create the application's database tables if they do not already exist.
    """

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS artworks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                medium TEXT,
                dimensions TEXT,
                creation_year INTEGER,
                retail_price REAL NOT NULL DEFAULT 0,
                inventory_number TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'In Studio',
                image_path TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS supplies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT,
                current_stock INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artwork_id INTEGER NOT NULL,
                customer_id INTEGER,
                sale_date TEXT NOT NULL,
                sale_price REAL NOT NULL,
                tax_charged REAL NOT NULL DEFAULT 0,
                payment_method TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (artwork_id)
                    REFERENCES artworks(id),

                FOREIGN KEY (customer_id)
                    REFERENCES customers(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                vendor_item TEXT NOT NULL,
                cost REAL NOT NULL,
                tax_category TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exhibitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                venue TEXT,
                entry_fee REAL NOT NULL DEFAULT 0,
                deadline TEXT,
                status TEXT NOT NULL DEFAULT 'Planned',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

    print(f"Database created successfully at: {DB_PATH}")


if __name__ == "__main__":
    create_tables()
    add_test_artwork()