import sqlite3
from datetime import datetime

class UserManager:
    def __init__(self, db_manager):
        """Initialize with a reference to a DatabaseManager instance."""
        self.db_manager = db_manager

    def login(self, email, password):
        """Authenticate a user with an email and password."""
        query = "SELECT * FROM members WHERE email = ? AND passwd LIKE ?;"
        row = self.db_manager.fetch_one(query, (email, password))
        if row is not None:
            # Compare passwords in a case-sensitive manner
            if row[1] == password:
                return row
        return None

    def register(self, email, password, name, byear, faculty):
        """Register a new user with the given information."""

        checkindatabase = self.db_manager.fetch_one("SELECT * FROM members WHERE email = ?;", (email,))
        if(checkindatabase != None):
            print("Email already exists in the database.")
            return False
        query = "INSERT INTO members VALUES (?, ?, ?, ?, ?) ;"
        return self.db_manager.execute_query(query, (email, password, name, byear, faculty))

    def view_profile(self, email):
        """Display the profile information for the given email."""
        personal_info = self.personal_information(email) 
        self.db_manager.update_overdue_penalties(email, datetime.now().strftime('%Y-%m-%d'))
        unpaid_penalties_count, total_debt = self.penalty_information(email)
        previous_borrowings, current_borrowings, overdue_borrowings = self.borrowings_information(email)
        

        if personal_info:
            name, email, birth_year = personal_info
            print("Name:", name)
            print("Email:", email)
            print("Birth Year:", birth_year)
            print("Previous Borrowings:", previous_borrowings)
            print("Current Borrowings:", current_borrowings)
            print("Overdue Borrowings:", overdue_borrowings)
            print("Unpaid Penalties:", unpaid_penalties_count)
            print("Total Debt:", total_debt)
        else:
            print("User not found.")
    
    # Function to fetch personal information
    def personal_information(self, user_email):
        try:
            return self.db_manager.fetch_one("SELECT name, email, byear FROM members WHERE email = ?;", (user_email,))
        except sqlite3.Error as e:
            print("Error fetching personal information:", e)

    # Function to fetch borrowings information
    def borrowings_information(self, user_email):
        try:
            prev = self.db_manager.fetch_one("SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NOT NULL;", (user_email,))
            if prev == None:
                previous_borrowings = 0
            else:
                previous_borrowings = prev[0]

            curr = self.db_manager.fetch_one("SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL;", (user_email,))
            if curr == None:
                current_borrowings = 0
            else:    
                current_borrowings = curr[0]
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            overdue_borrowings = self.db_manager.update_overdue_penalties(user_email, current_date)

            return previous_borrowings, current_borrowings, overdue_borrowings
        except sqlite3.Error as e:
            print("Error fetching borrowings information:", e)

    # Function to fetch penalty information
    def penalty_information(self, user_email):
        try:
            # Combine both calculations into a single query for efficiency
            query = """
            SELECT 
                COUNT(*) AS unpaid_penalties_count, 
                SUM(p.amount - COALESCE(p.paid_amount, 0)) AS total_debt
            FROM borrowings AS b 
            JOIN penalties AS p ON b.bid = p.bid 
            WHERE b.member = ? 
            AND (p.paid_amount IS NULL OR p.paid_amount < p.amount);
            """
            
            result = self.db_manager.fetch_one(query, (user_email,))
            
            # Handling the case where the query returns None or contains None values
            if result is None or result[0] is None:
                return 0, 0
            
            unpaid_penalties_count, total_debt = result
            total_debt = total_debt if total_debt is not None else 0
            
            return unpaid_penalties_count, total_debt

        except sqlite3.Error as e:
            print("Error fetching penalty information:", e)
            return None


        