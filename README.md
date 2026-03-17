# DUAL Python SDK

Official Python client for the [DUAL tokenization platform](https://dual-docs-gray.vercel.app).

Covers **100 API endpoints** across **14 resource modules** with both synchronous and asynchronous interfaces.

## Installation

```bash
pip install git+https://github.com/ro-ro-b/dual-sdk-python.git
```

## Quick Start

```python
import os
from dual_sdk import DualClient

client = DualClient(api_key=os.environ["DUAL_API_KEY"])

# Get current wallet
wallet = client.wallets.me()

# List templates
templates = client.templates.list(limit=20)

# Create an object from a template
obj = client.objects.create(
    template_id="tmpl_abc123",
    properties={"name": "My First Token"}
)
```

## Async Support

```python
import asyncio
from dual_sdk import AsyncDualClient

async def main():
    async with AsyncDualClient(api_key=os.environ["DUAL_API_KEY"]) as client:
        wallet = await client.wallets.me()
        templates = await client.templates.list(limit=20)

asyncio.run(main())
```

## Configuration

```python
client = DualClient(
    api_key=os.environ["DUAL_API_KEY"],
    base_url="https://blockv-labs.io",  # default
    timeout=10.0,       # seconds
    max_retries=3,      # retry on 429/5xx
    backoff=1.0,        # exponential backoff base
)
```

## Error Handling

```python
from dual_sdk import DualClient, DualError, DualAuthError, DualRateLimitError

try:
    wallet = client.wallets.me()
except DualAuthError as e:
    print(f"Auth failed [{e.status}]: {e.code}")
except DualRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except DualError as e:
    print(f"API error [{e.status}]: {e.message}")
```

## Modules

| Module | Methods | Description |
|--------|---------|-------------|
| `client.wallets` | 14 | Login, registration, profile, token refresh |
| `client.templates` | 7 | CRUD operations, search, variations |
| `client.objects` | 9 | Create, list, search, state management |
| `client.organizations` | 18 | Org management, members, roles, invitations |
| `client.payments` | 2 | Payment config, deposit listing |
| `client.storage` | 5 | File upload, metadata, template assets |
| `client.webhooks` | 6 | CRUD, test endpoint |
| `client.notifications` | 7 | Messages, templates |
| `client.event_bus` | 8 | Actions, action types, batch execution |
| `client.faces` | 6 | Face CRUD, by-template lookup |
| `client.sequencer` | 4 | Batch submission, checkpoints |
| `client.indexer` | 7 | Public API, stats, search |
| `client.api_keys` | 3 | Create, list, delete keys |
| `client.support` | 4 | Ticket management |

## Documentation

Full docs at [dual-docs-gray.vercel.app](https://dual-docs-gray.vercel.app/docs/developer-kit/python-sdk)

## License

MIT
