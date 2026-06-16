"""
Library Management System — Entry Point
"""

import asyncio
import sys

from exceptions import (
    BookNotFoundException,
    BookNotIssuedException,
    DuplicateBookIDException,
    InvalidInputException,
    NoCopiesAvailableException,
)
from services import (
    add_book,
    async_load_books,
    delete_book,
    display_statistics,
    issue_book,
    return_book,
    search_book,
    view_books,
)
from utils import (
    Colors,
    get_input,
    get_int_input,
    print_book_table_header,
    print_divider,
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
    format_book_row,
)


# ── Sub-menus ─────────────────────────────────────────────────────────────────

def handle_add_book() -> None:
    """Collect inputs and call add_book()."""
    print_header("Add New Book")
    try:
        book_id          = get_input("Enter Book ID         : ")
        title            = get_input("Enter Title           : ")
        author           = get_input("Enter Author          : ")
        publication_year = get_int_input("Enter Publication Year: ")
        category         = get_input("Enter Category        : ")
        copies           = get_int_input("Enter Number of Copies: ")

        add_book(book_id, title, author, publication_year, category, copies)

    except (DuplicateBookIDException, InvalidInputException) as exc:
        print_error(str(exc))
    except ValueError:
        print_error("Publication year and number of copies must be valid integers.")


def handle_search_book() -> None:
    """Collect search parameters and display results."""
    print_header("Search Books")
    print("  Search by:  1. Book ID   2. Title   3. Author   4. All Fields")
    print_divider()

    try:
        choice = get_int_input("Enter choice (1-4): ")
        field_map = {1: "id", 2: "title", 3: "author", 4: "all"}

        if choice not in field_map:
            raise InvalidInputException("Choose a number between 1 and 4.")

        query = get_input("Enter search term: ")
        if not query:
            raise InvalidInputException("Search term cannot be empty.")

        results = search_book(query, field_map[choice])

        if not results:
            print_warning(f"No books found matching '{query}'.")
            return

        print_info(f"Found {len(results)} result(s) for '{query}':")
        print_book_table_header()
        for idx, book in enumerate(results, start=1):
            print(format_book_row(book, idx))
        print_divider()

    except InvalidInputException as exc:
        print_error(str(exc))
    except ValueError:
        print_error("Please enter a valid number.")


def handle_delete_book() -> None:
    """Collect book ID and call delete_book()."""
    print_header("Delete Book")
    try:
        book_id = get_input("Enter Book ID to delete: ")
        confirm = get_input(f"Are you sure you want to delete '{book_id}'? (yes/no): ")
        if confirm.lower() not in ("yes", "y"):
            print_info("Deletion cancelled.")
            return
        delete_book(book_id)

    except BookNotFoundException as exc:
        print_error(str(exc))


def handle_issue_book() -> None:
    """Collect book ID and call issue_book()."""
    print_header("Issue Book")
    try:
        book_id = get_input("Enter Book ID to issue: ")
        issue_book(book_id)

    except (BookNotFoundException, NoCopiesAvailableException) as exc:
        print_error(str(exc))


def handle_return_book() -> None:
    """Collect book ID and call return_book()."""
    print_header("Return Book")
    try:
        book_id = get_input("Enter Book ID to return: ")
        return_book(book_id)

    except (BookNotFoundException, BookNotIssuedException) as exc:
        print_error(str(exc))


# ── Main menu ─────────────────────────────────────────────────────────────────

MENU = """
  {b}┌─────────────────────────────────────┐{r}
  {b}│      LIBRARY MANAGEMENT SYSTEM      │{r}
  {b}├─────────────────────────────────────┤{r}
  {b}│{r}  1. Add Book                        {b}│{r}
  {b}│{r}  2. View All Books                  {b}│{r}
  {b}│{r}  3. Search Book                     {b}│{r}
  {b}│{r}  4. Delete Book                     {b}│{r}
  {b}│{r}  5. Issue Book                      {b}│{r}
  {b}│{r}  6. Return Book                     {b}│{r}
  {b}│{r}  7. Library Statistics              {b}│{r}
  {b}│{r}  8. Exit                            {b}│{r}
  {b}└─────────────────────────────────────┘{r}
""".format(b=Colors.BLUE + Colors.BOLD, r=Colors.RESET)


def show_menu() -> None:
    print(MENU)


def run() -> None:
    """Main application loop."""
    # Load books asynchronously (simulates DB fetch)
    asyncio.run(async_load_books())

    action_map = {
        1: handle_add_book,
        2: view_books,
        3: handle_search_book,
        4: handle_delete_book,
        5: handle_issue_book,
        6: handle_return_book,
        7: display_statistics,
    }

    while True:
        show_menu()
        try:
            choice = get_int_input("Enter your choice (1-8): ")

            if choice == 8:
                print_success("Thank you for using the Library Management System. Goodbye!")
                sys.exit(0)

            handler = action_map.get(choice)
            if handler is None:
                print_error("Invalid choice. Please enter a number between 1 and 8.")
            else:
                handler()

        except ValueError:
            print_error("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n")
            print_info("Interrupted. Press 8 to exit cleanly.")


if __name__ == "__main__":
    run()
