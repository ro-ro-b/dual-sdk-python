"""Tests for the DUAL SDK client initialization, typed returns, and error handling."""

from __future__ import annotations

import pytest
import httpx
from pytest_httpx import HTTPXMock

from dual_sdk import (
    AsyncDualClient,
    AuthMode,
    DualClient,
    DualAuthError,
    DualError,
    DualNotFoundError,
    DualRateLimitError,
    PaginatedResponse,
)
from dual_sdk.models import (
    ApiKey,
    Face,
    FileRecord,
    Object,
    Organization,
    PublicStats,
    Template,
    TokenPair,
    Wallet,
    Webhook,
)


@pytest.fixture
def client() -> DualClient:
    return DualClient(api_key="test-key", base_url="https://test.local", max_retries=0)


@pytest.fixture
def bearer_client() -> DualClient:
    return DualClient(
        api_key="jwt-token",
        auth_mode=AuthMode.BEARER,
        base_url="https://test.local",
        max_retries=0,
    )


# ── Client Init ─────────────────────────────────────────────


class TestClientInit:
    def test_has_all_modules(self, client: DualClient) -> None:
        modules = [
            "wallets", "templates", "objects", "organizations",
            "payments", "storage", "webhooks", "notifications",
            "event_bus", "faces", "sequencer", "indexer",
            "api_keys", "support",
        ]
        for mod in modules:
            assert hasattr(client, mod), f"Missing module: {mod}"

    def test_repr(self, client: DualClient) -> None:
        assert "test.local" in repr(client)

    def test_context_manager(self) -> None:
        with DualClient(api_key="test-key", base_url="https://test.local") as c:
            assert c is not None

    def test_auth_mode_api_key_header(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "w_1", "email": "a@b.com"})
        client.wallets.me()
        req = httpx_mock.get_requests()[0]
        assert req.headers.get("x-api-key") == "test-key"

    def test_auth_mode_bearer_header(self, httpx_mock: HTTPXMock, bearer_client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "w_1", "email": "a@b.com"})
        bearer_client.wallets.me()
        req = httpx_mock.get_requests()[0]
        assert req.headers.get("authorization") == "Bearer jwt-token"


# ── Wallets ──────────────────────────────────────────────────


class TestWallets:
    def test_me_returns_wallet(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "w_123", "email": "user@example.com"})
        wallet = client.wallets.me()
        assert isinstance(wallet, Wallet)
        assert wallet.id == "w_123"
        assert wallet.email == "user@example.com"

    def test_login_returns_token_pair(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"access_token": "tok_abc", "refresh_token": "ref_xyz"})
        result = client.wallets.login("user@example.com", "password123")
        assert isinstance(result, TokenPair)
        assert result.access_token == "tok_abc"
        assert result.refresh_token == "ref_xyz"

    def test_me_with_payload_envelope(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        """API may wrap data in a 'payload' key."""
        httpx_mock.add_response(json={"payload": {"id": "w_456", "email": "test@test.com"}})
        wallet = client.wallets.me()
        assert wallet.id == "w_456"
        assert wallet.email == "test@test.com"

    def test_wallet_extra_fields_preserved(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        """Models should tolerate unknown fields from the API."""
        httpx_mock.add_response(json={"id": "w_1", "email": "a@b.com", "custom_field": "hello"})
        wallet = client.wallets.me()
        assert wallet.id == "w_1"


# ── Templates ────────────────────────────────────────────────


class TestTemplates:
    def test_list_returns_paginated(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            json={"items": [{"id": "t_1", "name": "T1"}, {"id": "t_2", "name": "T2"}], "next": "cursor_abc"},
        )
        result = client.templates.list()
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 2
        assert isinstance(result.items[0], Template)
        assert result.items[0].id == "t_1"
        assert result.cursor == "cursor_abc"
        assert result.next == "cursor_abc"  # .next property aliases .cursor

    def test_list_none_cursor(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"items": [{"id": "t_1", "name": "T1"}], "next": None})
        result = client.templates.list()
        assert result.cursor is None
        assert result.next is None

    def test_create_returns_template(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "t_new", "name": "Test Template"})
        tmpl = client.templates.create(name="Test Template")
        assert isinstance(tmpl, Template)
        assert tmpl.name == "Test Template"

    def test_get_returns_template(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "t_1", "name": "Template One"})
        tmpl = client.templates.get("t_1")
        assert isinstance(tmpl, Template)
        assert tmpl.id == "t_1"

    def test_template_payload_envelope(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"payload": {"id": "t_1", "name": "Wrapped"}})
        tmpl = client.templates.get("t_1")
        assert tmpl.id == "t_1"


# ── Objects ──────────────────────────────────────────────────


class TestObjects:
    def test_create_returns_object(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "o_1", "template_id": "t_1"})
        obj = client.objects.create(template_id="t_1", properties={"name": "Token"})
        assert isinstance(obj, Object)
        assert obj.template_id == "t_1"

    def test_list_returns_paginated(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"items": [{"id": "o_1", "template_id": "t_1"}], "next": None})
        result = client.objects.list()
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 1
        assert isinstance(result.items[0], Object)

    def test_get_returns_object(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "o_1", "template_id": "t_1"})
        obj = client.objects.get("o_1")
        assert isinstance(obj, Object)
        assert obj.id == "o_1"


# ── Organizations ────────────────────────────────────────────


class TestOrganizations:
    def test_create_returns_organization(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "org_1", "name": "Test Org"})
        org = client.organizations.create(name="Test Org")
        assert isinstance(org, Organization)
        assert org.name == "Test Org"

    def test_list_returns_paginated(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"items": [{"id": "org_1", "name": "Org"}], "next": None})
        result = client.organizations.list()
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 1


# ── Faces ────────────────────────────────────────────────────


class TestFaces:
    def test_list_returns_paginated(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"items": [{"id": "f_1", "template_id": "t_1"}], "next": None})
        result = client.faces.list()
        assert isinstance(result, PaginatedResponse)
        assert isinstance(result.items[0], Face)

    def test_get_returns_face(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "f_1", "template_id": "t_1"})
        face = client.faces.get("f_1")
        assert isinstance(face, Face)
        assert face.id == "f_1"


# ── Webhooks ─────────────────────────────────────────────────


class TestWebhooks:
    def test_create_returns_webhook(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            json={"id": "wh_1", "url": "https://example.com/hook", "events": ["object.created"]},
        )
        wh = client.webhooks.create(url="https://example.com/hook", events=["object.created"])
        assert isinstance(wh, Webhook)
        assert wh.url == "https://example.com/hook"

    def test_list_returns_paginated(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            json={"items": [{"id": "wh_1", "url": "https://example.com", "events": []}], "next": None},
        )
        result = client.webhooks.list()
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 1


# ── API Keys ─────────────────────────────────────────────────


class TestApiKeys:
    def test_create_returns_api_key(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "key_1", "name": "My Key", "key": "sk_secret"})
        key = client.api_keys.create(name="My Key")
        assert isinstance(key, ApiKey)
        assert key.name == "My Key"

    def test_list_returns_list(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json=[{"id": "key_1", "name": "Key"}])
        result = client.api_keys.list()
        assert isinstance(result, list)
        assert isinstance(result[0], ApiKey)


# ── Indexer ──────────────────────────────────────────────────


class TestIndexer:
    def test_stats_returns_typed(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"total_templates": 100, "total_objects": 5000})
        stats = client.indexer.stats()
        assert isinstance(stats, PublicStats)
        assert stats.total_templates == 100
        assert stats.total_objects == 5000


# ── Error Handling ───────────────────────────────────────────


class TestErrorHandling:
    def test_401_raises_auth_error(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(status_code=401, json={"message": "Unauthorized", "code": "INVALID_TOKEN"})
        with pytest.raises(DualAuthError) as exc_info:
            client.wallets.me()
        assert exc_info.value.status == 401
        assert exc_info.value.code == "INVALID_TOKEN"

    def test_404_raises_not_found(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(status_code=404, json={"message": "Not found", "code": "NOT_FOUND"})
        with pytest.raises(DualNotFoundError):
            client.objects.get("bad_id")

    def test_429_raises_rate_limit(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(status_code=429, json={"message": "Too many requests"}, headers={"retry-after": "5"})
        with pytest.raises(DualRateLimitError) as exc_info:
            client.objects.list()
        assert exc_info.value.retry_after == 5.0

    def test_500_raises_dual_error(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(status_code=500, json={"message": "Internal error"})
        with pytest.raises(DualError):
            client.wallets.me()


# ── Retry Behavior ───────────────────────────────────────────


class TestRetryBehavior:
    def test_max_retries_zero_no_retry(self, httpx_mock: HTTPXMock) -> None:
        c = DualClient(api_key="test", base_url="https://test.local", max_retries=0)
        httpx_mock.add_response(status_code=503, json={"message": "Unavailable"})
        with pytest.raises(DualError):
            c.wallets.me()
        assert len(httpx_mock.get_requests()) == 1


# ── AuthMode Export ──────────────────────────────────────────


class TestAuthModeExport:
    def test_importable(self) -> None:
        assert AuthMode is not None

    def test_has_api_key(self) -> None:
        assert hasattr(AuthMode, "API_KEY")

    def test_has_bearer(self) -> None:
        assert hasattr(AuthMode, "BEARER")

    def test_has_both(self) -> None:
        assert hasattr(AuthMode, "BOTH")


# ── Async Client ─────────────────────────────────────────────


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_has_all_modules(self) -> None:
        async with AsyncDualClient(api_key="test-key", base_url="https://test.local") as client:
            assert hasattr(client, "wallets")
            assert hasattr(client, "templates")
            assert hasattr(client, "objects")

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        async with AsyncDualClient(api_key="test-key", base_url="https://test.local") as client:
            assert client is not None

    @pytest.mark.asyncio
    async def test_async_wallets_me(self, httpx_mock: HTTPXMock) -> None:
        async with AsyncDualClient(api_key="test-key", base_url="https://test.local", max_retries=0) as client:
            httpx_mock.add_response(json={"id": "w_async", "email": "async@test.com"})
            wallet = await client.wallets.me()
            assert isinstance(wallet, Wallet)
            assert wallet.id == "w_async"

    @pytest.mark.asyncio
    async def test_async_templates_list(self, httpx_mock: HTTPXMock) -> None:
        async with AsyncDualClient(api_key="test-key", base_url="https://test.local", max_retries=0) as client:
            httpx_mock.add_response(json={"items": [{"id": "t_1", "name": "T1"}], "next": None})
            result = await client.templates.list()
            assert isinstance(result, PaginatedResponse)
            assert len(result.items) == 1

    @pytest.mark.asyncio
    async def test_async_error_handling(self, httpx_mock: HTTPXMock) -> None:
        async with AsyncDualClient(api_key="test-key", base_url="https://test.local", max_retries=0) as client:
            httpx_mock.add_response(status_code=401, json={"message": "Unauthorized", "code": "INVALID_TOKEN"})
            with pytest.raises(DualAuthError) as exc_info:
                await client.wallets.me()
            assert exc_info.value.status == 401

    @pytest.mark.asyncio
    async def test_async_bearer_auth(self, httpx_mock: HTTPXMock) -> None:
        async with AsyncDualClient(
            api_key="jwt-token", auth_mode=AuthMode.BEARER,
            base_url="https://test.local", max_retries=0,
        ) as client:
            httpx_mock.add_response(json={"id": "w_1", "email": "test@test.com"})
            await client.wallets.me()
            req = httpx_mock.get_requests()[0]
            assert req.headers.get("authorization") == "Bearer jwt-token"


# ── Typed Model Integration ──────────────────────────────────


class TestTypedModels:
    def test_wallet_is_pydantic(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "w_1", "email": "test@test.com"})
        wallet = client.wallets.me()
        assert hasattr(wallet, "model_dump")
        d = wallet.model_dump()
        assert d["id"] == "w_1"

    def test_paginated_is_generic(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"items": [{"id": "t_1", "name": "T1"}], "next": None})
        result = client.templates.list()
        assert hasattr(result, "items")
        assert isinstance(result.items, list)
        assert all(isinstance(item, Template) for item in result.items)


# ── Storage ─────────────────────────────────────────────────


class TestStorage:
    def test_upload_returns_file_record(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            json={"id": "file_1", "url": "https://cdn.example.com/file_1.png", "content_type": "image/png", "size": 1024},
        )
        record = client.storage.upload(file=("test.png", b"fake-png-data", "image/png"))
        assert isinstance(record, FileRecord)
        assert record.id == "file_1"
        assert record.url == "https://cdn.example.com/file_1.png"
        assert record.content_type == "image/png"
        assert record.size == 1024

    def test_upload_sends_multipart(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "file_2", "url": "https://cdn.example.com/file_2.png"})
        client.storage.upload(file=("photo.png", b"\x89PNG", "image/png"))
        req = httpx_mock.get_requests()[0]
        assert req.method == "POST"
        assert "/storage/upload" in str(req.url)
        content_type = req.headers.get("content-type", "")
        assert "multipart/form-data" in content_type

    def test_upload_with_template_id(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "file_3", "url": "https://cdn.example.com/file_3.png"})
        client.storage.upload(file=("img.png", b"\x89PNG", "image/png"), template_id="tmpl_abc")
        req = httpx_mock.get_requests()[0]
        body = req.content.decode("utf-8", errors="replace")
        assert "tmpl_abc" in body

    def test_get_returns_file_record(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "file_1", "url": "https://cdn.example.com/file_1.png"})
        record = client.storage.get("file_1")
        assert isinstance(record, FileRecord)
        assert record.id == "file_1"

    def test_delete_returns_none(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(status_code=204)
        result = client.storage.delete("file_1")
        assert result is None

    def test_template_assets_returns_list(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json=[{"id": "file_1", "url": "https://cdn.example.com/a.png"}, {"id": "file_2", "url": "https://cdn.example.com/b.png"}])
        assets = client.storage.template_assets("tmpl_abc")
        assert isinstance(assets, list)
        assert len(assets) == 2
        assert all(isinstance(a, FileRecord) for a in assets)

    def test_upload_template_asset(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "file_4", "url": "https://cdn.example.com/asset.png"})
        record = client.storage.upload_template_asset("tmpl_abc", file=("asset.png", b"\x89PNG", "image/png"))
        assert isinstance(record, FileRecord)
        assert record.id == "file_4"
        req = httpx_mock.get_requests()[0]
        assert "/storage/template/tmpl_abc" in str(req.url)


# ── User-Agent Header ──────────────────────────────────────


class TestUserAgent:
    def test_user_agent_contains_version(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(json={"id": "w_1", "email": "a@b.com"})
        client.wallets.me()
        req = httpx_mock.get_requests()[0]
        assert req.headers.get("user-agent") == "dual-sdk-python/0.1.0"
