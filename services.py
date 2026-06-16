"""
Core library service functions.

Data-structure choices
─────────────────────
• books        → dict[str, dict]   O(1) lookup by Book ID
• issued_books → set[str]          O(1) membership check; no duplicates needed
• categories   → Counter           tracks category-wise book counts automatically
• issue_log    → deque             bounded history of recent issue/return events
"""

import asyncio
from collections import Counter, deque
from typing import Any

from pydantic import ValidationError

from exceptions import (
    BookNotFoundException,
    BookNotIssuedException,
    DuplicateBookIDException,
    InvalidInputException,
    NoCopiesAvailableException,
)
from models import Book
from utils import (
    format_book_row,
    print_book_table_header,
    print_divider,
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
    Colors,
)


# ── In-memory data stores ─────────────────────────────────────────────────────

# Primary store: book_id → book dict
books: dict[str, dict[str, Any]] = {}

# Tracks which book IDs are currently issued (at least one copy out)
issued_books: set[str] = set()

# Category-wise book count  (collections.Counter)
category_counter: Counter = Counter()

# Bounded log of the last 50 issue / return events  (collections.deque)
issue_log: deque[str] = deque(maxlen=50)


# ── Seed data ─────────────────────────────────────────────────────────────────

def _seed_initial_data() -> None:
    """Populate the library with a few sample books on first run."""
    sample_books = [
        {
            "book_id": "B001",
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "publication_year": 1999,
            "category": "Technology",
            "total_copies": 3,
            "available_copies": 3,
        },
        {
            "book_id": "B002",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "publication_year": 2008,
            "category": "Technology",
            "total_copies": 2,
            "available_copies": 2,
        },
        {
            "book_id": "B003",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "publication_year": 1960,
            "category": "Fiction",
            "total_copies": 4,
            "available_copies": 4,
        },
        {
            "book_id": "B004",
            "title": "Sapiens",
            "author": "Yuval Noah Harari",
            "publication_year": 2011,
            "category": "History",
            "total_copies": 2,
            "available_copies": 2,
        },
        {
            "book_id": "B005",
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "publication_year": 2019,
            "category": "Technology",
            "total_copies": 3,
            "available_copies": 3,
        },
    ]
    for b in sample_books:
        books[b["book_id"]] = b
        category_counter[b["category"]] += b["total_copies"]


# ── Async helpers ─────────────────────────────────────────────────────────────

async def async_load_books() -> None:
    """
    Simulate an async I/O operation (e.g. fetching records from a remote DB).
    In production this would be an actual network / DB call.
    """
    print_info("Loading library records …")
    await asyncio.sleep(0.6)   # simulate network latency
    _seed_initial_data()
    print_success(f"Loaded {len(books)} book(s) into memory.\n")


async def async_fetch_statistics() -> dict[str, Any]:
    """
    Simulate async fetching of aggregated statistics.
    Returns a stats dictionary after a brief delay.
    """
    await asyncio.sleep(0.4)
    total_books      = len(books)
    unique_titles    = len({b["title"] for b in books.values()})
    total_available  = sum(b["available_copies"] for b in books.values())
    total_issued     = sum(b["total_copies"] - b["available_copies"] for b in books.values())

    return {
        "total_books":      total_books,
        "unique_titles":    unique_titles,
        "total_available":  total_available,
        "books_issued":     total_issued,
        "category_counts":  dict(category_counter),
        "recent_activity":  list(issue_log),
    }


# ── CRUD operations ───────────────────────────────────────────────────────────

def add_book(
    book_id: str,
    title: str,
    author: str,
    publication_year: int,
    category: str,
    copies: int,
) -> None:
    """
    Validate and add a new book to the library.

    Raises:
        DuplicateBookIDException: if book_id already exists.
        InvalidInputException:    if Pydantic validation fails.
    """
    if book_id in books:
        raise DuplicateBookIDException(book_id)

    try:
        new_book = Book(
            book_id=book_id,
            title=title,
            author=author,
            publication_year=publication_year,
            category=category,
            total_copies=copies,
            available_copies=copies,
        )
    except ValidationError as exc:
        # Extract the first human-readable error message from Pydantic
        first_error = exc.errors()[0]["msg"]
        raise InvalidInputException(first_error) from exc

    books[book_id] = new_book.to_dict()
    category_counter[category] += copies
    print_success(f"Book '{title}' (ID: {book_id}) added successfully.")


def view_books() -> None:
    """Display all books currently in the library."""
    print_header("All Library Books")

    if not books:
        print_warning("No books found in the library.")
        return

    print_book_table_header()
    for idx, book in enumerate(books.values(), start=1):
        print(format_book_row(book, idx))

    print_divider()
    print_info(f"Total: {len(books)} book record(s).")


def search_book(query: str, field: str = "all") -> list[dict[str, Any]]:
    """
    Search books by book_id, title, author, or across all fields.

    Args:
        query: The search term.
        field: One of 'id', 'title', 'author', or 'all'.

    Returns:
        A list of matching book dictionaries.
    """
    query_lower = query.lower().strip()
    results: list[dict[str, Any]] = []

    for book in books.values():
        match field:
            case "id":
                if query_lower == book["book_id"].lower():
                    results.append(book)
            case "title":
                if query_lower in book["title"].lower():
                    results.append(book)
            case "author":
                if query_lower in book["author"].lower():
                    results.append(book)
            case _:  # "all"
                if (
                    query_lower in book["book_id"].lower()
                    or query_lower in book["title"].lower()
                    or query_lower in book["author"].lower()
                ):
                    results.append(book)

    return results


def delete_book(book_id: str) -> None:
    """
    Delete a book by its ID.

    Raises:
        BookNotFoundException: if no book with that ID exists.
    """
    if book_id not in books:
        raise BookNotFoundException(book_id)

    book = books[book_id]
    category_counter[book["category"]] -= book["total_copies"]
    if category_counter[book["category"]] <= 0:
        del category_counter[book["category"]]

    issued_books.discard(book_id)
    del books[book_id]
    print_success(f"Book '{book['title']}' (ID: {book_id}) deleted successfully.")


def issue_book(book_id: str) -> None:
    """
    Issue one copy of a book to a borrower.

    Raises:
        BookNotFoundException:      if the book doesn't exist.
        NoCopiesAvailableException: if all copies are already out.
    """
    if book_id not in books:
        raise BookNotFoundException(book_id)

    book = books[book_id]
    if book["available_copies"] == 0:
        raise NoCopiesAvailableException(book["title"])

    books[book_id]["available_copies"] -= 1
    issued_books.add(book_id)

    event = f"ISSUED  → {book['title']} (ID: {book_id})"
    issue_log.appendleft(event)
    print_success(f"Book '{book['title']}' issued. "
                  f"Remaining copies: {books[book_id]['available_copies']}")


def return_book(book_id: str) -> None:
    """
    Return a previously issued book.

    Raises:
        BookNotFoundException:   if the book doesn't exist.
        BookNotIssuedException:  if the book was never issued.
    """
    if book_id not in books:
        raise BookNotFoundException(book_id)

    book = books[book_id]

    # A book can only be returned if at least one copy is currently out
    copies_out = book["total_copies"] - book["available_copies"]
    if copies_out == 0:
        raise BookNotIssuedException(book_id)

    books[book_id]["available_copies"] += 1

    # Remove from issued_books set only when all copies are back
    if books[book_id]["available_copies"] == book["total_copies"]:
        issued_books.discard(book_id)

    event = f"RETURNED← {book['title']} (ID: {book_id})"
    issue_log.appendleft(event)
    print_success(f"Book '{book['title']}' returned. "
                  f"Available copies: {books[book_id]['available_copies']}")


def display_statistics() -> None:
    """Fetch and display library statistics (runs async fetch synchronously)."""
    print_info("Fetching statistics …")
    stats = asyncio.run(async_fetch_statistics())

    print_header("Library Statistics")

    print(f"  {Colors.BOLD}Total Book Records   :{Colors.RESET} {stats['total_books']}")
    print(f"  {Colors.BOLD}Unique Titles        :{Colors.RESET} {stats['unique_titles']}")
    print(f"  {Colors.BOLD}Total Available Copies:{Colors.RESET} {stats['total_available']}")
    print(f"  {Colors.BOLD}Copies Currently Issued:{Colors.RESET} {stats['books_issued']}")

    print(f"\n  {Colors.BOLD}{Colors.UNDERLINE}Category Breakdown:{Colors.RESET}")
    if stats["category_counts"]:
        for cat, count in sorted(stats["category_counts"].items(),
                                  key=lambda x: x[1], reverse=True):
            bar = "█" * min(count, 30)
            print(f"    {cat:<18} {bar}  ({count})")
    else:
        print_warning("  No category data available.")

    print(f"\n  {Colors.BOLD}{Colors.UNDERLINE}Recent Activity (last {len(stats['recent_activity'])}):{Colors.RESET}")
    if stats["recent_activity"]:
        for entry in stats["recent_activity"][:10]:
            print(f"    {Colors.CYAN}{entry}{Colors.RESET}")
    else:
        print_warning("  No activity recorded yet.")

    print_divider()
