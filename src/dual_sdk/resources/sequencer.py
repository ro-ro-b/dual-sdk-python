"""Sequencer resource — batch and checkpoint tracking."""

from __future__ import annotations

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import Batch, Checkpoint, PaginatedResponse


class Sequencer(SyncResource):
    """Synchronous sequencer client (4 endpoints)."""

    def list_batches(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Batch]:
        """List batches with cursor pagination."""
        data = self._get("/batches", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Batch], data)

    def get_batch(self, batch_id: str) -> Batch:
        """Get a batch by ID."""
        return _parse(Batch, self._get(f"/batches/{batch_id}"))

    def list_checkpoints(
        self, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Checkpoint]:
        """List checkpoints with cursor pagination."""
        data = self._get("/checkpoints", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Checkpoint], data)

    def get_checkpoint(self, checkpoint_id: str) -> Checkpoint:
        """Get a checkpoint by ID."""
        return _parse(Checkpoint, self._get(f"/checkpoints/{checkpoint_id}"))


class AsyncSequencer(AsyncResource):
    """Asynchronous sequencer client (4 endpoints)."""

    async def list_batches(
        self, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Batch]:
        data = await self._get("/batches", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Batch], data)

    async def get_batch(self, batch_id: str) -> Batch:
        return _parse(Batch, await self._get(f"/batches/{batch_id}"))

    async def list_checkpoints(
        self, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Checkpoint]:
        data = await self._get("/checkpoints", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Checkpoint], data)

    async def get_checkpoint(self, checkpoint_id: str) -> Checkpoint:
        return _parse(Checkpoint, await self._get(f"/checkpoints/{checkpoint_id}"))
