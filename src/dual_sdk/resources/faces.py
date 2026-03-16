"""Faces resource — NFT faces and identity management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Faces(SyncResource):
    """Synchronous faces client (6 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List faces with cursor pagination."""
        return self._get("/faces", params={"limit": limit, "next": next})

    def create(self, **fields: Any) -> dict[str, Any]:
        """Create a new face."""
        return self._post("/faces", json=fields)

    def get(self, face_id: str) -> dict[str, Any]:
        """Get a face by ID."""
        return self._get(f"/faces/{face_id}")

    def update(self, face_id: str, **fields: Any) -> dict[str, Any]:
        """Update a face."""
        return self._patch(f"/faces/{face_id}", json=fields)

    def delete(self, face_id: str) -> None:
        """Delete a face."""
        self._delete(f"/faces/{face_id}")

    def by_template(self, template_id: str) -> dict[str, Any]:
        """Get faces associated with a template."""
        return self._get(f"/faces/template/{template_id}")


class AsyncFaces(AsyncResource):
    """Asynchronous faces client (6 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/faces", params={"limit": limit, "next": next})

    async def create(self, **fields: Any) -> dict[str, Any]:
        return await self._post("/faces", json=fields)

    async def get(self, face_id: str) -> dict[str, Any]:
        return await self._get(f"/faces/{face_id}")

    async def update(self, face_id: str, **fields: Any) -> dict[str, Any]:
        return await self._patch(f"/faces/{face_id}", json=fields)

    async def delete(self, face_id: str) -> None:
        await self._delete(f"/faces/{face_id}")

    async def by_template(self, template_id: str) -> dict[str, Any]:
        return await self._get(f"/faces/template/{template_id}")
