import sqlite3

# Specify your database file name
db_file = 'enterprise_data.db'

# SQL commands to drop existing tables
drop_table_commands = [
    "DROP TABLE IF EXISTS reviews;",
    "DROP TABLE IF EXISTS penalties;",
    "DROP TABLE IF EXISTS borrowings;",
    "DROP TABLE IF EXISTS books;",
    "DROP TABLE IF EXISTS members;"
]

# SQL commands to create new tables
create_table_commands = [
    """
    PRAGMA foreign_keys = ON;
    """,
    """
    CREATE TABLE members (
        email CHAR(100),
        passwd CHAR(100),
        name CHAR(255) NOT NULL,
        byear INTEGER,
        faculty CHAR(100),
        PRIMARY KEY (email)
    );
    """,
    """
    CREATE TABLE books (
        book_id INTEGER,
        title CHAR(255),
        author CHAR(150),
        pyear INTEGER,
        PRIMARY KEY (book_id)
    );
    """,
    """
    CREATE TABLE borrowings (
        bid INTEGER,
        member CHAR(100) NOT NULL,
        book_id INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        PRIMARY KEY (bid),
        FOREIGN KEY (member) REFERENCES members(email),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    );
    """,
    """
    CREATE TABLE penalties (
        pid INTEGER,
        bid INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        paid_amount INTEGER,
        PRIMARY KEY (pid),
        FOREIGN KEY (bid) REFERENCES borrowings(bid)
    );
    """,
    """
    CREATE TABLE reviews (
        rid INTEGER,
        book_id INTEGER NOT NULL,
        member CHAR(100) NOT NULL,
        rating INTEGER NOT NULL,
        rtext CHAR(255),
        rdate DATE,
        PRIMARY KEY (rid),
        FOREIGN KEY (member) REFERENCES members(email),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    );
    """
]

# Insert data commands
insert_data_commands = [
    """
    INSERT INTO members (email, passwd, name, byear, faculty) VALUES 
('bakhshis@ualberta.ca', 'bakhshis', 'Bakhshish', 2003, 'Science'),
('sapan@ualberta.ca', 'sapan', 'Sapandeep', 2003, 'Science');
    """
]

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Execute commands to drop tables if they exist
    for command in drop_table_commands:
        c.execute(command)

    # Execute commands to create tables
    for command in create_table_commands:
        c.executescript(command) if 'PRAGMA' in command else c.execute(command)

    # Execute each insert command
    for command in insert_data_commands:
        try:
            c.executescript(command)  # Use executescript() to handle multiple insertions in one command
            print("Data inserted successfully.")
        except sqlite3.IntegrityError as e:
            print("An error occurred: {}. Data may already exist.".format(e))
        except sqlite3.OperationalError as e:
            print("Operational error: {}. Check your SQL syntax.".format(e))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database and tables created successfully in '{}'.".format(db_file))

if __name__ == "__main__":
    main()
