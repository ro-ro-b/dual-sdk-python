"""Objects resource — create, list, transfer, state management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import (
    Action,
    CreateObjectRequest,
    Object,
    ObjectCount,
    ObjectQuery,
    PaginatedResponse,
    UpdateObjectRequest,
)


class Objects(SyncResource):
    """Synchronous objects client (9 endpoints)."""

    def list(
        self, *, limit: int = 20, next: str | None = None, **params: Any
    ) -> PaginatedResponse[Object]:
        """List objects with cursor pagination."""
        data = self._get("/objects", params={"limit": limit, "next": next, **params})
        return _parse(PaginatedResponse[Object], data)

    def get(self, object_id: str) -> Object:
        """Get an object by ID."""
        return _parse(Object, self._get(f"/objects/{object_id}"))

    def create(self, body: CreateObjectRequest | dict[str, Any]) -> Object:
        """Create an object from a template.

        Accepts a :class:`CreateObjectRequest` or a plain dict.
        """
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, CreateObjectRequest) else body
        )
        return _parse(Object, self._post("/objects", json=payload))

    def update(self, object_id: str, body: UpdateObjectRequest | dict[str, Any]) -> Object:
        """Update an existing object.

        Accepts an :class:`UpdateObjectRequest` or a plain dict.
        """
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, UpdateObjectRequest) else body
        )
        return _parse(Object, self._patch(f"/objects/{object_id}", json=payload))

    def children(
        self, object_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Object]:
        """Get child objects."""
        data = self._get(f"/objects/{object_id}/children", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Object], data)

    def parents(
        self, object_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Object]:
        """Get parent objects."""
        data = self._get(f"/objects/{object_id}/parents", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Object], data)

    def activity(
        self, object_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Action]:
        """Get activity log for an object."""

        data = self._get(f"/objects/{object_id}/activity", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Action], data)

    def search(self, query: ObjectQuery | dict[str, Any]) -> PaginatedResponse[Object]:
        """Search objects with a query payload.

        Accepts an :class:`ObjectQuery` or a plain dict.
        """
        payload = query.model_dump(exclude_none=True) if isinstance(query, ObjectQuery) else query
        data = self._post("/objects/search", json=payload)
        return _parse(PaginatedResponse[Object], data)

    def count(self, query: ObjectQuery | dict[str, Any]) -> ObjectCount:
        """Count objects matching a query.

        Accepts an :class:`ObjectQuery` or a plain dict.
        """
        payload = query.model_dump(exclude_none=True) if isinstance(query, ObjectQuery) else query
        return _parse(ObjectCount, self._post("/objects/count", json=payload))


class AsyncObjects(AsyncResource):
    """Asynchronous objects client (9 endpoints)."""

    async def list(
        self, *, limit: int = 20, next: str | None = None, **params: Any
    ) -> PaginatedResponse[Object]:
        data = await self._get("/objects", params={"limit": limit, "next": next, **params})
        return _parse(PaginatedResponse[Object], data)

    async def get(self, object_id: str) -> Object:
        return _parse(Object, await self._get(f"/objects/{object_id}"))

    async def create(self, body: CreateObjectRequest | dict[str, Any]) -> Object:
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, CreateObjectRequest) else body
        )
        return _parse(Object, await self._post("/objects", json=payload))

    async def update(self, object_id: str, body: UpdateObjectRequest | dict[str, Any]) -> Object:
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, UpdateObjectRequest) else body
        )
        return _parse(Object, await self._patch(f"/objects/{object_id}", json=payload))

    async def children(
        self, object_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Object]:
        data = await self._get(
            f"/objects/{object_id}/children", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[Object], data)

    async def parents(
        self, object_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Object]:
        data = await self._get(
            f"/objects/{object_id}/parents", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[Object], data)

    async def activity(
        self, object_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Action]:
        data = await self._get(
            f"/objects/{object_id}/activity", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[Action], data)

    async def search(self, query: ObjectQuery | dict[str, Any]) -> PaginatedResponse[Object]:
        payload = query.model_dump(exclude_none=True) if isinstance(query, ObjectQuery) else query
        data = await self._post("/objects/search", json=payload)
        return _parse(PaginatedResponse[Object], data)

    async def count(self, query: ObjectQuery | dict[str, Any]) -> ObjectCount:
        payload = query.model_dump(exclude_none=True) if isinstance(query, ObjectQuery) else query
        return _parse(ObjectCount, await self._post("/objects/count", json=payload))
