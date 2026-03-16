"""Tests for the DUAL SDK client initialization and module access."""

from __future__ import annotations

import pytest
import httpx
from pytest_httpx import HTTPXMock

from dual_sdk import DualClient, AsyncDualClient, DualError, DualAuthError, DualNotFoundError, DualRateLimitError


@pytest.fixture
def client() -> DualClient:
    return DualClient(api_key="test-key", base_url="https://test.local", max_retries=0)


class TestClientInit:
    def test_has_all_modules(self, client: DualClient) -> None:
        assert hasattr(client, "wallets")
        assert hasattr(client, "templates")
        assert hasattr(client, "objects")
        assert hasattr(client, "organizations")
        assert hasattr(client, "payments")
        assert hasattr(client, "storage")
        assert hasattr(client, "webhooks")
        assert hasattr(client, "notifications")
        assert hasattr(client, "event_bus")
        assert hasattr(client, "faces")
        assert hasattr(client, "sequencer")
        assert hasattr(client, "indexer")
        assert hasattr(client, "api_keys")
        assert hasattr(client, "support")

    def test_repr(self, client: DualClient) -> None:
        assert "test.local" in repr(client)

    def test_context_manager(self) -> None:
        with DualClient(api_key="test-key", base_url="https://test.local") as client:
            assert client is not None


class TestWallets:
    def test_me(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/wallets/me",
            json={"id": "w_123", "email": "user@example.com"},
        )
        result = client.wallets.me()
        assert result["id"] == "w_123"

    def test_login(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/wallets/login",
            json={"access_token": "tok_abc", "refresh_token": "ref_xyz"},
        )
        result = client.wallets.login("user@example.com", "password123")
        assert result["access_token"] == "tok_abc"


class TestTemplates:
    def test_list(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url=httpx.URL("https://test.local/templates", params={"limit": "20", "next": ""}),
            json={"items": [{"id": "t_1"}], "next": None},
        )
        result = client.templates.list()
        assert len(result["items"]) == 1

    def test_create(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/templates",
            json={"id": "t_new", "name": "Test Template"},
        )
        result = client.templates.create(name="Test Template")
        assert result["name"] == "Test Template"


class TestObjects:
    def test_create(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/objects",
            json={"id": "o_1", "template_id": "t_1"},
        )
        result = client.objects.create(template_id="t_1", properties={"name": "Token"})
        assert result["template_id"] == "t_1"


class TestErrorHandling:
    def test_401_raises_auth_error(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/wallets/me",
            status_code=401,
            json={"message": "Unauthorized", "code": "INVALID_TOKEN"},
        )
        with pytest.raises(DualAuthError) as exc_info:
            client.wallets.me()
        assert exc_info.value.status == 401
        assert exc_info.value.code == "INVALID_TOKEN"

    def test_404_raises_not_found(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/objects/bad_id",
            status_code=404,
            json={"message": "Not found", "code": "NOT_FOUND"},
        )
        with pytest.raises(DualNotFoundError):
            client.objects.get("bad_id")

    def test_429_raises_rate_limit(self, httpx_mock: HTTPXMock, client: DualClient) -> None:
        httpx_mock.add_response(
            url="https://test.local/objects",
            status_code=429,
            json={"message": "Too many requests"},
            headers={"retry-after": "5"},
        )
        with pytest.raises(DualRateLimitError) as exc_info:
            client.objects.list()
        assert exc_info.value.retry_after == 5.0


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_has_all_modules(self) -> None:
        client = AsyncDualClient(api_key="test-key", base_url="https://test.local")
        assert hasattr(client, "wallets")
        assert hasattr(client, "templates")
        assert hasattr(client, "objects")
        await client.close()

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        async with AsyncDualClient(api_key="test-key", base_url="https://test.local") as client:
            assert client is not None
