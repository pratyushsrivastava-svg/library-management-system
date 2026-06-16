# library-management-system
Here is a polished, humanized version of your README file. I have removed the em dashes, softened the technical jargon into a more conversational and engaging tone, and used clean formatting to make it highly readable and professional.

---

# 📚 Library Management System

Welcome to the Library Management System! This is a Python-based command-line application designed to help librarians seamlessly manage books and handle everyday library tasks. I originally built this as my Week 1 internship assignment.

## 📖 Project Overview

With this system, a librarian can easily add, view, search, and delete books. You can also handle issuing and returning copies, as well as check out live library statistics with category breakdowns and recent activity logs.

Under the hood, the app is fully modular. It simulates async I/O, uses Pydantic for strict data validation, and puts a variety of Python data structures and collections to work in practical ways.

## ✨ Features

| Feature | Description |
| --- | --- |
| **Add Book** | Validates and stores a new book with its ID, title, author, year, category, and total copies. |
| **View All Books** | Displays a neatly formatted table of every book currently in the library. |
| **Search Books** | Search by Book ID, Title, Author, or scan across all fields at once. |
| **Delete Book** | Removes a book by its ID after a quick confirmation prompt. |
| **Issue Book** | Reduces available copies by 1, validating both the book's existence and its current availability. |
| **Return Book** | Increases available copies by 1, making sure the book was actually issued first. |
| **Statistics** | Shows total books, unique titles, available copies, issue counts, a category bar chart, and a log of recent activity. |
| **Async Loading** | Simulates fetching records from a remote database on startup to show how asynchronous operations feel in practice. |

## 🗂️ Project Structure

```text
library_management_system/
│
├── main.py          # CLI entry point and main menu loop
├── models.py        # Pydantic Book model with strict field validators
├── exceptions.py    # Custom exception hierarchy for clean error handling
├── services.py      # Core business logic (add, view, search, delete, etc.)
├── utils.py         # Helpful utilities for display, color formatting, and input
├── requirements.txt # Project dependencies
└── README.md        # You are here!

```

## 🧠 Concepts Used

I built this project to demonstrate a strong understanding of core Python concepts. Here is a breakdown of how they are applied:

### Data Structures

* **Lists:** We use these behind the scenes when returning search results (`list[dict]`) and when converting the activity log into a standard list to display our statistics.
* **Dictionaries:** Our primary data store is a `books` dictionary (`dict[str, dict]`), keyed by the `book_id`. Dictionaries give us lightning-fast O(1) lookups, insertions, and deletions, which are the most common operations here. Each value is a flat dictionary holding a single book's record.
* **Sets:** The `issued_books` set (`set[str]`) keeps track of which Book IDs currently have at least one copy checked out. Sets are perfect here because they offer instant O(1) membership checks (`book_id in issued_books`) and naturally prevent duplicate entries.

### Architecture & Safety

* **Modular Functions:** Everything is broken down into standalone functions in `services.py` (like `add_book()`, `issue_book()`, and their async variants). Meanwhile, `main.py` handles all the user input, keeping the business logic completely separated from the UI.
* **Exception Handling:** The app uses a custom exception family starting with `LibraryException` in `exceptions.py`. You will find specific errors like `BookNotFoundException` or `NoCopiesAvailableException`. All user actions are safely wrapped in try/except blocks.
* **Type Hints:** The code is fully type-hinted. Every function signature and variable tells you exactly what data type to expect, making the codebase highly predictable.

### External Libraries & Advanced Modules

* **Pydantic:** Inside `models.py`, the `Book` model uses `@field_validator` decorators to make sure fields aren't empty, publication years make sense, and copy counts are positive. Any slip-ups trigger a `ValidationError` that the app gracefully catches and packages as an `InvalidInputException`.
* **Collections Module:** We tap into `collections` in two main ways. First, a `Counter` tracks the number of copies per category to build the statistics bar chart. Second, a `deque(maxlen=50)` acts as a bounded log for issue and return events. By appending new events to the left, the newest activity stays at the top, and the maximum length cap prevents memory bloat.
* **Asyncio:** To mimic real-world network latency, `async_load_books()` and `async_fetch_statistics()` pause briefly to simulate fetching data from remote databases or API services.

---

## 🚀 How To Run

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd library_management_system

```

**2. Create and activate a virtual environment (recommended)**

```bash
python -m venv venv

# For macOS / Linux:
source venv/bin/activate        

# For Windows:
venv\Scripts\activate.bat       

```

**3. Install dependencies**

```bash
pip install -r requirements.txt

```

**4. Run the application**

```bash
python main.py

```

## ⚙️ Requirements

* **Python 3.10 or higher** (The app takes advantage of modern structural pattern matching)
* **pydantic >= 2.0.0**

---

## 💻 Sample Session

```text
ℹ  Loading library records ...
✔  Loaded 5 book(s) into memory.

  ┌─────────────────────────────────────┐
  │      LIBRARY MANAGEMENT SYSTEM      │
  ├─────────────────────────────────────┤
  │  1. Add Book                        │
  │  2. View All Books                  │
  │  ...                                │
  └─────────────────────────────────────┘

Enter your choice (1-8): 5
Enter Book ID to issue: B001
✔  Book 'The Pragmatic Programmer' issued. Remaining copies: 2

```
Add README
