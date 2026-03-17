"""Payments resource — deposit tracking and payment configuration."""

from __future__ import annotations

from dual_sdk._base import AsyncResource, SyncResource, _parse, _parse_list
from dual_sdk.models import Deposit, PaymentConfig


class Payments(SyncResource):
    """Synchronous payments client (2 endpoints)."""

    def config(self) -> PaymentConfig:
        """Get payment configuration."""
        return _parse(PaymentConfig, self._get("/payments/config"))

    def list_deposits(
        self,
        *,
        tx_hash: str | None = None,
        token: str | None = None,
        token_address: str | None = None,
    ) -> list[Deposit]:
        """List deposits with optional filtering."""
        data = self._get(
            "/payments/deposits",
            params={"tx_hash": tx_hash, "token": token, "token_address": token_address},
        )
        return _parse_list(Deposit, data)


class AsyncPayments(AsyncResource):
    """Asynchronous payments client (2 endpoints)."""

    async def config(self) -> PaymentConfig:
        return _parse(PaymentConfig, await self._get("/payments/config"))

    async def list_deposits(
        self,
        *,
        tx_hash: str | None = None,
        token: str | None = None,
        token_address: str | None = None,
    ) -> list[Deposit]:
        data = await self._get(
            "/payments/deposits",
            params={"tx_hash": tx_hash, "token": token, "token_address": token_address},
        )
        return _parse_list(Deposit, data)
