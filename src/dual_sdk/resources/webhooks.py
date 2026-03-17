"""Webhooks resource — event subscriptions and webhook management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import PaginatedResponse, Webhook, WebhookTestResult


class Webhooks(SyncResource):
    """Synchronous webhooks client (6 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Webhook]:
        """List webhooks with cursor pagination."""
        data = self._get("/webhooks", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Webhook], data)

    def create(self, *, url: str, events: list[str], **fields: Any) -> Webhook:
        """Create a new webhook subscription."""
        return _parse(
            Webhook, self._post("/webhooks", json={"url": url, "events": events, **fields})
        )

    def get(self, webhook_id: str) -> Webhook:
        """Get a webhook by ID."""
        return _parse(Webhook, self._get(f"/webhooks/{webhook_id}"))

    def update(self, webhook_id: str, **fields: Any) -> Webhook:
        """Update a webhook."""
        return _parse(Webhook, self._patch(f"/webhooks/{webhook_id}", json=fields))

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook."""
        self._delete(f"/webhooks/{webhook_id}")

    def test(self, webhook_id: str) -> WebhookTestResult:
        """Send a test event to a webhook."""
        return _parse(WebhookTestResult, self._post(f"/webhooks/{webhook_id}/test"))


class AsyncWebhooks(AsyncResource):
    """Asynchronous webhooks client (6 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Webhook]:
        data = await self._get("/webhooks", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Webhook], data)

    async def create(self, *, url: str, events: list[str], **fields: Any) -> Webhook:
        return _parse(
            Webhook, await self._post("/webhooks", json={"url": url, "events": events, **fields})
        )

    async def get(self, webhook_id: str) -> Webhook:
        return _parse(Webhook, await self._get(f"/webhooks/{webhook_id}"))

    async def update(self, webhook_id: str, **fields: Any) -> Webhook:
        return _parse(Webhook, await self._patch(f"/webhooks/{webhook_id}", json=fields))

    async def delete(self, webhook_id: str) -> None:
        await self._delete(f"/webhooks/{webhook_id}")

    async def test(self, webhook_id: str) -> WebhookTestResult:
        return _parse(WebhookTestResult, await self._post(f"/webhooks/{webhook_id}/test"))
