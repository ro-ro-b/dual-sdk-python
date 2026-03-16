"""Wallets resource — authentication, registration, and wallet management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Wallets(SyncResource):
    """Synchronous wallets client (14 endpoints)."""

    def login(self, email: str, password: str) -> dict[str, Any]:
        """Authenticate with email and password. Returns access + refresh tokens."""
        return self._post("/wallets/login", json={"email": email, "password": password})

    def guest_login(self) -> dict[str, Any]:
        """Create a guest session."""
        return self._post("/wallets/login/guest")

    def register(self, email: str, password: str, **kwargs: Any) -> dict[str, Any]:
        """Register a new wallet."""
        return self._post("/wallets/register", json={"email": email, "password": password, **kwargs})

    def verify_registration(self, token: str) -> dict[str, Any]:
        """Verify registration with confirmation token."""
        return self._post("/wallets/register/verify", json={"token": token})

    def request_reset_code(self, email: str) -> dict[str, Any]:
        """Request a password reset code."""
        return self._post("/wallets/reset-code", json={"email": email})

    def verify_reset_code(self, code: str, new_password: str) -> dict[str, Any]:
        """Verify reset code and set new password."""
        return self._post("/wallets/reset-code/verify", json={"code": code, "new_password": new_password})

    def me(self) -> dict[str, Any]:
        """Get the current authenticated wallet."""
        return self._get("/wallets/me")

    def update_me(self, **fields: Any) -> dict[str, Any]:
        """Update the current wallet's profile."""
        return self._patch("/wallets/me", json=fields)

    def delete_me(self) -> None:
        """Delete the current wallet."""
        self._delete("/wallets/me")

    def linked(self) -> dict[str, Any]:
        """Get wallets linked to the current wallet."""
        return self._get("/wallets/me/linked")

    def get(self, wallet_id: str) -> dict[str, Any]:
        """Get a wallet by ID."""
        return self._get(f"/wallets/{wallet_id}")

    def get_linked(self, wallet_id: str) -> dict[str, Any]:
        """Get linked wallets for a specific wallet."""
        return self._get(f"/wallets/{wallet_id}/linked")

    def link(self, **kwargs: Any) -> dict[str, Any]:
        """Link an external wallet."""
        return self._post("/wallets/link", json=kwargs)

    def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        """Refresh the access token."""
        return self._post("/wallets/token/refresh", json={"refresh_token": refresh_token})


class AsyncWallets(AsyncResource):
    """Asynchronous wallets client (14 endpoints)."""

    async def login(self, email: str, password: str) -> dict[str, Any]:
        return await self._post("/wallets/login", json={"email": email, "password": password})

    async def guest_login(self) -> dict[str, Any]:
        return await self._post("/wallets/login/guest")

    async def register(self, email: str, password: str, **kwargs: Any) -> dict[str, Any]:
        return await self._post("/wallets/register", json={"email": email, "password": password, **kwargs})

    async def verify_registration(self, token: str) -> dict[str, Any]:
        return await self._post("/wallets/register/verify", json={"token": token})

    async def request_reset_code(self, email: str) -> dict[str, Any]:
        return await self._post("/wallets/reset-code", json={"email": email})

    async def verify_reset_code(self, code: str, new_password: str) -> dict[str, Any]:
        return await self._post("/wallets/reset-code/verify", json={"code": code, "new_password": new_password})

    async def me(self) -> dict[str, Any]:
        return await self._get("/wallets/me")

    async def update_me(self, **fields: Any) -> dict[str, Any]:
        return await self._patch("/wallets/me", json=fields)

    async def delete_me(self) -> None:
        await self._delete("/wallets/me")

    async def linked(self) -> dict[str, Any]:
        return await self._get("/wallets/me/linked")

    async def get(self, wallet_id: str) -> dict[str, Any]:
        return await self._get(f"/wallets/{wallet_id}")

    async def get_linked(self, wallet_id: str) -> dict[str, Any]:
        return await self._get(f"/wallets/{wallet_id}/linked")

    async def link(self, **kwargs: Any) -> dict[str, Any]:
        return await self._post("/wallets/link", json=kwargs)

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        return await self._post("/wallets/token/refresh", json={"refresh_token": refresh_token})
