"""EventBus resource — event actions and action type management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class EventBus(SyncResource):
    """Synchronous event bus client (8 endpoints)."""

    def execute(self, *, action_type: str, payload: dict[str, Any] | None = None, **fields: Any) -> dict[str, Any]:
        """Execute a single action."""
        return self._post("/ebus/actions", json={"action_type": action_type, "payload": payload or {}, **fields})

    def list_actions(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List executed actions with cursor pagination."""
        return self._get("/ebus/actions", params={"limit": limit, "next": next})

    def get_action(self, action_id: str) -> dict[str, Any]:
        """Get an action by ID."""
        return self._get(f"/ebus/actions/{action_id}")

    def execute_batch(self, actions: list[dict[str, Any]]) -> dict[str, Any]:
        """Execute multiple actions in a batch."""
        return self._post("/ebus/actions/batch", json={"actions": actions})

    def list_action_types(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        """List action types with cursor pagination."""
        return self._get("/ebus/action-types", params={"limit": limit, "next": next})

    def create_action_type(self, *, name: str, **fields: Any) -> dict[str, Any]:
        """Create a new action type."""
        return self._post("/ebus/action-types", json={"name": name, **fields})

    def get_action_type(self, action_type_id: str) -> dict[str, Any]:
        """Get an action type by ID."""
        return self._get(f"/ebus/action-types/{action_type_id}")

    def update_action_type(self, action_type_id: str, **fields: Any) -> dict[str, Any]:
        """Update an action type."""
        return self._put(f"/ebus/action-types/{action_type_id}", json=fields)


class AsyncEventBus(AsyncResource):
    """Asynchronous event bus client (8 endpoints)."""

    async def execute(
        self, *, action_type: str, payload: dict[str, Any] | None = None, **fields: Any
    ) -> dict[str, Any]:
        return await self._post("/ebus/actions", json={"action_type": action_type, "payload": payload or {}, **fields})

    async def list_actions(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/ebus/actions", params={"limit": limit, "next": next})

    async def get_action(self, action_id: str) -> dict[str, Any]:
        return await self._get(f"/ebus/actions/{action_id}")

    async def execute_batch(self, actions: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._post("/ebus/actions/batch", json={"actions": actions})

    async def list_action_types(self, *, limit: int = 20, next: str | None = None) -> dict[str, Any]:
        return await self._get("/ebus/action-types", params={"limit": limit, "next": next})

    async def create_action_type(self, *, name: str, **fields: Any) -> dict[str, Any]:
        return await self._post("/ebus/action-types", json={"name": name, **fields})

    async def get_action_type(self, action_type_id: str) -> dict[str, Any]:
        return await self._get(f"/ebus/action-types/{action_type_id}")

    async def update_action_type(self, action_type_id: str, **fields: Any) -> dict[str, Any]:
        return await self._put(f"/ebus/action-types/{action_type_id}", json=fields)
