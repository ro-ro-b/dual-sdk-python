"""Payments resource — deposit tracking and payment configuration."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Payments(SyncResource):
    """Synchronous payments client (2 endpoints)."""

    def config(self) -> dict[str, Any]:
        """Get payment configuration."""
        return self._get("/payments/config")

    def list_deposits(
        self,
        *,
        tx_hash: str | None = None,
        token: str | None = None,
        token_address: str | None = None,
    ) -> dict[str, Any]:
        """List deposits with optional filtering."""
        return self._get(
            "/payments/deposits",
            params={"tx_hash": tx_hash, "token": token, "token_address": token_address},
        )


class AsyncPayments(AsyncResource):
    """Asynchronous payments client (2 endpoints)."""

    async def config(self) -> dict[str, Any]:
        return await self._get("/payments/config")

    async def list_deposits(
        self,
        *,
        tx_hash: str | None = None,
        token: str | None = None,
        token_address: str | None = None,
    ) -> dict[str, Any]:
        return await self._get(
            "/payments/deposits",
            params={"tx_hash": tx_hash, "token": token, "token_address": token_address},
        )
