"""Objects resource — create, list, transfer, state management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import Object, PaginatedResponse


class Objects(SyncResource):
    """Synchronous objects client (9 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None, **params: Any) -> PaginatedResponse[Object]:
        """List objects with cursor pagination."""
        data = self._get("/objects", params={"limit": limit, "next": next, **params})
        return _parse(PaginatedResponse[Object], data)

    def get(self, object_id: str) -> Object:
        """Get an object by ID."""
        return _parse(Object, self._get(f"/objects/{object_id}"))

    def create(self, *, template_id: str, properties: dict[str, Any] | None = None, **fields: Any) -> Object:
        """Create an object from a template."""
        return _parse(Object, self._post("/objects", json={"template_id": template_id, "properties": properties or {}, **fields}))

    def update(self, object_id: str, **fields: Any) -> Object:
        """Update an existing object."""
        return _parse(Object, self._patch(f"/objects/{object_id}", json=fields))

    def children(self, object_id: str, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Object]:
        """Get child objects."""
        data = self._get(f"/objects/{object_id}/children", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Object], data)

    def parents(self, object_id: str, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Object]:
        """Get parent objects."""
        data = self._get(f"/objects/{object_id}/parents", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Object], data)

    def activity(self, object_id: str, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Action]:
        """Get activity log for an object."""
        from dual_sdk.models import Action
        data = self._get(f"/objects/{object_id}/activity", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Action], data)

    def search(self, query: dict[str, Any]) -> PaginatedResponse[Object]:
        """Search objects with a query payload."""
        data = self._post("/objects/search", json=query)
        return _parse(PaginatedResponse[Object], data)

    def count(self, query: dict[str, Any]) -> dict[str, Any]:
        """Count objects matching a query."""
        return self._post("/objects/count", json=query)


class AsyncObjects(AsyncResource):
    """Asynchronous objects client (9 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None, **params: Any) -> PaginatedResponse[Object]:
        data = await self._get("/objects", params={"limit": limit, "next": next, **params})
        return _parse(PaginatedResponse[Object], data)

    async def get(self, object_id: str) -> Object:
        return _parse(Object, await self._get(f"/objects/{object_id}"))

    async def create(self, *, template_id: str, properties: dict[str, Any] | None = None, **fields: Any) -> Object:
        return _parse(Object, await self._post("/objects", json={"template_id": template_id, "properties": properties or {}, **fields}))

    async def update(self, object_id: str, **fields: Any) -> Object:
        return _parse(Object, await self._patch(f"/objects/{object_id}", json=fields))

    async def children(self, object_id: str, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Object]:
        data = await self._get(f"/objects/{object_id}/children", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Object], data)

    async def parents(self, object_id: str, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Object]:
        data = await self._get(f"/objects/{object_id}/parents", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Object], data)

    async def activity(self, object_id: str, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Action]:
        from dual_sdk.models import Action
        data = await self._get(f"/objects/{object_id}/activity", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Action], data)

    async def search(self, query: dict[str, Any]) -> PaginatedResponse[Object]:
        data = await self._post("/objects/search", json=query)
        return _parse(PaginatedResponse[Object], data)

    async def count(self, query: dict[str, Any]) -> dict[str, Any]:
        return await self._post("/objects/count", json=query)
