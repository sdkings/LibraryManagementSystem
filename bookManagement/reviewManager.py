import sqlite3
from datetime import datetime
class ReviewManager:
    def __init__(self, db_manager):
        """Initialize with a reference to a DatabaseManager instance."""
        self.db_manager = db_manager

    def add_review(self, book_id, member_email, rating, review_text):
        """Add a review for a book with the given rating and text."""
         # Ensure the rating is between 1 and 5 inclusive
        if not (1 <= rating <= 5):
            return "Rating must be between 1 and 5 inclusive."

        # Check if the book exists and the member has borrowed it before
        book_exists_query = "SELECT 1 FROM books WHERE book_id = ?"
        book_exists = self.db_manager.fetch_one(book_exists_query, (book_id,))
        if not book_exists:
            return "Book does not exist."

        # Check if the member exists
        member_exists_query = "SELECT 1 FROM members WHERE email = ?"
        member_exists = self.db_manager.fetch_one(member_exists_query, (member_email,))
        if not member_exists:
            return "Member does not exist."

        # Insert the new review into the reviews table
        # Assuming that the review ID is auto-incremented by the database
        insert_review_query = """
            INSERT INTO reviews (book_id, member, rating, rtext, rdate)
            VALUES (?, ?, ?, ?, ?);
        """
        review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
        try:
            self.db_manager.execute_query(insert_review_query, (book_id, member_email, rating, review_text, review_date))
            return "Review added successfully."
        except sqlite3.IntegrityError:
            return "Failed to add review. There might already be a review from this member for the book."
        except sqlite3.Error as e:
            return f"An error occurred: {e}"

