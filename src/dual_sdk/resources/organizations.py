"""Organizations resource — org management, members, roles, invitations."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse, _parse_list
from dual_sdk.models import (
    AcceptInvitationResult,
    Balance,
    BalanceTransaction,
    Invitation,
    Member,
    Organization,
    PaginatedResponse,
    Role,
)


class Organizations(SyncResource):
    """Synchronous organizations client (18 endpoints)."""

    def list(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Organization]:
        data = self._get("/organizations", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Organization], data)

    def create(self, *, name: str, description: str | None = None, **fields: Any) -> Organization:
        body: dict[str, Any] = {"name": name, **fields}
        if description is not None:
            body["description"] = description
        return _parse(Organization, self._post("/organizations", json=body))

    def get(self, org_id: str) -> Organization:
        return _parse(Organization, self._get(f"/organizations/{org_id}"))

    def update(
        self,
        org_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        **fields: Any,
    ) -> Organization:
        body: dict[str, Any] = {**fields}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        return _parse(Organization, self._put(f"/organizations/{org_id}", json=body))

    def balance(self, org_id: str) -> Balance:
        return _parse(Balance, self._get(f"/organizations/{org_id}/balance"))

    def balance_history(
        self, org_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[BalanceTransaction]:
        data = self._get(
            f"/organizations/{org_id}/balance/history", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[BalanceTransaction], data)

    # ── Members ──

    def list_members(
        self, org_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Member]:
        data = self._get(f"/organizations/{org_id}/members", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Member], data)

    def add_member(self, org_id: str, *, wallet_id: str, role: str | None = None) -> Member:
        body: dict[str, Any] = {"wallet_id": wallet_id}
        if role:
            body["role"] = role
        return _parse(Member, self._post(f"/organizations/{org_id}/members", json=body))

    def remove_member(self, org_id: str, member_id: str) -> None:
        self._delete(f"/organizations/{org_id}/members/{member_id}")

    def update_member_role(self, org_id: str, member_id: str, *, role: str) -> Member:
        return _parse(
            Member, self._patch(f"/organizations/{org_id}/members/{member_id}", json={"role": role})
        )

    # ── Roles ──

    def list_roles(self, org_id: str) -> list[Role]:
        return _parse_list(Role, self._get(f"/organizations/{org_id}/roles"))

    def create_role(self, org_id: str, *, name: str, permissions: list[str] | None = None) -> Role:
        return _parse(
            Role,
            self._post(
                f"/organizations/{org_id}/roles",
                json={"name": name, "permissions": permissions or []},
            ),
        )

    def update_role(
        self,
        org_id: str,
        role_id: str,
        *,
        name: str | None = None,
        permissions: list[str] | None = None,
        **fields: Any,
    ) -> Role:
        body: dict[str, Any] = {**fields}
        if name is not None:
            body["name"] = name
        if permissions is not None:
            body["permissions"] = permissions
        return _parse(Role, self._patch(f"/organizations/{org_id}/roles/{role_id}", json=body))

    def delete_role(self, org_id: str, role_id: str) -> None:
        self._delete(f"/organizations/{org_id}/roles/{role_id}")

    # ── Invitations ──

    def invite(self, org_id: str, *, email: str, role: str | None = None) -> Invitation:
        body: dict[str, Any] = {"email": email}
        if role:
            body["role"] = role
        return _parse(Invitation, self._post(f"/organizations/{org_id}/invitations", json=body))

    def list_invitations(self, org_id: str) -> list[Invitation]:
        return _parse_list(Invitation, self._get(f"/organizations/{org_id}/invitations"))

    def delete_invitation(self, org_id: str, invitation_id: str) -> None:
        self._delete(f"/organizations/{org_id}/invitations/{invitation_id}")

    def accept_invitation(self, invitation_id: str) -> AcceptInvitationResult:
        return _parse(
            AcceptInvitationResult,
            self._post(f"/organizations/invitations/{invitation_id}/accept"),
        )


class AsyncOrganizations(AsyncResource):
    """Asynchronous organizations client (18 endpoints)."""

    async def list(
        self, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Organization]:
        data = await self._get("/organizations", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Organization], data)

    async def create(
        self, *, name: str, description: str | None = None, **fields: Any
    ) -> Organization:
        body: dict[str, Any] = {"name": name, **fields}
        if description is not None:
            body["description"] = description
        return _parse(Organization, await self._post("/organizations", json=body))

    async def get(self, org_id: str) -> Organization:
        return _parse(Organization, await self._get(f"/organizations/{org_id}"))

    async def update(
        self,
        org_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        **fields: Any,
    ) -> Organization:
        body: dict[str, Any] = {**fields}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        return _parse(Organization, await self._put(f"/organizations/{org_id}", json=body))

    async def balance(self, org_id: str) -> Balance:
        return _parse(Balance, await self._get(f"/organizations/{org_id}/balance"))

    async def balance_history(
        self, org_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[BalanceTransaction]:
        data = await self._get(
            f"/organizations/{org_id}/balance/history", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[BalanceTransaction], data)

    async def list_members(
        self, org_id: str, *, limit: int = 20, next: str | None = None
    ) -> PaginatedResponse[Member]:
        data = await self._get(
            f"/organizations/{org_id}/members", params={"limit": limit, "next": next}
        )
        return _parse(PaginatedResponse[Member], data)

    async def add_member(self, org_id: str, *, wallet_id: str, role: str | None = None) -> Member:
        body: dict[str, Any] = {"wallet_id": wallet_id}
        if role:
            body["role"] = role
        return _parse(Member, await self._post(f"/organizations/{org_id}/members", json=body))

    async def remove_member(self, org_id: str, member_id: str) -> None:
        await self._delete(f"/organizations/{org_id}/members/{member_id}")

    async def update_member_role(self, org_id: str, member_id: str, *, role: str) -> Member:
        return _parse(
            Member,
            await self._patch(f"/organizations/{org_id}/members/{member_id}", json={"role": role}),
        )

    async def list_roles(self, org_id: str) -> list[Role]:
        return _parse_list(Role, await self._get(f"/organizations/{org_id}/roles"))

    async def create_role(
        self, org_id: str, *, name: str, permissions: list[str] | None = None
    ) -> Role:
        return _parse(
            Role,
            await self._post(
                f"/organizations/{org_id}/roles",
                json={"name": name, "permissions": permissions or []},
            ),
        )

    async def update_role(
        self,
        org_id: str,
        role_id: str,
        *,
        name: str | None = None,
        permissions: list[str] | None = None,
        **fields: Any,
    ) -> Role:
        body: dict[str, Any] = {**fields}
        if name is not None:
            body["name"] = name
        if permissions is not None:
            body["permissions"] = permissions
        return _parse(
            Role, await self._patch(f"/organizations/{org_id}/roles/{role_id}", json=body)
        )

    async def delete_role(self, org_id: str, role_id: str) -> None:
        await self._delete(f"/organizations/{org_id}/roles/{role_id}")

    async def invite(self, org_id: str, *, email: str, role: str | None = None) -> Invitation:
        body: dict[str, Any] = {"email": email}
        if role:
            body["role"] = role
        return _parse(
            Invitation, await self._post(f"/organizations/{org_id}/invitations", json=body)
        )

    async def list_invitations(self, org_id: str) -> list[Invitation]:
        return _parse_list(Invitation, await self._get(f"/organizations/{org_id}/invitations"))

    async def delete_invitation(self, org_id: str, invitation_id: str) -> None:
        await self._delete(f"/organizations/{org_id}/invitations/{invitation_id}")

    async def accept_invitation(self, invitation_id: str) -> AcceptInvitationResult:
        return _parse(
            AcceptInvitationResult,
            await self._post(f"/organizations/invitations/{invitation_id}/accept"),
        )
