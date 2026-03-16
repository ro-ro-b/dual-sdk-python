"""Webhooks resource — event subscriptions and webhook management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Webhooks(SyncResource):
    """Synchronous webhooks client (6 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List webhooks with cursor pagination."""
        return self._get("/webhooks", params={"limit": limit, "next": next})

    def create(self, *, url: str, events: list[str], **fields: Any) -> dict[str, Any]:
        """Create a new webhook subscription."""
        return self._post("/webhooks", json={"url": url, "events": events, **fields})

    def get(self, webhook_id: str) -> dict[str, Any]:
        """Get a webhook by ID."""
        return self._get(f"/webhooks/{webhook_id}")

    def update(self, webhook_id: str, **fields: Any) -> dict[str, Any]:
        """Update a webhook."""
        return self._patch(f"/webhooks/{webhook_id}", json=fields)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook."""
        self._delete(f"/webhooks/{webhook_id}")

    def test(self, webhook_id: str) -> dict[str, Any]:
        """Send a test event to a webhook."""
        return self._post(f"/webhooks/{webhook_id}/test")


class AsyncWebhooks(AsyncResource):
    """Asynchronous webhooks client (6 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/webhooks", params={"limit": limit, "next": next})

    async def create(self, *, url: str, events: list[str], **fields: Any) -> dict[str, Any]:
        return await self._post("/webhooks", json={"url": url, "events": events, **fields})

    async def get(self, webhook_id: str) -> dict[str, Any]:
        return await self._get(f"/webhooks/{webhook_id}")

    async def update(self, webhook_id: str, **fields: Any) -> dict[str, Any]:
        return await self._patch(f"/webhooks/{webhook_id}", json=fields)

    async def delete(self, webhook_id: str) -> None:
        await self._delete(f"/webhooks/{webhook_id}")

    async def test(self, webhook_id: str) -> dict[str, Any]:
        return await self._post(f"/webhooks/{webhook_id}/test")
