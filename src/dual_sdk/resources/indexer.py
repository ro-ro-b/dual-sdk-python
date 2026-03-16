"""Indexer resource — public API for browsing objects and templates."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse, _parse_list
from dual_sdk.models import Face, Object, Organization, PaginatedResponse, PublicStats, Template


class Indexer(SyncResource):
    """Synchronous indexer client (7 endpoints)."""

    def templates(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Template]:
        """List public templates with cursor pagination."""
        data = self._get("/public/templates", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Template], data)

    def get_template(self, template_id: str) -> Template:
        """Get a public template by ID."""
        return _parse(Template, self._get(f"/public/templates/{template_id}"))

    def get_object(self, object_id: str) -> Object:
        """Get a public object by ID."""
        return _parse(Object, self._get(f"/public/objects/{object_id}"))

    def search_objects(self, query: dict[str, Any]) -> PaginatedResponse[Object]:
        """Search public objects."""
        data = self._post("/public/objects/search", json=query)
        return _parse(PaginatedResponse[Object], data)

    def faces_by_template(self, template_id: str) -> list[Face]:
        """Get public faces for a template."""
        return _parse_list(Face, self._get(f"/public/faces/template/{template_id}"))

    def get_organization(self, org_id: str) -> Organization:
        """Get organization details."""
        return _parse(Organization, self._get(f"/public/organizations/{org_id}"))

    def stats(self) -> PublicStats:
        """Get global statistics."""
        return _parse(PublicStats, self._get("/public/stats"))


class AsyncIndexer(AsyncResource):
    """Asynchronous indexer client (7 endpoints)."""

    async def templates(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Template]:
        data = await self._get("/public/templates", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Template], data)

    async def get_template(self, template_id: str) -> Template:
        return _parse(Template, await self._get(f"/public/templates/{template_id}"))

    async def get_object(self, object_id: str) -> Object:
        return _parse(Object, await self._get(f"/public/objects/{object_id}"))

    async def search_objects(self, query: dict[str, Any]) -> PaginatedResponse[Object]:
        data = await self._post("/public/objects/search", json=query)
        return _parse(PaginatedResponse[Object], data)

    async def faces_by_template(self, template_id: str) -> list[Face]:
        return _parse_list(Face, await self._get(f"/public/faces/template/{template_id}"))

    async def get_organization(self, org_id: str) -> Organization:
        return _parse(Organization, await self._get(f"/public/organizations/{org_id}"))

    async def stats(self) -> PublicStats:
        return _parse(PublicStats, await self._get("/public/stats"))
