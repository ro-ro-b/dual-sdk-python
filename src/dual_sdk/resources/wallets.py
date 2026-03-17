"""Wallets resource — authentication, registration, and wallet management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import TokenPair, Wallet


class Wallets(SyncResource):
    """Synchronous wallets client (14 endpoints)."""

    def login(self, email: str, password: str) -> TokenPair:
        """Authenticate with email and password. Returns access + refresh tokens."""
        data = self._post("/wallets/login", json={"email": email, "password": password})
        return _parse(TokenPair, data)

    def guest_login(self) -> TokenPair:
        """Create a guest session."""
        return _parse(TokenPair, self._post("/wallets/login/guest"))

    def register(self, email: str, password: str, **kwargs: Any) -> TokenPair:
        """Register a new wallet."""
        return _parse(
            TokenPair,
            self._post("/wallets/register", json={"email": email, "password": password, **kwargs}),
        )

    def verify_registration(self, token: str) -> TokenPair:
        """Verify registration with confirmation token."""
        return _parse(TokenPair, self._post("/wallets/register/verify", json={"token": token}))

    def request_reset_code(self, email: str) -> dict[str, Any]:
        """Request a password reset code."""
        return self._post("/wallets/reset-code", json={"email": email})

    def verify_reset_code(self, code: str, new_password: str) -> dict[str, Any]:
        """Verify reset code and set new password."""
        return self._post(
            "/wallets/reset-code/verify", json={"code": code, "new_password": new_password}
        )

    def me(self) -> Wallet:
        """Get the current authenticated wallet."""
        return _parse(Wallet, self._get("/wallets/me"))

    def update_me(self, **fields: Any) -> Wallet:
        """Update the current wallet's profile."""
        return _parse(Wallet, self._patch("/wallets/me", json=fields))

    def delete_me(self) -> None:
        """Delete the current wallet."""
        self._delete("/wallets/me")

    def linked(self) -> list[Wallet]:
        """Get wallets linked to the current wallet."""
        data = self._get("/wallets/me/linked")
        if isinstance(data, dict):
            data = data.get("payload", data)
        items = (
            data
            if isinstance(data, list)
            else data.get("items", [])
            if isinstance(data, dict)
            else []
        )
        return [Wallet.model_validate(w) for w in items]

    def get(self, wallet_id: str) -> Wallet:
        """Get a wallet by ID."""
        return _parse(Wallet, self._get(f"/wallets/{wallet_id}"))

    def get_linked(self, wallet_id: str) -> list[Wallet]:
        """Get linked wallets for a specific wallet."""
        data = self._get(f"/wallets/{wallet_id}/linked")
        if isinstance(data, dict):
            data = data.get("payload", data)
        items = (
            data
            if isinstance(data, list)
            else data.get("items", [])
            if isinstance(data, dict)
            else []
        )
        return [Wallet.model_validate(w) for w in items]

    def link(self, **kwargs: Any) -> Wallet:
        """Link an external wallet."""
        return _parse(Wallet, self._post("/wallets/link", json=kwargs))

    def refresh_token(self, refresh_token: str) -> TokenPair:
        """Refresh the access token."""
        return _parse(
            TokenPair, self._post("/wallets/token/refresh", json={"refresh_token": refresh_token})
        )


class AsyncWallets(AsyncResource):
    """Asynchronous wallets client (14 endpoints)."""

    async def login(self, email: str, password: str) -> TokenPair:
        """Authenticate with email and password. Returns access + refresh tokens."""
        data = await self._post("/wallets/login", json={"email": email, "password": password})
        return _parse(TokenPair, data)

    async def guest_login(self) -> TokenPair:
        """Create a guest session."""
        return _parse(TokenPair, await self._post("/wallets/login/guest"))

    async def register(self, email: str, password: str, **kwargs: Any) -> TokenPair:
        """Register a new wallet."""
        return _parse(
            TokenPair,
            await self._post(
                "/wallets/register", json={"email": email, "password": password, **kwargs}
            ),
        )

    async def verify_registration(self, token: str) -> TokenPair:
        """Verify registration with confirmation token."""
        return _parse(
            TokenPair, await self._post("/wallets/register/verify", json={"token": token})
        )

    async def request_reset_code(self, email: str) -> dict[str, Any]:
        """Request a password reset code."""
        return await self._post("/wallets/reset-code", json={"email": email})

    async def verify_reset_code(self, code: str, new_password: str) -> dict[str, Any]:
        """Verify reset code and set new password."""
        return await self._post(
            "/wallets/reset-code/verify", json={"code": code, "new_password": new_password}
        )

    async def me(self) -> Wallet:
        """Get the current authenticated wallet."""
        return _parse(Wallet, await self._get("/wallets/me"))

    async def update_me(self, **fields: Any) -> Wallet:
        """Update the current wallet's profile."""
        return _parse(Wallet, await self._patch("/wallets/me", json=fields))

    async def delete_me(self) -> None:
        """Delete the current wallet."""
        await self._delete("/wallets/me")

    async def linked(self) -> list[Wallet]:
        """Get wallets linked to the current wallet."""
        data = await self._get("/wallets/me/linked")
        if isinstance(data, dict):
            data = data.get("payload", data)
        items = (
            data
            if isinstance(data, list)
            else data.get("items", [])
            if isinstance(data, dict)
            else []
        )
        return [Wallet.model_validate(w) for w in items]

    async def get(self, wallet_id: str) -> Wallet:
        """Get a wallet by ID."""
        return _parse(Wallet, await self._get(f"/wallets/{wallet_id}"))

    async def get_linked(self, wallet_id: str) -> list[Wallet]:
        """Get linked wallets for a specific wallet."""
        data = await self._get(f"/wallets/{wallet_id}/linked")
        if isinstance(data, dict):
            data = data.get("payload", data)
        items = (
            data
            if isinstance(data, list)
            else data.get("items", [])
            if isinstance(data, dict)
            else []
        )
        return [Wallet.model_validate(w) for w in items]

    async def link(self, **kwargs: Any) -> Wallet:
        """Link an external wallet."""
        return _parse(Wallet, await self._post("/wallets/link", json=kwargs))

    async def refresh_token(self, refresh_token: str) -> TokenPair:
        """Refresh the access token."""
        return _parse(
            TokenPair,
            await self._post("/wallets/token/refresh", json={"refresh_token": refresh_token}),
        )
