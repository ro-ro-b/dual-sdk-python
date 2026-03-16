"""Objects resource — create, list, transfer, state management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Objects(SyncResource):
    """Synchronous objects client (9 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None, **params: Any) -> dict[str, Any]:
        """List objects with cursor pagination."""
        return self._get("/objects", params={"limit": limit, "next": next, **params})

    def get(self, object_id: str) -> dict[str, Any]:
        """Get an object by ID."""
        return self._get(f"/objects/{object_id}")

    def create(self, *, template_id: str, properties: dict[str, Any] | None = None, **fields: Any) -> dict[str, Any]:
        """Create an object from a template."""
        return self._post("/objects", json={"template_id": template_id, "properties": properties or {}, **fields})

    def update(self, object_id: str, **fields: Any) -> dict[str, Any]:
        """Update an existing object."""
        return self._patch(f"/objects/{object_id}", json=fields)

    def children(self, object_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """Get child objects."""
        return self._get(f"/objects/{object_id}/children", params={"limit": limit, "next": next})

    def parents(self, object_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """Get parent objects."""
        return self._get(f"/objects/{object_id}/parents", params={"limit": limit, "next": next})

    def activity(self, object_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """Get activity log for an object."""
        return self._get(f"/objects/{object_id}/activity", params={"limit": limit, "next": next})

    def search(self, query: dict[str, Any]) -> dict[str, Any]:
        """Search objects with a query payload."""
        return self._post("/objects/search", json=query)

    def count(self, query: dict[str, Any]) -> dict[str, Any]:
        """Count objects matching a query."""
        return self._post("/objects/count", json=query)


class AsyncObjects(AsyncResource):
    """Asynchronous objects client (9 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None, **params: Any) -> dict[str, Any]:
        return await self._get("/objects", params={"limit": limit, "next": next, **params})

    async def get(self, object_id: str) -> dict[str, Any]:
        return await self._get(f"/objects/{object_id}")

    async def create(self, *, template_id: str, properties: dict[str, Any] | None = None, **fields: Any) -> dict[str, Any]:
        return await self._post("/objects", json={"template_id": template_id, "properties": properties or {}, **fields})

    async def update(self, object_id: str, **fields: Any) -> dict[str, Any]:
        return await self._patch(f"/objects/{object_id}", json=fields)

    async def children(self, object_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get(f"/objects/{object_id}/children", params={"limit": limit, "next": next})

    async def parents(self, object_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get(f"/objects/{object_id}/parents", params={"limit": limit, "next": next})

    async def activity(self, object_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get(f"/objects/{object_id}/activity", params={"limit": limit, "next": next})

    async def search(self, query: dict[str, Any]) -> dict[str, Any]:
        return await self._post("/objects/search", json=query)

    async def count(self, query: dict[str, Any]) -> dict[str, Any]:
        return await self._post("/objects/count", json=query)
