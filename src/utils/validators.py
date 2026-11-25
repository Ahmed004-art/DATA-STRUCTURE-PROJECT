"""Input validation utilities and custom validation exceptions."""

from __future__ import annotations


class ValidationError(ValueError):
    """Raised when user or caller input fails validation rules."""


def parse_positive_int(raw_value: str | int, field_name: str = "value") -> int:
    """Parse and validate a strictly positive integer (> 0).

    Rejects booleans, floats, zero, negative numbers, and non-numeric strings.
    """
    if isinstance(raw_value, bool):
        raise ValidationError(f"Invalid {field_name}: boolean is not a valid integer.")

    if isinstance(raw_value, int):
        value = raw_value
    elif isinstance(raw_value, str):
        stripped = raw_value.strip()
        if not stripped:
            raise ValidationError(f"Invalid {field_name}: input cannot be empty.")
        try:
            value = int(stripped)
        except ValueError as exc:
            raise ValidationError(
                f"Invalid {field_name}: '{raw_value}' is not a valid integer."
            ) from exc
    else:
        raise ValidationError(
            f"Invalid {field_name}: expected an integer, got {type(raw_value).__name__}."
        )

    if value <= 0:
        raise ValidationError(
            f"Invalid {field_name}: must be a positive integer (>= 1), got {value}."
        )
    return value
