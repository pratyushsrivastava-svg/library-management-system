"""
Pydantic models for data validation in the Library Management System.
"""

from datetime import datetime
from pydantic import BaseModel, field_validator, Field


CURRENT_YEAR = datetime.now().year


class Book(BaseModel):
    """
    Pydantic model for a library book.
    Validates all fields on creation.
    """

    book_id: str = Field(..., description="Unique identifier for the book")
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    publication_year: int = Field(..., description="Year the book was published")
    category: str = Field(..., description="Genre or category of the book")
    total_copies: int = Field(..., description="Total number of copies owned by the library")
    available_copies: int = Field(..., description="Number of copies currently available")

    @field_validator("book_id")
    @classmethod
    def book_id_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Book ID cannot be empty.")
        return v.strip()

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty.")
        return v.strip()

    @field_validator("author")
    @classmethod
    def author_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Author cannot be empty.")
        return v.strip()

    @field_validator("publication_year")
    @classmethod
    def publication_year_must_be_valid(cls, v: int) -> int:
        if v < 1000 or v > CURRENT_YEAR:
            raise ValueError(
                f"Publication year must be between 1000 and {CURRENT_YEAR}."
            )
        return v

    @field_validator("total_copies")
    @classmethod
    def copies_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Number of copies must be greater than zero.")
        return v

    @field_validator("available_copies")
    @classmethod
    def available_copies_must_be_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Available copies cannot be negative.")
        return v

    def to_dict(self) -> dict:
        """Convert the Book model to a plain dictionary."""
        return self.model_dump()
