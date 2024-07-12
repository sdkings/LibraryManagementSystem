import sqlite3

class PenaltyManager:
    def __init__(self, db_manager):
        """Initialize with a reference to a DatabaseManager instance."""
        self.db_manager = db_manager
    
    def list_penalties(self, member_email):
        """List all penalties for the given member email."""
        query = """
        SELECT p.pid, p.bid, p.amount, p.paid_amount
        FROM penalties AS p
        JOIN borrowings AS b ON p.bid = b.bid
        WHERE b.member = ? AND (p.paid_amount is NULL or p.paid_amount < p.amount);
        """
        penalties = self.db_manager.fetch_all(query, (member_email,))
        return penalties
    
    def pay_penalty(self, penalty_id, amount):
        """Pay a specified amount towards a penalty by its ID."""
         # SQL query to select the total penalty amount and the amount already paid for a specific penalty ID.
    # COALESCE is used to ensure that if the paid_amount is NULL, it treats it as 0.
        penalty_query = """
        SELECT amount, COALESCE(paid_amount, 0) FROM penalties WHERE pid = ?;
        """
        penalty = self.db_manager.fetch_one(penalty_query, (penalty_id,))
        if penalty is None:
            return "Penalty not found."

        total_amount, paid_amount = penalty  # Unpack the fetched penalty details.
        new_paid_amount = paid_amount + amount  # Calculate the new paid amount after making the payment

        if new_paid_amount > total_amount:
            return "Payment exceeds the penalty amount."
 # SQL query to update the paid amount for the penalty.
        update_query = """
        UPDATE penalties SET paid_amount = ? WHERE pid = ?;
        """
        self.db_manager.execute_query(update_query, (new_paid_amount, penalty_id))
        return "Penalty paid successfully."
        

