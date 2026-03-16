"""Storage resource — file uploads, templates, and asset management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource


class Storage(SyncResource):
    """Synchronous storage client (5 endpoints)."""

    def upload(self, *, file: Any, template_id: str | None = None) -> dict[str, Any]:
        """Upload a file. Returns file metadata with ID."""
        data = {}
        if template_id is not None:
            data["template_id"] = template_id
        return self._post("/storage/upload", files={"file": file}, data=data)

    def get(self, file_id: str) -> dict[str, Any]:
        """Get file metadata by ID."""
        return self._get(f"/storage/{file_id}")

    def delete(self, file_id: str) -> None:
        """Delete a file."""
        self._delete(f"/storage/{file_id}")

    def template_assets(self, template_id: str) -> dict[str, Any]:
        """Get assets associated with a template."""
        return self._get(f"/storage/template/{template_id}")

    def upload_template_asset(self, template_id: str, *, file: Any) -> dict[str, Any]:
        """Upload an asset for a template."""
        return self._post(f"/storage/template/{template_id}", files={"file": file})


class AsyncStorage(AsyncResource):
    """Asynchronous storage client (5 endpoints)."""

    async def upload(self, *, file: Any, template_id: str | None = None) -> dict[str, Any]:
        data = {}
        if template_id is not None:
            data["template_id"] = template_id
        return await self._post("/storage/upload", files={"file": file}, data=data)

    async def get(self, file_id: str) -> dict[str, Any]:
        return await self._get(f"/storage/{file_id}")

    async def delete(self, file_id: str) -> None:
        await self._delete(f"/storage/{file_id}")

    async def template_assets(self, template_id: str) -> dict[str, Any]:
        return await self._get(f"/storage/template/{template_id}")

    async def upload_template_asset(self, template_id: str, *, file: Any) -> dict[str, Any]:
        return await self._post(f"/storage/template/{template_id}", files={"file": file})
