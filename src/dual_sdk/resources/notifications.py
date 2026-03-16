"""Notifications resource — message templates and notification delivery."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import Message, MessageTemplate, PaginatedResponse


class Notifications(SyncResource):
    """Synchronous notifications client (7 endpoints)."""

    def list_messages(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Message]:
        """List messages with cursor pagination."""
        data = self._get("/messages", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Message], data)

    def send(self, *, content: str, **fields: Any) -> Message:
        """Send a message."""
        return _parse(Message, self._post("/messages/send", json={"content": content, **fields}))

    def list_templates(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[MessageTemplate]:
        """List message templates with cursor pagination."""
        data = self._get("/messages/templates", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[MessageTemplate], data)

    def get_template(self, template_id: str) -> MessageTemplate:
        """Get a message template by ID."""
        return _parse(MessageTemplate, self._get(f"/messages/templates/{template_id}"))

    def create_template(self, *, name: str, body: str, **fields: Any) -> MessageTemplate:
        """Create a new message template."""
        return _parse(MessageTemplate, self._post("/messages/templates", json={"name": name, "body": body, **fields}))

    def update_template(self, template_id: str, **fields: Any) -> MessageTemplate:
        """Update a message template."""
        return _parse(MessageTemplate, self._patch(f"/messages/templates/{template_id}", json=fields))

    def delete_template(self, template_id: str) -> None:
        """Delete a message template."""
        self._delete(f"/messages/templates/{template_id}")


class AsyncNotifications(AsyncResource):
    """Asynchronous notifications client (7 endpoints)."""

    async def list_messages(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Message]:
        data = await self._get("/messages", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Message], data)

    async def send(self, *, content: str, **fields: Any) -> Message:
        return _parse(Message, await self._post("/messages/send", json={"content": content, **fields}))

    async def list_templates(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[MessageTemplate]:
        data = await self._get("/messages/templates", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[MessageTemplate], data)

    async def get_template(self, template_id: str) -> MessageTemplate:
        return _parse(MessageTemplate, await self._get(f"/messages/templates/{template_id}"))

    async def create_template(self, *, name: str, body: str, **fields: Any) -> MessageTemplate:
        return _parse(MessageTemplate, await self._post("/messages/templates", json={"name": name, "body": body, **fields}))

    async def update_template(self, template_id: str, **fields: Any) -> MessageTemplate:
        return _parse(MessageTemplate, await self._patch(f"/messages/templates/{template_id}", json=fields))

    async def delete_template(self, template_id: str) -> None:
        await self._delete(f"/messages/templates/{template_id}")
