"""Error types for the DUAL SDK."""

from __future__ import annotations

from typing import Any


class DualError(Exception):
    """Base error raised by the DUAL SDK for all API errors.

    Attributes:
        status: HTTP status code.
        code: Machine-readable error code from the API (e.g. ``"INVALID_TOKEN"``).
        body: Full parsed JSON response body.
        message: Human-readable error message.
    """

    def __init__(
        self,
        message: str,
        *,
        status: int = 0,
        code: str = "UNKNOWN",
        body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.body = body or {}
        self.message = message

    def __repr__(self) -> str:
        return f"DualError(status={self.status}, code={self.code!r}, message={self.message!r})"


class DualAuthError(DualError):
    """Raised on 401 Unauthorized responses."""


class DualNotFoundError(DualError):
    """Raised on 404 Not Found responses."""


class DualRateLimitError(DualError):
    """Raised on 429 Too Many Requests responses.

    Attributes:
        retry_after: Seconds to wait before retrying (if provided by the API).
    """

    def __init__(self, message: str, *, retry_after: float | None = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
