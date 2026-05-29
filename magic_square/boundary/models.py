"""Boundary failure result models."""

from pydantic import BaseModel


class ValidationFailure(BaseModel):
    """Structured validation failure for Boundary layer (AC-FR-01-01 contract)."""

    code: str
    message: str
