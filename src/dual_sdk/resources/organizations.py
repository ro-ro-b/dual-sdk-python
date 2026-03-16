"""Organizations resource — org management, members, roles, invitations."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Organizations(SyncResource):
    """Synchronous organizations client (18 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return self._get("/organizations", params={"limit": limit, "next": next})

    def create(self, *, name: str, **fields: Any) -> dict[str, Any]:
        return self._post("/organizations", json={"name": name, **fields})

    def get(self, org_id: str) -> dict[str, Any]:
        return self._get(f"/organizations/{org_id}")

    def update(self, org_id: str, **fields: Any) -> dict[str, Any]:
        return self._put(f"/organizations/{org_id}", json=fields)

    def balance(self, org_id: str) -> dict[str, Any]:
        return self._get(f"/organizations/{org_id}/balance")

    def balance_history(self, org_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return self._get(f"/organizations/{org_id}/balance/history", params={"limit": limit, "next": next})

    # ── Members ──

    def list_members(self, org_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return self._get(f"/organizations/{org_id}/members", params={"limit": limit, "next": next})

    def add_member(self, org_id: str, *, wallet_id: str, role: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"wallet_id": wallet_id}
        if role:
            body["role"] = role
        return self._post(f"/organizations/{org_id}/members", json=body)

    def remove_member(self, org_id: str, member_id: str) -> None:
        self._delete(f"/organizations/{org_id}/members/{member_id}")

    def update_member_role(self, org_id: str, member_id: str, *, role: str) -> dict[str, Any]:
        return self._patch(f"/organizations/{org_id}/members/{member_id}", json={"role": role})

    # ── Roles ──

    def list_roles(self, org_id: str) -> dict[str, Any]:
        return self._get(f"/organizations/{org_id}/roles")

    def create_role(self, org_id: str, *, name: str, permissions: list[str] | None = None) -> dict[str, Any]:
        return self._post(f"/organizations/{org_id}/roles", json={"name": name, "permissions": permissions or []})

    def update_role(self, org_id: str, role_id: str, **fields: Any) -> dict[str, Any]:
        return self._patch(f"/organizations/{org_id}/roles/{role_id}", json=fields)

    def delete_role(self, org_id: str, role_id: str) -> None:
        self._delete(f"/organizations/{org_id}/roles/{role_id}")

    # ── Invitations ──

    def invite(self, org_id: str, *, email: str, role: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"email": email}
        if role:
            body["role"] = role
        return self._post(f"/organizations/{org_id}/invitations", json=body)

    def list_invitations(self, org_id: str) -> dict[str, Any]:
        return self._get(f"/organizations/{org_id}/invitations")

    def delete_invitation(self, org_id: str, invitation_id: str) -> None:
        self._delete(f"/organizations/{org_id}/invitations/{invitation_id}")

    def accept_invitation(self, invitation_id: str) -> dict[str, Any]:
        return self._post(f"/organizations/invitations/{invitation_id}/accept")


class AsyncOrganizations(AsyncResource):
    """Asynchronous organizations client (18 endpoints)."""

    async def list(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/organizations", params={"limit": limit, "next": next})

    async def create(self, *, name: str, **fields: Any) -> dict[str, Any]:
        return await self._post("/organizations", json={"name": name, **fields})

    async def get(self, org_id: str) -> dict[str, Any]:
        return await self._get(f"/organizations/{org_id}")

    async def update(self, org_id: str, **fields: Any) -> dict[str, Any]:
        return await self._put(f"/organizations/{org_id}", json=fields)

    async def balance(self, org_id: str) -> dict[str, Any]:
        return await self._get(f"/organizations/{org_id}/balance")

    async def balance_history(self, org_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get(f"/organizations/{org_id}/balance/history", params={"limit": limit, "next": next})

    async def list_members(self, org_id: str, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get(f"/organizations/{org_id}/members", params={"limit": limit, "next": next})

    async def add_member(self, org_id: str, *, wallet_id: str, role: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"wallet_id": wallet_id}
        if role:
            body["role"] = role
        return await self._post(f"/organizations/{org_id}/members", json=body)

    async def remove_member(self, org_id: str, member_id: str) -> None:
        await self._delete(f"/organizations/{org_id}/members/{member_id}")

    async def update_member_role(self, org_id: str, member_id: str, *, role: str) -> dict[str, Any]:
        return await self._patch(f"/organizations/{org_id}/members/{member_id}", json={"role": role})

    async def list_roles(self, org_id: str) -> dict[str, Any]:
        return await self._get(f"/organizations/{org_id}/roles")

    async def create_role(self, org_id: str, *, name: str, permissions: list[str] | None = None) -> dict[str, Any]:
        return await self._post(f"/organizations/{org_id}/roles", json={"name": name, "permissions": permissions or []})

    async def update_role(self, org_id: str, role_id: str, **fields: Any) -> dict[str, Any]:
        return await self._patch(f"/organizations/{org_id}/roles/{role_id}", json=fields)

    async def delete_role(self, org_id: str, role_id: str) -> None:
        await self._delete(f"/organizations/{org_id}/roles/{role_id}")

    async def invite(self, org_id: str, *, email: str, role: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"email": email}
        if role:
            body["role"] = role
        return await self._post(f"/organizations/{org_id}/invitations", json=body)

    async def list_invitations(self, org_id: str) -> dict[str, Any]:
        return await self._get(f"/organizations/{org_id}/invitations")

    async def delete_invitation(self, org_id: str, invitation_id: str) -> None:
        await self._delete(f"/organizations/{org_id}/invitations/{invitation_id}")

    async def accept_invitation(self, invitation_id: str) -> dict[str, Any]:
        return await self._post(f"/organizations/invitations/{invitation_id}/accept")
