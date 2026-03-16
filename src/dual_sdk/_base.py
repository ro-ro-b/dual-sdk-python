"""Base class for all resource modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from dual_sdk._transport import AsyncTransport, Transport

M = TypeVar("M", bound=BaseModel)


def _parse(model: Type[M], data: Any) -> M:
    """Parse a raw API response dict into a Pydantic model.

    The DUAL API typically wraps payloads in a ``"payload"`` key.
    This helper checks for that wrapper, falling through to the
    raw dict if the key is absent.
    """
    if isinstance(data, dict):
        data = data.get("payload", data)
    return model.model_validate(data)


def _parse_list(model: Type[M], data: Any) -> list[M]:
    """Parse a list of items from an API response into Pydantic models."""
    if isinstance(data, dict):
        data = data.get("payload", data)
    if isinstance(data, list):
        return [model.model_validate(item) for item in data]
    if isinstance(data, dict) and "items" in data:
        return [model.model_validate(item) for item in data["items"]]
    return []


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
