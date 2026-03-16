"""Notifications resource — message templates and notification delivery."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Notifications(SyncResource):
    """Synchronous notifications client (7 endpoints)."""

    def list_messages(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List messages with cursor pagination."""
        return self._get("/messages", params={"limit": limit, "next": next})

    def send(self, *, content: str, **fields: Any) -> dict[str, Any]:
        """Send a message."""
        return self._post("/messages/send", json={"content": content, **fields})

    def list_templates(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List message templates with cursor pagination."""
        return self._get("/messages/templates", params={"limit": limit, "next": next})

    def get_template(self, template_id: str) -> dict[str, Any]:
        """Get a message template by ID."""
        return self._get(f"/messages/templates/{template_id}")

    def create_template(self, *, name: str, body: str, **fields: Any) -> dict[str, Any]:
        """Create a new message template."""
        return self._post("/messages/templates", json={"name": name, "body": body, **fields})

    def update_template(self, template_id: str, **fields: Any) -> dict[str, Any]:
        """Update a message template."""
        return self._patch(f"/messages/templates/{template_id}", json=fields)

    def delete_template(self, template_id: str) -> None:
        """Delete a message template."""
        self._delete(f"/messages/templates/{template_id}")


class AsyncNotifications(AsyncResource):
    """Asynchronous notifications client (7 endpoints)."""

    async def list_messages(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/messages", params={"limit": limit, "next": next})

    async def send(self, *, content: str, **fields: Any) -> dict[str, Any]:
        return await self._post("/messages/send", json={"content": content, **fields})

    async def list_templates(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/messages/templates", params={"limit": limit, "next": next})

    async def get_template(self, template_id: str) -> dict[str, Any]:
        return await self._get(f"/messages/templates/{template_id}")

    async def create_template(self, *, name: str, body: str, **fields: Any) -> dict[str, Any]:
        return await self._post("/messages/templates", json={"name": name, "body": body, **fields})

    async def update_template(self, template_id: str, **fields: Any) -> dict[str, Any]:
        return await self._patch(f"/messages/templates/{template_id}", json=fields)

    async def delete_template(self, template_id: str) -> None:
        await self._delete(f"/messages/templates/{template_id}")
