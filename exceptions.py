"""
Custom exceptions for the Library Management System.
"""


class LibraryException(Exception):
    """Base exception for all library-related errors."""
    pass


class BookNotFoundException(LibraryException):
    """Raised when a book with the given ID does not exist in the library."""

    def __init__(self, book_id: str):
        self.book_id = book_id
        super().__init__(f"Book with ID '{book_id}' was not found in the library.")


class DuplicateBookIDException(LibraryException):
    """Raised when trying to add a book with an ID that already exists."""

    def __init__(self, book_id: str):
        self.book_id = book_id
        super().__init__(f"A book with ID '{book_id}' already exists in the library.")


class NoCopiesAvailableException(LibraryException):
    """Raised when trying to issue a book that has no available copies."""

    def __init__(self, title: str):
        self.title = title
        super().__init__(f"No available copies of '{title}' to issue.")


class InvalidInputException(LibraryException):
    """Raised when user provides invalid input."""

    def __init__(self, message: str):
        super().__init__(f"Invalid input: {message}")


class BookNotIssuedException(LibraryException):
    """Raised when trying to return a book that hasn't been issued."""

    def __init__(self, book_id: str):
        self.book_id = book_id
        super().__init__(f"Book with ID '{book_id}' has not been issued, so it cannot be returned.")
