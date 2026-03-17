"""Templates resource — CRUD, search, and variations."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import (
    CreateTemplateRequest,
    PaginatedResponse,
    Template,
    UpdateTemplateRequest,
    Variation,
)


class Templates(SyncResource):
    """Synchronous templates client (7 endpoints)."""

    def list(
        self, *, limit: int = 20, next: str | None = None, **params: Any
    ) -> PaginatedResponse[Template]:
        """List templates with cursor pagination."""
        data = self._get("/templates", params={"limit": limit, "next": next, **params})
        return _parse(PaginatedResponse[Template], data)

    def create(self, body: CreateTemplateRequest | dict[str, Any]) -> Template:
        """Create a new template.

        Accepts a :class:`CreateTemplateRequest` or a plain dict.
        """
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, CreateTemplateRequest) else body
        )
        return _parse(Template, self._post("/templates", json=payload))

    def get(self, template_id: str) -> Template:
        """Get a template by ID."""
        return _parse(Template, self._get(f"/templates/{template_id}"))

    def update(self, template_id: str, body: UpdateTemplateRequest | dict[str, Any]) -> Template:
        """Update an existing template.

        Accepts an :class:`UpdateTemplateRequest` or a plain dict.
        """
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, UpdateTemplateRequest) else body
        )
        return _parse(Template, self._patch(f"/templates/{template_id}", json=payload))

    def delete(self, template_id: str) -> None:
        """Delete a template."""
        self._delete(f"/templates/{template_id}")

    def list_variations(
        self, template_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Variation]:
        """List variations for a template."""
        data = self._get(
            f"/templates/{template_id}/variations", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[Variation], data)

    def create_variation(self, template_id: str, body: dict[str, Any]) -> Variation:
        """Create a variation on a template."""
        return _parse(
            Variation,
            self._post(f"/templates/{template_id}/variations", json=body),
        )


class AsyncTemplates(AsyncResource):
    """Asynchronous templates client (7 endpoints)."""

    async def list(
        self, *, limit: int = 20, next: str | None = None, **params: Any
    ) -> PaginatedResponse[Template]:
        data = await self._get("/templates", params={"limit": limit, "next": next, **params})
        return _parse(PaginatedResponse[Template], data)

    async def create(self, body: CreateTemplateRequest | dict[str, Any]) -> Template:
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, CreateTemplateRequest) else body
        )
        return _parse(Template, await self._post("/templates", json=payload))

    async def get(self, template_id: str) -> Template:
        return _parse(Template, await self._get(f"/templates/{template_id}"))

    async def update(
        self, template_id: str, body: UpdateTemplateRequest | dict[str, Any]
    ) -> Template:
        payload = (
            body.model_dump(exclude_none=True) if isinstance(body, UpdateTemplateRequest) else body
        )
        return _parse(Template, await self._patch(f"/templates/{template_id}", json=payload))

    async def delete(self, template_id: str) -> None:
        await self._delete(f"/templates/{template_id}")

    async def list_variations(
        self, template_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Variation]:
        data = await self._get(
            f"/templates/{template_id}/variations", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[Variation], data)

    async def create_variation(self, template_id: str, body: dict[str, Any]) -> Variation:
        return _parse(
            Variation,
            await self._post(f"/templates/{template_id}/variations", json=body),
        )
