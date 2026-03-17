"""Support resource — support requests and messaging."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import PaginatedResponse, StatusResult, SupportMessage


class Support(SyncResource):
    """Synchronous support client (4 endpoints)."""

    def request_access(self, *, feature: str, reason: str | None = None) -> StatusResult:
        """Request access to a feature."""
        return _parse(
            StatusResult,
            self._post("/support/request-access", json={"feature": feature, "reason": reason}),
        )

    def list_messages(
        self, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[SupportMessage]:
        """List support messages with cursor pagination."""
        data = self._get("/support", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[SupportMessage], data)

    def send_message(self, *, content: str, **fields: Any) -> SupportMessage:
        """Send a support message."""
        return _parse(SupportMessage, self._post("/support", json={"content": content, **fields}))

    def get_message(self, message_id: str) -> SupportMessage:
        """Get a support message by ID."""
        return _parse(SupportMessage, self._get(f"/support/{message_id}"))


class AsyncSupport(AsyncResource):
    """Asynchronous support client (4 endpoints)."""

    async def request_access(self, *, feature: str, reason: str | None = None) -> StatusResult:
        return _parse(
            StatusResult,
            await self._post(
                "/support/request-access", json={"feature": feature, "reason": reason}
            ),
        )

    async def list_messages(
        self, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[SupportMessage]:
        data = await self._get("/support", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[SupportMessage], data)

    async def send_message(self, *, content: str, **fields: Any) -> SupportMessage:
        return _parse(
            SupportMessage, await self._post("/support", json={"content": content, **fields})
        )

    async def get_message(self, message_id: str) -> SupportMessage:
        return _parse(SupportMessage, await self._get(f"/support/{message_id}"))
