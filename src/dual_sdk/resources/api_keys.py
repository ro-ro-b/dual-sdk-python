"""ApiKeys resource — API key management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse, _parse_list
from dual_sdk.models import ApiKey


class ApiKeys(SyncResource):
    """Synchronous API keys client (3 endpoints)."""

    def list(self) -> list[ApiKey]:
        """List all API keys."""
        return _parse_list(ApiKey, self._get("/api-keys"))

    def create(self, *, name: str | None = None, **fields: Any) -> ApiKey:
        """Create a new API key."""
        return _parse(ApiKey, self._post("/api-keys", json={"name": name, **fields}))

    def delete(self, api_key_id: str) -> None:
        """Delete an API key."""
        self._delete(f"/api-keys/{api_key_id}")


class AsyncApiKeys(AsyncResource):
    """Asynchronous API keys client (3 endpoints)."""

    async def list(self) -> list[ApiKey]:
        return _parse_list(ApiKey, await self._get("/api-keys"))

    async def create(self, *, name: str | None = None, **fields: Any) -> ApiKey:
        return _parse(ApiKey, await self._post("/api-keys", json={"name": name, **fields}))

    async def delete(self, api_key_id: str) -> None:
        await self._delete(f"/api-keys/{api_key_id}")
