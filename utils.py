"""
Utility functions for the Library Management System.
"""

from typing import Any


# ── ANSI color codes ──────────────────────────────────────────────────────────
class Colors:
    HEADER    = "\033[95m"
    BLUE      = "\033[94m"
    CYAN      = "\033[96m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    RED       = "\033[91m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET     = "\033[0m"


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{Colors.GREEN}✔  {message}{Colors.RESET}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{Colors.RED}✘  {message}{Colors.RESET}")


def print_info(message: str) -> None:
    """Print an informational message in cyan."""
    print(f"{Colors.CYAN}ℹ  {message}{Colors.RESET}")


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    print(f"{Colors.YELLOW}⚠  {message}{Colors.RESET}")


def print_header(title: str) -> None:
    """Print a styled section header."""
    width = 60
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(width)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'═' * width}{Colors.RESET}")


def print_divider() -> None:
    """Print a thin horizontal divider."""
    print(f"{Colors.BLUE}{'─' * 60}{Colors.RESET}")


def get_input(prompt: str) -> str:
    """Prompt the user and return stripped input."""
    return input(f"{Colors.YELLOW}{prompt}{Colors.RESET}").strip()


def get_int_input(prompt: str) -> int:
    """
    Prompt the user for an integer.
    Raises ValueError if the input is not a valid integer.
    """
    raw = get_input(prompt)
    if not raw:
        raise ValueError("Input cannot be empty.")
    return int(raw)


def format_book_row(book: dict[str, Any], index: int | None = None) -> str:
    """Return a single formatted string representing a book row."""
    prefix = f"{index:>3}. " if index is not None else "     "
    status_color = Colors.GREEN if book["available_copies"] > 0 else Colors.RED
    status = (
        f"{status_color}{book['available_copies']}/{book['total_copies']}{Colors.RESET}"
    )
    return (
        f"{prefix}{Colors.BOLD}{book['book_id']:<10}{Colors.RESET}"
        f"{book['title']:<30}"
        f"{book['author']:<22}"
        f"{book['publication_year']:<6}"
        f"{book['category']:<16}"
        f"Copies: {status}"
    )


def print_book_table_header() -> None:
    """Print the column header for a book listing."""
    print(
        f"\n{'#':>4}  "
        f"{'ID':<10}"
        f"{'Title':<30}"
        f"{'Author':<22}"
        f"{'Year':<6}"
        f"{'Category':<16}"
        f"Copies (Avail/Total)"
    )
    print_divider()
