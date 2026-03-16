"""Support resource — support requests and messaging."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Support(SyncResource):
    """Synchronous support client (4 endpoints)."""

    def request_access(self, *, feature: str, reason: str | None = None) -> dict[str, Any]:
        """Request access to a feature."""
        return self._post("/support/request-access", json={"feature": feature, "reason": reason})

    def list_messages(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List support messages with cursor pagination."""
        return self._get("/support", params={"limit": limit, "next": next})

    def send_message(self, *, content: str, **fields: Any) -> dict[str, Any]:
        """Send a support message."""
        return self._post("/support", json={"content": content, **fields})

    def get_message(self, message_id: str) -> dict[str, Any]:
        """Get a support message by ID."""
        return self._get(f"/support/{message_id}")


class AsyncSupport(AsyncResource):
    """Asynchronous support client (4 endpoints)."""

    async def request_access(self, *, feature: str, reason: str | None = None) -> dict[str, Any]:
        return await self._post("/support/request-access", json={"feature": feature, "reason": reason})

    async def list_messages(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/support", params={"limit": limit, "next": next})

    async def send_message(self, *, content: str, **fields: Any) -> dict[str, Any]:
        return await self._post("/support", json={"content": content, **fields})

    async def get_message(self, message_id: str) -> dict[str, Any]:
        return await self._get(f"/support/{message_id}")
