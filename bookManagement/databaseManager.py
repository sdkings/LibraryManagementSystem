import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        """Initialize the connection to the database."""
        self.conn = sqlite3.connect(db_path) # The connection object represents the database and allows for executing SQL commands.
        self.c = self.conn.cursor()	  # The cursor is used to execute SQL queries and fetch data from the database.
        self.c.execute('PRAGMA   foreign_keys=ON;')	 # This is important for maintaining referential integrity in relationships between tables.

    def execute_query(self, query, params=()):
        """Execute a single query with optional parameters."""
        if not sqlite3.complete_statement(query):  # Check if the provided query is a complete and valid SQL statement.
            print("Invalid query")
            return False
        try:
            self.c.execute(query, params)  # This uses the cursor object created during the database connection initialization.
            self.conn.commit()  # Commit the transaction
            return True
        except sqlite3.Error as e:
            print(e)
            return False
        

    def fetch_one(self, query, params=()):
        """Fetch a single row from a query with optional parameters."""
        if not sqlite3.complete_statement(query):
            print("Invalid query")
            return None
        try:
            self.c.execute(query, params)
            return self.c.fetchone()
        except sqlite3.Error as e:
            print(e)
            return None

    def fetch_all(self, query, params=()):
        """Fetch all rows from a query with optional parameters."""
        try:
            self.c.execute(query, params)
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(e)
            return None
    
    def update_overdue_penalties(self, user_email, current_date):
        """Update or insert penalties for overdue borrowings of a specific user."""

 # SQL query to select borrowings that are overdue. It calculates the number of overdue days
    # by comparing the current date with the borrowing start date. A book is considered overdue
    # if it hasn't been returned within 20 days from the borrowing date.
        overdue_query = """
        SELECT bid, julianday(?) - julianday(start_date) AS overdue_days
        FROM borrowings
        WHERE member = ?
        AND (end_date IS NULL OR end_date > ?)
        AND julianday(?) - julianday(start_date) > 20
        """
        overdue_borrowings = self.fetch_all(overdue_query, (current_date, user_email, current_date, current_date))
        overdue_count = 0 # Initialize a counter for overdue borrowings processed.
        for borrowing in overdue_borrowings:
            bid, overdue_days = borrowing
            penalty = int(max(0, overdue_days - 20))  # Calculate penalty
            existing_penalty = self.fetch_one("SELECT pid FROM penalties WHERE bid = ?;", (bid,))
            if existing_penalty is not None:
                self.execute_query("UPDATE penalties SET amount = ? WHERE bid = ?;", (penalty, bid))
            else:
                self.execute_query("INSERT INTO penalties (bid, amount, paid_amount) VALUES (?, ?, 0);", (bid, penalty))
            overdue_count += 1  # Increment the counter
        return overdue_count
        
