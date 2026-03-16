"""Low-level HTTP transport with retry, timeout, and error mapping."""

from __future__ import annotations

import asyncio
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


class Transport:
    """Synchronous HTTP transport using httpx."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        backoff: float = _DEFAULT_BACKOFF,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._backoff = backoff

        default_headers = {
            "x-api-key": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "dual-sdk-python/1.0.0",
        }
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
        last_error: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                kwargs: dict[str, Any] = {}
                if params:
                    kwargs["params"] = {k: v for k, v in params.items() if v is not None}
                if json is not None:
                    kwargs["json"] = json
                if data is not None:
                    kwargs["data"] = data
                if files is not None:
                    kwargs["files"] = files
                    # Remove Content-Type for multipart uploads
                    kwargs["headers"] = {"Content-Type": ""}

                resp = self._client.request(method, path, **kwargs)

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
    """Asynchronous HTTP transport using httpx."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        backoff: float = _DEFAULT_BACKOFF,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._backoff = backoff

        default_headers = {
            "x-api-key": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "dual-sdk-python/1.0.0",
        }
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
        last_error: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                kwargs: dict[str, Any] = {}
                if params:
                    kwargs["params"] = {k: v for k, v in params.items() if v is not None}
                if json is not None:
                    kwargs["json"] = json
                if data is not None:
                    kwargs["data"] = data
                if files is not None:
                    kwargs["files"] = files
                    kwargs["headers"] = {"Content-Type": ""}

                resp = await self._client.request(method, path, **kwargs)

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
