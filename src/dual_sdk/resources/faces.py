"""Faces resource — face registration and management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse, _parse_list
from dual_sdk.models import Face, PaginatedResponse


class Faces(SyncResource):
    """Synchronous faces client (6 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Face]:
        """List faces with cursor pagination."""
        data = self._get("/faces", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Face], data)

    def create(self, **fields: Any) -> Face:
        """Create a new face."""
        return _parse(Face, self._post("/faces", json=fields))

    def get(self, face_id: str) -> Face:
        """Get a face by ID."""
        return _parse(Face, self._get(f"/faces/{face_id}"))

    def update(self, face_id: str, **fields: Any) -> Face:
        """Update a face."""
        return _parse(Face, self._patch(f"/faces/{face_id}", json=fields))

    def delete(self, face_id: str) -> None:
        """Delete a face."""
        self._delete(f"/faces/{face_id}")

    def by_template(self, template_id: str) -> list[Face]:
        """Get faces associated with a template."""
        return _parse_list(Face, self._get(f"/faces/template/{template_id}"))


class AsyncFaces(AsyncResource):
    """Asynchronous faces client (6 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Face]:
        data = await self._get("/faces", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Face], data)

    async def create(self, **fields: Any) -> Face:
        return _parse(Face, await self._post("/faces", json=fields))

    async def get(self, face_id: str) -> Face:
        return _parse(Face, await self._get(f"/faces/{face_id}"))

    async def update(self, face_id: str, **fields: Any) -> Face:
        return _parse(Face, await self._patch(f"/faces/{face_id}", json=fields))

    async def delete(self, face_id: str) -> None:
        await self._delete(f"/faces/{face_id}")

    async def by_template(self, template_id: str) -> list[Face]:
        return _parse_list(Face, await self._get(f"/faces/template/{template_id}"))
