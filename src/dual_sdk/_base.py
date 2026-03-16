"""Base class for all resource modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dual_sdk._transport import AsyncTransport, Transport


class SyncResource:
    """Base for synchronous resource modules."""

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def _get(self, path: str, **kwargs: Any) -> Any:
        return self._t.request("GET", path, **kwargs)

    def _post(self, path: str, **kwargs: Any) -> Any:
        return self._t.request("POST", path, **kwargs)

    def _patch(self, path: str, **kwargs: Any) -> Any:
        return self._t.request("PATCH", path, **kwargs)

    def _put(self, path: str, **kwargs: Any) -> Any:
        return self._t.request("PUT", path, **kwargs)

    def _delete(self, path: str, **kwargs: Any) -> Any:
        return self._t.request("DELETE", path, **kwargs)


class AsyncResource:
    """Base for asynchronous resource modules."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def _get(self, path: str, **kwargs: Any) -> Any:
        return await self._t.request("GET", path, **kwargs)

    async def _post(self, path: str, **kwargs: Any) -> Any:
        return await self._t.request("POST", path, **kwargs)

    async def _patch(self, path: str, **kwargs: Any) -> Any:
        return await self._t.request("PATCH", path, **kwargs)

    async def _put(self, path: str, **kwargs: Any) -> Any:
        return await self._t.request("PUT", path, **kwargs)

    async def _delete(self, path: str, **kwargs: Any) -> Any:
        return await self._t.request("DELETE", path, **kwargs)
