"""Low-level HTTP transport with retry, timeout, and error mapping."""

from __future__ import annotations

import asyncio
import enum
import time
from typing import Any

import httpx

from dual_sdk.errors import (
    DualAuthError,
    DualError,
    DualNotFoundError,
    DualRateLimitError,
)

_DEFAULT_BASE_URL = "https://blockv-labs.io"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_BACKOFF = 1.0

_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class AuthMode(enum.Enum):
    """Authentication strategy for API requests.

    - ``API_KEY``: sends ``x-api-key`` header (for long-lived API keys).
    - ``BEARER``: sends ``Authorization: Bearer <token>`` header (for JWTs).
    - ``BOTH``: sends both headers (legacy compatibility; not recommended).
    """

    API_KEY = "api_key"
    BEARER = "bearer"
    BOTH = "both"


def _error_from_response(resp: httpx.Response) -> DualError:
    """Build the appropriate DualError subclass from an HTTP response."""
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text}

    message = body.get("message") or body.get("error") or resp.reason_phrase or "Unknown error"
    code = body.get("code") or body.get("error_code") or "UNKNOWN"
    kwargs: dict[str, Any] = {"status": resp.status_code, "code": code, "body": body}

    if resp.status_code == 401:
        return DualAuthError(message, **kwargs)
    if resp.status_code == 404:
        return DualNotFoundError(message, **kwargs)
    if resp.status_code == 429:
        retry_after = resp.headers.get("retry-after")
        return DualRateLimitError(
            message, retry_after=float(retry_after) if retry_after else None, **kwargs
        )
    return DualError(message, **kwargs)


def _build_auth_headers(api_key: str, auth_mode: AuthMode) -> dict[str, str]:
    """Build authentication headers based on the chosen strategy."""
    headers: dict[str, str] = {}
    if auth_mode in (AuthMode.API_KEY, AuthMode.BOTH):
        headers["x-api-key"] = api_key
    if auth_mode in (AuthMode.BEARER, AuthMode.BOTH):
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _prepare_request_kwargs(
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: Any | None = None,
    files: Any | None = None,
) -> dict[str, Any]:
    """Prepare keyword arguments for an httpx request.

    When ``files`` is provided, we omit ``json`` and let httpx set the
    ``Content-Type: multipart/form-data`` boundary automatically.
    Any ``data`` dict is passed alongside ``files`` as form fields.
    """
    kwargs: dict[str, Any] = {}

    if params:
        kwargs["params"] = {k: v for k, v in params.items() if v is not None}

    if files is not None:
        # Multipart upload — httpx handles Content-Type automatically.
        kwargs["files"] = files
        if data is not None:
            kwargs["data"] = data
    elif json is not None:
        kwargs["json"] = json
    elif data is not None:
        kwargs["data"] = data

    return kwargs


class Transport:
    """Synchronous HTTP transport using httpx.

    Args:
        api_key: API key or JWT token.
        auth_mode: How to send credentials (default: ``API_KEY``).
        base_url: API base URL.
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts on transient errors.
        backoff: Base backoff in seconds (doubles each attempt).
        headers: Additional headers merged into every request.
    """

    def __init__(
        self,
        *,
        api_key: str,
        auth_mode: AuthMode = AuthMode.API_KEY,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        backoff: float = _DEFAULT_BACKOFF,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._api_key = api_key
        self._auth_mode = auth_mode
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._backoff = backoff

        default_headers: dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": "dual-sdk-python/0.1.0",
        }
        default_headers.update(_build_auth_headers(api_key, auth_mode))
        if headers:
            default_headers.update(headers)

        self._client = httpx.Client(
            base_url=self._base_url,
            headers=default_headers,
            timeout=httpx.Timeout(timeout),
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
        files: Any | None = None,
    ) -> Any:
        """Execute an HTTP request with automatic retry on transient failures."""
        req_kwargs = _prepare_request_kwargs(
            params=params, json=json, data=data, files=files
        )
        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                resp = self._client.request(method, path, **req_kwargs)

                if resp.status_code >= 400:
                    err = _error_from_response(resp)
                    if resp.status_code in _RETRYABLE_STATUS and attempt < self._max_retries:
                        last_error = err
                        wait = self._backoff * (2**attempt)
                        if isinstance(err, DualRateLimitError) and err.retry_after:
                            wait = err.retry_after
                        time.sleep(wait)
                        continue
                    raise err

                if resp.status_code == 204:
                    return None
                return resp.json()

            except httpx.TransportError as exc:
                last_error = exc
                if attempt < self._max_retries:
                    time.sleep(self._backoff * (2**attempt))
                    continue
                raise DualError(
                    f"Transport error after {self._max_retries + 1} attempts: {exc}",
                    status=0,
                    code="TRANSPORT_ERROR",
                ) from exc

        raise last_error  # type: ignore[misc]

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Transport:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncTransport:
    """Asynchronous HTTP transport using httpx.

    Same interface as :class:`Transport` but uses ``httpx.AsyncClient``.
    """

    def __init__(
        self,
        *,
        api_key: str,
        auth_mode: AuthMode = AuthMode.API_KEY,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        backoff: float = _DEFAULT_BACKOFF,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._api_key = api_key
        self._auth_mode = auth_mode
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._backoff = backoff

        default_headers: dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": "dual-sdk-python/0.1.0",
        }
        default_headers.update(_build_auth_headers(api_key, auth_mode))
        if headers:
            default_headers.update(headers)

        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=default_headers,
            timeout=httpx.Timeout(timeout),
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
        files: Any | None = None,
    ) -> Any:
        """Execute an async HTTP request with automatic retry."""
        req_kwargs = _prepare_request_kwargs(
            params=params, json=json, data=data, files=files
        )
        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                resp = await self._client.request(method, path, **req_kwargs)

                if resp.status_code >= 400:
                    err = _error_from_response(resp)
                    if resp.status_code in _RETRYABLE_STATUS and attempt < self._max_retries:
                        last_error = err
                        wait = self._backoff * (2**attempt)
                        if isinstance(err, DualRateLimitError) and err.retry_after:
                            wait = err.retry_after
                        await asyncio.sleep(wait)
                        continue
                    raise err

                if resp.status_code == 204:
                    return None
                return resp.json()

            except httpx.TransportError as exc:
                last_error = exc
                if attempt < self._max_retries:
                    await asyncio.sleep(self._backoff * (2**attempt))
                    continue
                raise DualError(
                    f"Transport error after {self._max_retries + 1} attempts: {exc}",
                    status=0,
                    code="TRANSPORT_ERROR",
                ) from exc

        raise last_error  # type: ignore[misc]

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncTransport:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
