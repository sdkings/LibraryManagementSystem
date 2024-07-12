from datetime import datetime
import sqlite3
class BookManager:
    def __init__(self, db_manager):
        """Initialize with a reference to a DatabaseManager instance."""
        self.db_manager = db_manager  # Assign the passed DatabaseManager instance to an instance variable.

    def search_booksss(self, keyword, page=1):
        keyword_pattern = f'%{keyword}%'   # Prepare the keyword pattern for SQL LIKE search, wrapping the provided keyword with wildcards.
        items_per_page = 5
        offset = (page - 1) * items_per_page

        # SQL query to search for books by keyword in the title or author and to fetch additional information.
    # This includes book ID, title, author, publish year, average rating, and availability status.
    # The query makes use of LEFT JOINs to include books even if they haven't been reviewed or borrowed.
        query = """
        SELECT 
            b.book_id, 
            b.title, 
            b.author, 
            b.pyear AS publish_year, 
            COALESCE(AVG(r.rating), 0) AS average_rating,  # Calculates the average rating; uses 0 if there are no ratings.
            CASE 
                WHEN COUNT(bo.book_id) > 0 THEN 'on borrow'  # Checks if the book is currently borrowed.
                ELSE 'available'  # If not borrowed, marks the book as available
            END AS availability
        FROM 
            books b
        LEFT JOIN 
            borrowings bo ON b.book_id = bo.book_id AND bo.end_date IS NULL  # Joins with borrowings to find books that are currently borrowed.
        LEFT JOIN 
            reviews r ON b.book_id = r.book_id  # Joins with reviews to calculate average rating.
        GROUP BY 
            b.book_id
        HAVING 
            b.title LIKE ? OR b.author LIKE ?   # Filters the results to include only those that match the keyword in title or author.
        ORDER BY 
            CASE 
                WHEN b.title LIKE ? THEN 1   # Prioritizes matches in title over author in the sorting order.
                WHEN b.author LIKE ? THEN 2
                ELSE 3
            END,
            CASE 
                WHEN b.title LIKE ? THEN b.title   # Further orders the results alphabetically by title or author, depending on the match.
                WHEN b.author LIKE ? THEN b.author
                ELSE NULL
            END
        LIMIT ? OFFSET ?;  #limiting the number of results per page and skipping over the results of previous pages.
        """

        # Execute the corrected query
        return self.db_manager.fetch_all(query, (keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern, items_per_page, offset))


    def borrow_book(self, book_id, member_email):
        """Borrow a book by its ID for the given member email."""

        # Check if the book is currently borrowed
        check_query = """
        SELECT 1 FROM borrowings
        WHERE book_id = ? AND end_date IS NULL;
        """
        if self.db_manager.fetch_one(check_query, (book_id,)):
            return "The book is currently borrowed."

        # # Check if the member exists
        # member_exists_query = "SELECT 1 FROM members WHERE email = ?;"
        # if not self.db_manager.fetch_one(member_exists_query, (member_email,)):
        #     return "Member does not exist."

        # Insert a new borrowing record
        borrow_query = """
        INSERT INTO borrowings (member, book_id, start_date)
        VALUES (?, ?, ?);
        """
        today = datetime.today().strftime("%Y-%m-%d")
        try:
            # Execute the SQL query using the db_manager's execute_query method.
    # The parameters for the query (member's email, book ID, and today's date) are passed as a tuple.
            self.db_manager.execute_query(borrow_query, (member_email, book_id, today))
            print("\nThe book has been successfully borrowed.\n")
        except sqlite3.IntegrityError as e:   # If an IntegrityError occurs, it likely means there was a problem with the database's integrity constraints.
            print(f"\nFailed to borrow the book: {e}\n")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def return_book(self, email):
        """ Returning a Book: First the system should display the user’s current borrowings, as a list of the borrowing id, book title, borrowing date, and return deadline for each unreturned borrowing (including overdue ones). The return deadline is 20 days after the borrowing date. User can pick a borrowing to return, and the system should record today’s date as the returning date."""

        # Fetch the user's current borrowings
        borrowing_query = """
        SELECT b.bid, b.book_id, bo.title, b.start_date, date(b.start_date, '+20 days') AS return_deadline
        FROM borrowings b
        JOIN books bo ON b.book_id = bo.book_id
        WHERE b.member = ? AND b.end_date IS NULL;
        """
        borrowings = self.db_manager.fetch_all(borrowing_query, (email,))  # Execute the query and fetch the results.

        # Display the borrowings
        if borrowings:
            print("Your current borrowings:")
            for borrowing in borrowings:
                borrowing_id, book_id, title, start_date, return_deadline = borrowing
                print(f"Borrowing ID: {borrowing_id}")
                print(f"Book id: {book_id}")
                print(f"Book Title: {title}")
                print(f"Borrowing Date: {start_date}")
                print(f"Return Deadline: {return_deadline}")
                print()
            
            # Prompt the user to select a borrowing to return
            return_book = input("press 2 to write a review, 1 to return a book, 0 to exit:  ")
            if return_book == "1":
                selected_borrowing_id = input("Enter the Borrowing ID of the book you want to return: ")

                # Check if the selected borrowing exists and belongs to the user
                selected_borrowing_query = """
                SELECT 1 FROM borrowings WHERE bid = ? AND member = ? AND end_date IS NULL;
                """
                if self.db_manager.fetch_one(selected_borrowing_query, (selected_borrowing_id, email)):
                    # Update the borrowing with the return date
                    return_date = datetime.now().strftime("%Y-%m-%d")
                    update_borrowing_query = """
                    UPDATE borrowings SET end_date = ? WHERE bid = ?;
                    """
                    self.db_manager.execute_query(update_borrowing_query, (return_date, selected_borrowing_id))  # If valid, update the borrowing record to set today's date as the end_date, marking the book as returned.
                    print("Book returned successfully.")
                else:
                    print("Invalid Borrowing ID or the book does not belong to you.")
            elif return_book == "2":
                # If the user wants to write a review, ask for the book ID and validate it.
            # Then, collect review text and rating, and insert the review into the database.
            # The steps include validating the book ID, ensuring the rating is within the acceptable range (1-5),
            # and finally, executing an SQL query to insert the review.
                book_id = int(input("Enter the book ID: "))
                flag = False
                for book in borrowings:
                    if book[1] == book_id:
                        flag = True
                        break
                if not flag:
                    print(" Invalid book Id")
                    return
                review_text = input("Enter your review: ")
                rating = int(input("Enter your rating (1-5): "))

                # Check if the rating is valid
                if rating < 1 or rating > 5:
                    print("Invalid rating. Please enter a number between 1 and 5.")
                else:
                    # Insert the review into the database
                    insert_review_query = """
                    INSERT INTO reviews (book_id, member,rating, rtext,rdate)
                    VALUES (?, ?, ?, ?, ?);
                    """
                    review_date = datetime.now().strftime("%Y-%m-%d")
                    self.db_manager.execute_query(insert_review_query, (book_id, email,rating,review_text,review_date))
                    print("Review submitted successfully.")
            elif return_book == "0":
                return
        else:
            print("You have no current borrowings.")

    
    def search_books(self, keyword, page=1):
        """Search for books by keyword with pagination and sorting.

        Args:
            keyword (str): The keyword to search in the title or author.
            page (int): The page number for pagination, starting from 1.

        Returns:
            A list of dictionaries, each containing details of a book.
        """
        offset = (page - 1) * 5  # 5 results per page

# SQL query to search for books. It joins the books table with reviews to calculate average rating,
    # and checks for availability based on current borrowings.
    # Uses IFNULL to handle books without ratings, displaying 'Not Rated' instead.
        query = """
        SELECT
            b.book_id,
            b.title,
            b.author,
            b.pyear AS publish_year,
            IFNULL(AVG(r.rating), 'Not Rated') AS average_rating,
            CASE
                WHEN EXISTS (
                    SELECT 1 FROM borrowings br WHERE br.book_id = b.book_id AND br.end_date IS NULL
                ) THEN 'On Borrow'
                ELSE 'Available'
            END AS availability
            FROM books b
            LEFT JOIN reviews r ON b.book_id = r.book_id
            WHERE b.title LIKE '%' || ? || '%'
            OR b.author LIKE '%' || ? || '%'
            GROUP BY b.book_id, b.title, b.author, b.pyear
            ORDER BY 
                CASE
                    WHEN b.title LIKE '%' || ? || '%' THEN 1
                    ELSE 2
                END,
                CASE
                    WHEN b.title LIKE '%' || ? || '%' THEN b.title
                    ELSE b.author
                END
            LIMIT 5 OFFSET ?;
            """

        result = self.db_manager.fetch_all(query, (keyword, keyword, keyword, keyword, offset))

        books = [{  # Transform the query results into a list of dictionaries for easier manipulation and readability.
            "book_id": row[0],
            "title": row[1],
            "author": row[2],
            "publish_year": row[3],
            "average_rating": row[4],
            "availability": row[5]
        } for row in result]
        # print the books in formatted way in one line
        for book in books:
            print(f"Book ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, Publish Year: {book['publish_year']}, Average Rating: {book['average_rating']}, Availability: {book['availability']}")

        return books

        
        