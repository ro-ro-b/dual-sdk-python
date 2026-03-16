"""EventBus resource — event actions and action type management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse
from dual_sdk.models import Action, ActionType, PaginatedResponse


class EventBus(SyncResource):
    """Synchronous event bus client (8 endpoints)."""

    def execute(self, *, action_type: str, payload: dict[str, Any] | None = None, **fields: Any) -> Action:
        """Execute a single action."""
        return _parse(Action, self._post("/ebus/actions", json={"action_type": action_type, "payload": payload or {}, **fields}))

    def list_actions(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Action]:
        """List executed actions with cursor pagination."""
        data = self._get("/ebus/actions", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Action], data)

    def get_action(self, action_id: str) -> Action:
        """Get an action by ID."""
        return _parse(Action, self._get(f"/ebus/actions/{action_id}"))

    def execute_batch(self, actions: list[dict[str, Any]]) -> list[Action]:
        """Execute multiple actions in a batch."""
        data = self._post("/ebus/actions/batch", json={"actions": actions})
        if isinstance(data, dict):
            data = data.get("payload", data)
        items = data if isinstance(data, list) else data.get("items", []) if isinstance(data, dict) else []
        return [Action.model_validate(a) for a in items]

    def list_action_types(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[ActionType]:
        """List action types with cursor pagination."""
        data = self._get("/ebus/action-types", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[ActionType], data)

    def create_action_type(self, *, name: str, **fields: Any) -> ActionType:
        """Create a new action type."""
        return _parse(ActionType, self._post("/ebus/action-types", json={"name": name, **fields}))

    def get_action_type(self, action_type_id: str) -> ActionType:
        """Get an action type by ID."""
        return _parse(ActionType, self._get(f"/ebus/action-types/{action_type_id}"))

    def update_action_type(self, action_type_id: str, **fields: Any) -> ActionType:
        """Update an action type."""
        return _parse(ActionType, self._put(f"/ebus/action-types/{action_type_id}", json=fields))


class AsyncEventBus(AsyncResource):
    """Asynchronous event bus client (8 endpoints)."""

    async def execute(self, *, action_type: str, payload: dict[str, Any] | None = None, **fields: Any) -> Action:
        return _parse(Action, await self._post("/ebus/actions", json={"action_type": action_type, "payload": payload or {}, **fields}))

    async def list_actions(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[Action]:
        data = await self._get("/ebus/actions", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[Action], data)

    async def get_action(self, action_id: str) -> Action:
        return _parse(Action, await self._get(f"/ebus/actions/{action_id}"))

    async def execute_batch(self, actions: list[dict[str, Any]]) -> list[Action]:
        data = await self._post("/ebus/actions/batch", json={"actions": actions})
        if isinstance(data, dict):
            data = data.get("payload", data)
        items = data if isinstance(data, list) else data.get("items", []) if isinstance(data, dict) else []
        return [Action.model_validate(a) for a in items]

    async def list_action_types(self, *, limit: int = 20, next: str | None = None) -> PaginatedResponse[ActionType]:
        data = await self._get("/ebus/action-types", params={"limit": limit, "next": next})
        return _parse(PaginatedResponse[ActionType], data)

    async def create_action_type(self, *, name: str, **fields: Any) -> ActionType:
        return _parse(ActionType, await self._post("/ebus/action-types", json={"name": name, **fields}))

    async def get_action_type(self, action_type_id: str) -> ActionType:
        return _parse(ActionType, await self._get(f"/ebus/action-types/{action_type_id}"))

    async def update_action_type(self, action_type_id: str, **fields: Any) -> ActionType:
        return _parse(ActionType, await self._put(f"/ebus/action-types/{action_type_id}", json=fields))
