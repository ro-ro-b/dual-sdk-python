"""Indexer resource — public API for browsing objects and templates."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Indexer(SyncResource):
    """Synchronous indexer client (7 endpoints)."""

    def templates(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List public templates with cursor pagination."""
        return self._get("/public/templates", params={"limit": limit, "next": next})

    def get_template(self, template_id: str) -> dict[str, Any]:
        """Get a public template by ID."""
        return self._get(f"/public/templates/{template_id}")

    def get_object(self, object_id: str) -> dict[str, Any]:
        """Get a public object by ID."""
        return self._get(f"/public/objects/{object_id}")

    def search_objects(self, query: dict[str, Any]) -> dict[str, Any]:
        """Search public objects."""
        return self._post("/public/objects/search", json=query)

    def faces_by_template(self, template_id: str) -> dict[str, Any]:
        """Get public faces for a template."""
        return self._get(f"/public/faces/template/{template_id}")

    def get_organization(self, org_id: str) -> dict[str, Any]:
        """Get organization details."""
        return self._get(f"/public/organizations/{org_id}")

    def stats(self) -> dict[str, Any]:
        """Get global statistics."""
        return self._get("/public/stats")


class AsyncIndexer(AsyncResource):
    """Asynchronous indexer client (7 endpoints)."""

    async def templates(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/public/templates", params={"limit": limit, "next": next})

    async def get_template(self, template_id: str) -> dict[str, Any]:
        return await self._get(f"/public/templates/{template_id}")

    async def get_object(self, object_id: str) -> dict[str, Any]:
        return await self._get(f"/public/objects/{object_id}")

    async def search_objects(self, query: dict[str, Any]) -> dict[str, Any]:
        return await self._post("/public/objects/search", json=query)

    async def faces_by_template(self, template_id: str) -> dict[str, Any]:
        return await self._get(f"/public/faces/template/{template_id}")

    async def get_organization(self, org_id: str) -> dict[str, Any]:
        return await self._get(f"/public/organizations/{org_id}")

    async def stats(self) -> dict[str, Any]:
        return await self._get("/public/stats")
