"""Sequencer resource — batch and checkpoint tracking."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Sequencer(SyncResource):
    """Synchronous sequencer client (4 endpoints)."""

    def list_batches(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List batches with cursor pagination."""
        return self._get("/batches", params={"limit": limit, "next": next})

    def get_batch(self, batch_id: str) -> dict[str, Any]:
        """Get a batch by ID."""
        return self._get(f"/batches/{batch_id}")

    def list_checkpoints(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List checkpoints with cursor pagination."""
        return self._get("/checkpoints", params={"limit": limit, "next": next})

    def get_checkpoint(self, checkpoint_id: str) -> dict[str, Any]:
        """Get a checkpoint by ID."""
        return self._get(f"/checkpoints/{checkpoint_id}")


class AsyncSequencer(AsyncResource):
    """Asynchronous sequencer client (4 endpoints)."""

    async def list_batches(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/batches", params={"limit": limit, "next": next})

    async def get_batch(self, batch_id: str) -> dict[str, Any]:
        return await self._get(f"/batches/{batch_id}")

    async def list_checkpoints(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/checkpoints", params={"limit": limit, "next": next})

    async def get_checkpoint(self, checkpoint_id: str) -> dict[str, Any]:
        return await self._get(f"/checkpoints/{checkpoint_id}")
