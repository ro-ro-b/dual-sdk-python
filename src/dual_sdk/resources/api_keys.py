"""ApiKeys resource — API key management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class ApiKeys(SyncResource):
    """Synchronous API keys client (3 endpoints)."""

    def list(self) -> dict[str, Any]:
        """List all API keys."""
        return self._get("/api-keys")

    def create(self, *, name: str | None = None, **fields: Any) -> dict[str, Any]:
        """Create a new API key."""
        return self._post("/api-keys", json={"name": name, **fields})

    def delete(self, api_key_id: str) -> None:
        """Delete an API key."""
        self._delete(f"/api-keys/{api_key_id}")


class AsyncApiKeys(AsyncResource):
    """Asynchronous API keys client (3 endpoints)."""

    async def list(self) -> dict[str, Any]:
        return await self._get("/api-keys")

    async def create(self, *, name: str | None = None, **fields: Any) -> dict[str, Any]:
        return await self._post("/api-keys", json={"name": name, **fields})

    async def delete(self, api_key_id: str) -> None:
        await self._delete(f"/api-keys/{api_key_id}")
