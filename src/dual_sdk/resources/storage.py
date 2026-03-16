"""Storage resource — file uploads and asset management."""

from __future__ import annotations

from typing import Any

from dual_sdk._base import AsyncResource, SyncResource, _parse, _parse_list
from dual_sdk.models import FileRecord


class Storage(SyncResource):
    """Synchronous storage client (5 endpoints)."""

    def upload(self, *, file: Any, template_id: str | None = None) -> FileRecord:
        """Upload a file. Returns file metadata with ID and URL."""
        data: dict[str, Any] = {}
        if template_id is not None:
            data["template_id"] = template_id
        return _parse(FileRecord, self._post("/storage/upload", files={"file": file}, data=data or None))

    def get(self, file_id: str) -> FileRecord:
        """Get file metadata by ID."""
        return _parse(FileRecord, self._get(f"/storage/{file_id}"))

    def delete(self, file_id: str) -> None:
        """Delete a file."""
        self._delete(f"/storage/{file_id}")

    def template_assets(self, template_id: str) -> list[FileRecord]:
        """Get assets associated with a template."""
        return _parse_list(FileRecord, self._get(f"/storage/template/{template_id}"))

    def upload_template_asset(self, template_id: str, *, file: Any) -> FileRecord:
        """Upload an asset for a template."""
        return _parse(FileRecord, self._post(f"/storage/template/{template_id}", files={"file": file}))


class AsyncStorage(AsyncResource):
    """Asynchronous storage client (5 endpoints)."""

    async def upload(self, *, file: Any, template_id: str | None = None) -> FileRecord:
        data: dict[str, Any] = {}
        if template_id is not None:
            data["template_id"] = template_id
        return _parse(FileRecord, await self._post("/storage/upload", files={"file": file}, data=data or None))

    async def get(self, file_id: str) -> FileRecord:
        return _parse(FileRecord, await self._get(f"/storage/{file_id}"))

    async def delete(self, file_id: str) -> None:
        await self._delete(f"/storage/{file_id}")

    async def template_assets(self, template_id: str) -> list[FileRecord]:
        return _parse_list(FileRecord, await self._get(f"/storage/template/{template_id}"))

    async def upload_template_asset(self, template_id: str, *, file: Any) -> FileRecord:
        return _parse(FileRecord, await self._post(f"/storage/template/{template_id}", files={"file": file}))
