import getpass #for password protection
from databaseManager import DatabaseManager
from bookManager import BookManager
from userManager import UserManager
from paneltyManager import PenaltyManager
class CLIInterface:
    def __init__(self, user_manager, book_manager, review_manager, penalty_manager):
        """Initialize with references to the manager classes."""
        self.user_manager = user_manager
        self.book_manager = book_manager
        self.review_manager = review_manager
        self.penalty_manager = penalty_manager

    def main_menu(self, user_email):
        """Display the main menu and handle user input."""
        while True:
            user_input= input("Choose any options by typing the number:\n1. Member profile: \n2. Returning a Book  \n3. Search for Books \n4. Pay a Penalty \n5. Logout \nq. quit\n=>")
            try:
                if user_input == "q":
                    return False
                user_input = int(user_input)
                if user_input == 1:
                    self.user_manager.view_profile(user_email)
                elif user_input == 2:
                    self.book_manager.return_book(user_email)
                elif user_input == 3:
                    page = 1
                    new_search = True
                    while True:
                        if new_search:
                            keyword = input("Enter a keyword to search for books: ")
                            new_search = False
                        books = self.book_manager.search_books(keyword, page)
                        if not books:
                            print("No books found.")
                            break
                        selected_book = input("\nEnter the book ID to borrow, s for new search, q to exit search,or press 'n' for the next page: ")
                        # check if books is empty

                        if selected_book == "q":
                            break
                        elif selected_book == "n":
                            page += 1
                        elif selected_book == "s":
                            new_search = True
                            page = 1
                        else:
                            # check if the input is a number
                            try:
                                selected_book = int(selected_book)
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                                continue
                            # check if book id is in books and is available to borrow
                            found = False
                            for book in books:
                                if book["book_id"] == selected_book:
                                    found = True
                                    if book["availability"] == "On Borrow":
                                        print("Book is not available to borrow.")
                                    else:
                                        self.book_manager.borrow_book(selected_book, user_email)
                                        break
                            if not found:
                                print(" Invalid book Id")                       
                elif user_input == 4:
                    self.pay_a_penalty(user_email)
                elif user_input == 5:
                    self.log_out()
                    break
                else:
                    print("Invalid option. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    def log_out(self):
        """Log out the current user."""
        print("You have been logged out successfully.")     
    def pay_a_penalty(self, user_email):
        """Allow the user to view and pay their penalties."""
        penalties = self.penalty_manager.list_penalties(user_email)
        if not penalties:
            print("No unpaid penalties found.")
            return
        
        print("Unpaid Penalties:")
        for penalty in penalties:
            due_amount = penalty[2] - (penalty[3] if penalty[3] else 0)
            print(f"Penalty ID: {penalty[0]}, Borrowing ID: {penalty[1]}, Amount Due: ${due_amount}")
        
        try:
            check = input("Do you want to pay a penalty? (y/n): ")
            if check == "n":
                return
            penalty_id = int(input("Enter the Penalty ID you wish to pay: "))
            amount = float(input("Enter the amount you wish to pay: $"))
            response = self.penalty_manager.pay_penalty(penalty_id, amount)
            print(response)
        except ValueError:
            print("Invalid input. Please enter valid numbers for Penalty ID and amount.")          

    def login_menu(self):
        """Handle the login/signup process."""
        while True:
            inp = str(input("For login press: l\nFor Signup perss: s\nTo quit program press: q\n=> "))

            if inp == "l":
                email = str(input("Enter your email: "))
                password = getpass.getpass("Enter your password: ")
                # Add logic to handle the email and password entered by the user
                user = self.user_manager.login(email, password)
                if user == None:
                    print("Invalid email or password. Please try again.")
                else:
                    print("Welcome, " + user[2] + "!")  # user[2] is the name of the user
                    return email
            elif inp == "s":
                email = str(input("Enter your email: "))
                password = getpass.getpass("Enter your password: ")
                name = str(input("Enter your name: "))
                byear = str(input("Enter your birth year: "))
                faculty = str(input("Enter your faculty: "))
                # Add logic to handle the registration process
                if self.user_manager.register(email, password, name, byear, faculty) == False:
                    print("Registration failed. Please try again.")
                else:
                    print("Registration successful!")
                    return self.login_menu()
            elif inp == "q":
                print("Goodbye!")
                return False
            else:
                print("Invalid option, please try again.")

    def user_menu(self, email):
        """Display the user-specific menu for logged-in users."""

def main():
    database_name = input("Enter the name of the database: ")
    db_man = DatabaseManager(database_name)
    cl = CLIInterface(UserManager(db_man), BookManager(db_man),"he", PenaltyManager(db_man))
    while True:
        email = cl.login_menu()
        if email:
            if cl.main_menu(email) == False:
                break
        else:
            break
if __name__ == "__main__":
    main()