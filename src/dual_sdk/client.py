"""DualClient — main entry point for the DUAL Python SDK."""

from __future__ import annotations

from typing import Any

from dual_sdk._transport import AsyncTransport, AuthMode, Transport
from dual_sdk.resources import (
    ApiKeys,
    AsyncApiKeys,
    AsyncEventBus,
    AsyncFaces,
    AsyncIndexer,
    AsyncNotifications,
    AsyncObjects,
    AsyncOrganizations,
    AsyncPayments,
    AsyncSequencer,
    AsyncStorage,
    AsyncSupport,
    AsyncTemplates,
    AsyncWallets,
    AsyncWebhooks,
    EventBus,
    Faces,
    Indexer,
    Notifications,
    Objects,
    Organizations,
    Payments,
    Sequencer,
    Storage,
    Support,
    Templates,
    Wallets,
    Webhooks,
)

_DEFAULT_BASE_URL = "https://gateway-48587430648.europe-west6.run.app"


class DualClient:
    """Synchronous client for the DUAL API.

    Usage::

        from dual_sdk import DualClient

        client = DualClient(api_key="your-api-key")

        # Get current wallet
        wallet = client.wallets.me()
        print(wallet.id, wallet.email)

        # List templates (returns PaginatedResponse[Template])
        page = client.templates.list(limit=20)
        for tmpl in page.items:
            print(tmpl.name)

    Args:
        api_key: Your DUAL API key or JWT token.
        auth_mode: How credentials are sent — ``API_KEY`` (default),
            ``BEARER``, or ``BOTH``. See :class:`AuthMode`.
        base_url: API base URL (default: ``https://gateway-48587430648.europe-west6.run.app``).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Maximum retry attempts for transient errors (default: 3).
        backoff: Base backoff delay in seconds between retries (default: 1.0).
        headers: Additional HTTP headers to include in every request.
    """

    def __init__(
        self,
        *,
        api_key: str,
        auth_mode: AuthMode = AuthMode.API_KEY,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff: float = 1.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._transport = Transport(
            api_key=api_key,
            auth_mode=auth_mode,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff=backoff,
            headers=headers,
        )

        self.wallets = Wallets(self._transport)
        self.templates = Templates(self._transport)
        self.objects = Objects(self._transport)
        self.organizations = Organizations(self._transport)
        self.payments = Payments(self._transport)
        self.storage = Storage(self._transport)
        self.webhooks = Webhooks(self._transport)
        self.notifications = Notifications(self._transport)
        self.event_bus = EventBus(self._transport)
        self.faces = Faces(self._transport)
        self.sequencer = Sequencer(self._transport)
        self.indexer = Indexer(self._transport)
        self.api_keys = ApiKeys(self._transport)
        self.support = Support(self._transport)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._transport.close()

    def __enter__(self) -> DualClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"DualClient(base_url={self._transport._base_url!r})"


class AsyncDualClient:
    """Asynchronous client for the DUAL API.

    Usage::

        import asyncio
        from dual_sdk import AsyncDualClient

        async def main():
            async with AsyncDualClient(api_key="your-api-key") as client:
                wallet = await client.wallets.me()
                templates = await client.templates.list(limit=20)

        asyncio.run(main())

    Args:
        api_key: Your DUAL API key or JWT token.
        auth_mode: How credentials are sent — ``API_KEY`` (default),
            ``BEARER``, or ``BOTH``. See :class:`AuthMode`.
        base_url: API base URL (default: ``https://gateway-48587430648.europe-west6.run.app``).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Maximum retry attempts for transient errors (default: 3).
        backoff: Base backoff delay in seconds between retries (default: 1.0).
        headers: Additional HTTP headers to include in every request.
    """

    def __init__(
        self,
        *,
        api_key: str,
        auth_mode: AuthMode = AuthMode.API_KEY,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff: float = 1.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._transport = AsyncTransport(
            api_key=api_key,
            auth_mode=auth_mode,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff=backoff,
            headers=headers,
        )

        self.wallets = AsyncWallets(self._transport)
        self.templates = AsyncTemplates(self._transport)
        self.objects = AsyncObjects(self._transport)
        self.organizations = AsyncOrganizations(self._transport)
        self.payments = AsyncPayments(self._transport)
        self.storage = AsyncStorage(self._transport)
        self.webhooks = AsyncWebhooks(self._transport)
        self.notifications = AsyncNotifications(self._transport)
        self.event_bus = AsyncEventBus(self._transport)
        self.faces = AsyncFaces(self._transport)
        self.sequencer = AsyncSequencer(self._transport)
        self.indexer = AsyncIndexer(self._transport)
        self.api_keys = AsyncApiKeys(self._transport)
        self.support = AsyncSupport(self._transport)

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._transport.close()

    async def __aenter__(self) -> AsyncDualClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"AsyncDualClient(base_url={self._transport._base_url!r})"
