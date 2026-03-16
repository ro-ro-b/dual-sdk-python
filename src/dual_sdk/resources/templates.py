"""Templates resource — CRUD, search, and variations."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Templates(SyncResource):
    """Synchronous templates client (7 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None, **params: Any) -> dict[str, Any]:
        """List templates with cursor pagination."""
        return self._get("/templates", params={"limit": limit, "next": next, **params})

    def create(self, *, name: str, **fields: Any) -> dict[str, Any]:
        """Create a new template."""
        return self._post("/templates", json={"name": name, **fields})

    def get(self, template_id: str) -> dict[str, Any]:
        """Get a template by ID."""
        return self._get(f"/templates/{template_id}")

    def update(self, template_id: str, **fields: Any) -> dict[str, Any]:
        """Update an existing template."""
        return self._patch(f"/templates/{template_id}", json=fields)

    def delete(self, template_id: str) -> None:
        """Delete a template."""
        self._delete(f"/templates/{template_id}")

    def list_variations(self, template_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List variations for a template."""
        return self._get(f"/templates/{template_id}/variations", params={"limit": limit, "next": next})

    def create_variation(self, template_id: str, *, name: str, **fields: Any) -> dict[str, Any]:
        """Create a variation on a template."""
        return self._post(f"/templates/{template_id}/variations", json={"name": name, **fields})


class AsyncTemplates(AsyncResource):
    """Asynchronous templates client (7 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None, **params: Any) -> dict[str, Any]:
        return await self._get("/templates", params={"limit": limit, "next": next, **params})

    async def create(self, *, name: str, **fields: Any) -> dict[str, Any]:
        return await self._post("/templates", json={"name": name, **fields})

    async def get(self, template_id: str) -> dict[str, Any]:
        return await self._get(f"/templates/{template_id}")

    async def update(self, template_id: str, **fields: Any) -> dict[str, Any]:
        return await self._patch(f"/templates/{template_id}", json=fields)

    async def delete(self, template_id: str) -> None:
        await self._delete(f"/templates/{template_id}")

    async def list_variations(self, template_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get(f"/templates/{template_id}/variations", params={"limit": limit, "next": next})

    async def create_variation(self, template_id: str, *, name: str, **fields: Any) -> dict[str, Any]:
        return await self._post(f"/templates/{template_id}/variations", json={"name": name, **fields})
