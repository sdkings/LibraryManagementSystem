AI Tool Used: ChatGPT, https://chat.openai.com/

We decided to take help from the AI model ChatGPT from time to time, since the project was vast and required a large amount of queries and functions, and for us it was the first project that we worked on that included both sqlite and python. The biggest doubt that we had when we started thinking about the project, was how to arrange the different functionalities. We decided to ask ChatGPT about it. Whenever using the AI model, we were careful not to use the original question, but to ask the AI model how it thinks and learn about it, so that we can use it ourselves. Otherwise, AI models tend to return faulty pieces of code that make life more difficult. Throughout this description, we will be sharing the prompts that we gave ChatGPT and the replies it gave. 

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Prompt 1: I am working on a big project that uses sqlite inside python and has multiple functionalities, so how do we arrange it systematically?

ChatGPT's Response: When working on such a big project, it is very ideal to use classes in python and then integrate sql queries into it. 

Prompt 2: How can I use sqlite and classes in python? Can you give an example

ChatGPT's Response: 

Here's a simple example of how you can use classes in Python to interact with SQLite databases:

python
Copy code
import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, data)
        self.connection.commit()

    def fetch_data(self, table_name):
        select_query = f"SELECT * FROM {table_name}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    db = Database("example.db")
    db.create_table("students", ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"])
    db.insert_data("students", (1, "Alice", 25))
    db.insert_data("students", (2, "Bob", 30))
    print(db.fetch_data("students"))
    db.close()
In this example:

We create a Database class that represents our SQLite database.
The __init__ method initializes the database connection and cursor.
The create_table method creates a table with the given name and columns if it doesn't already exist.
The insert_data method inserts data into the specified table.
The fetch_data method fetches all rows from the specified table.
Finally, the close method closes the database connection.
You can extend this example by adding more functionality as needed, such as updating data, deleting data, or executing custom queries.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

After we had learned from ChatGPT that using classes in python was the best way to go about it, we started working on our project. We divided the work in our project based on our strengths, and each of us decided to create a few classes based on the tasks we had chosen. Daman chose the task about user manager and making a profile, so he chose to make and work on the class userManager. Sapandeep chose to work on the task that involved book borrowing and seaarching along with Bakhshish, and also the review, so both of us together set to making the classes BookManager and ReviewManager. Harveer was supervising us and also working on the complete code, so he took the class DatabaseManager and started working on it. We started working on it by using the advice that ChatGPT gave, but we still had a lot of doubts. 

- - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Prompt 3: How can we further structure out project better? We now have a class called DatabaseManager, and made other classes too like you suggested.

ChatGPT's Response: 

Organize your project into modules where each class is in its own file for clarity and ease of maintenance.
Use exception handling to manage errors, especially for database operations.
Ensure that your DatabaseManager class is robust, handling connections efficiently, and is used by other manager classes to avoid duplicating the database connection logic.
This structure and these prototypes should provide a solid foundation for your project, encapsulating different areas of functionality and making the codebase more manageable as you develop and expand your application.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Bakhshish and Sapandeep were working on the SQL queries that involved searching for books and borrowing and reviewing. We tried to avoid using ChatGPT as less as possible, but sometimes in our queries we just couldn't think of a way to solve the problem. The biggest problem that me and Sapandeep faced when working on SQL query for searching a book, was the number of results that had to be shown. We were only supposed to show 5 results based on the constraints, and then we were supposed to ask the user for their input. If the user replied and said they wanted to show more, then we were supposed to show the next few results. This was something that confused us a lot, so me and Sapandeep decided to use ChatGPT to find some solutions. 

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - -- - - - - -- - - -- 

Prompt 4: For our project, we have to make a SQL query to search for books. We are using sqlite in python. In our results, we need to show just 5 results out of many, and then if the user asks, we have to show five more, like that. Could you help us?

ChatGPT's Response: Try using the 'page' method:

Here's how page is used in the code:
When the user initiates a search, the program starts fetching results from the first page (page = 1).
As the user navigates through the search results, the program increments the page variable to fetch the next page of results.
The page variable determines the OFFSET value used in the SQL query. The OFFSET specifies how many rows to skip before starting to return rows from the query. For example, if page is 2 and items_per_page is 5, the OFFSET would be 5 (since we skip the first 5 rows, which belong to the first page).
Each page typically displays a certain number of items per page (items_per_page). In this case, it's set to 5, meaning each page will display up to 5 search results.

But now there was another problem. Me and Sapandeep did not know what OFFSET was and how to use it, so once again we used ChatGPT for help.

Prompt 5: what is OFFSET in SQL? can you please explain?

ChatGPT's Response: 

In SQL, OFFSET is a clause used in conjunction with LIMIT to control the starting point for returning rows from a query result set.
Here's a brief explanation of how OFFSET works:

When you execute a SQL query that returns multiple rows of data, you may not always want to retrieve all the rows at once, especially if the result set is large.
LIMIT specifies the maximum number of rows to return in the result set.
OFFSET specifies the number of rows to skip before starting to return rows from the query. It effectively specifies the starting point for retrieving rows after skipping the specified number of rows.

- - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - -

Harveer also faced some problems along the way, for which he had to rely on ChatGPT. The process of making a login setup was really complex, and he had to take some help from ChatGPT. He first tried giving ChatGPT some commands to get a basic password manager example, but that used complex stuff like tkinter which was not needed by the project. He wanted to make a login - password system for his chosen class which used sqlite in its core. Below is the prompt that finally came in handy for Harveer and helped him complete his part of the project code:

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Prompt 6: How can I make a login page in python using sqlite? please show an example

ChatGPT's response: Sure, let's modify the previous example to use SQLite3 for user authentication. First, you'll need to create a SQLite database to store user credentials. Here's how you can do it:

python
Copy code
import sqlite3

Connect to SQLite database (creates a new database if not exists)
conn = sqlite3.connect('users.db')
Create a cursor object to execute SQL queries
cursor = conn.cursor()

Create a table to store user credentials if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

Dummy user data for demonstration purposes
dummy_username = "user"
dummy_password = "password"

Insert dummy user data into the table
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (dummy_username, dummy_password))

Commit changes and close connection
conn.commit()
conn.close()

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Another huge problem that almost all of us faced was how to handle various dates and times. Since we are making a model similar to a library, dates are important, from the booking of the borrowing of a book to the penalty system. The penalty system also required some calculations that looked difficult at first, but thankfully we got it done without asking for AI help. The other thing that we were slightly confused about was - python's datetime model, and how it would be integrated with sqlite into our project, which depended a lot on dates. Moroever, there was one specific class in the datetime module that had all of our attention: the timedelta class. Basically, the timedelta class would come in handy a lot for implementing the Here are our prompts and ChatGPT's responses: 

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Prompt 7: what exactly is the datetime module in python?

ChatGPT's Response: The datetime module in Python is a powerful utility for working with dates and times. It provides classes and methods to manipulate dates, times, and time intervals conveniently. Handling dates and times accurately and efficiently is essential in various applications, including data analysis, web development, scientific computing, and more.

Prompt 8: what all classes does the module have?

ChatGPT's Response: datetime Class: This class represents a specific point in time with both date and time components, including year, month, day, hour, minute, second, and microsecond.

date Class: It represents a date without time information, containing year, month, and day attributes.
time Class: This class represents a specific time of day without date information, including hour, minute, second, and microsecond.
timedelta Class: This class represents a duration, or the difference between two points in time, with attributes for days, seconds, and microseconds.

Key Functionalities:
Creating datetime Objects: You can create datetime, date, and time objects using constructors provided by the module, passing appropriate arguments such as year, month, day, hour, minute, etc.
Manipulating Date and Time: The datetime module offers various methods to manipulate dates and times, such as adding or subtracting time intervals (timedelta objects) from datetime objects.
Formatting and Parsing: You can format datetime objects into strings using the strftime() method and parse strings into datetime objects using the strptime() function.
Timezone Handling: The module provides support for working with timezones through the timezone class and tzinfo interface. You can convert between timezones and perform timezone-aware arithmetic.
Arithmetic Operations: datetime objects support arithmetic operations like addition and subtraction, allowing you to compute time differences or find future/past dates easily.
Comparisons and Sorting: datetime objects can be compared using comparison operators (<, >, ==, etc.), enabling sorting and ordering of dates and times.

Prompt 9: what is the timedelta class in the module? how can it be used to implement a penalty system for a library?

ChatGPT's Response: 

The timedelta class in the datetime module of Python represents a duration of time, expressed as the difference between two points in time. It allows you to perform arithmetic operations on dates and times, such as addition and subtraction, making it useful for calculating intervals or implementing features like a penalty system in a library.

Here's a breakdown of how timedelta can be used to implement a penalty system for a library:

1. Importing the datetime Module and timedelta Class
python
Copy code
from datetime import datetime, timedelta
2. Define Penalty Rules
You need to establish the rules for your penalty system, such as the duration of the penalty and the conditions under which penalties are incurred.

python
Copy code
penalty_duration = timedelta(days=7)  # Example: 7 days penalty
3. Tracking Borrowing and Returning
You'll need to keep track of when books are borrowed and returned, so you can calculate whether a penalty should be applied.

python
Copy code
borrow_date = datetime(2024, 3, 1)  # Example: Book borrowed on March 1st, 2024
return_date = datetime(2024, 3, 9)   # Example: Book returned on March 9th, 2024
4. Calculate Penalty
After a book is returned, check if it was returned late. If so, calculate the penalty.

python
Copy code
if return_date > borrow_date + penalty_duration:
    late_duration = return_date - (borrow_date + penalty_duration)
    penalty = late_duration.days * penalty_per_day  # Adjust penalty_per_day according to your rules
    print("Penalty incurred:", penalty)
Example Implementation
python
Copy code
from datetime import datetime, timedelta

penalty_duration = timedelta(days=7)  # Example: 7 days penalty
penalty_per_day = 1                    # Example: $1 penalty per day

borrow_date = datetime(2024, 3, 1)     # Example: Book borrowed on March 1st, 2024
return_date = datetime(2024, 3, 9)     # Example: Book returned on March 9th, 2024

if return_date > borrow_date + penalty_duration:
    late_duration = return_date - (borrow_date + penalty_duration)
    penalty = late_duration.days * penalty_per_day  # Adjust penalty_per_day according to your rules
    print("Penalty incurred:", penalty)
else:
    print("No penalty incurred.")

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - -
