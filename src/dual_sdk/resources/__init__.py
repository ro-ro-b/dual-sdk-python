"""Resource modules for the DUAL SDK."""

from dual_sdk.resources.api_keys import ApiKeys, AsyncApiKeys
from dual_sdk.resources.event_bus import AsyncEventBus, EventBus
from dual_sdk.resources.faces import AsyncFaces, Faces
from dual_sdk.resources.indexer import AsyncIndexer, Indexer
from dual_sdk.resources.notifications import AsyncNotifications, Notifications
from dual_sdk.resources.objects import AsyncObjects, Objects
from dual_sdk.resources.organizations import AsyncOrganizations, Organizations
from dual_sdk.resources.payments import AsyncPayments, Payments
from dual_sdk.resources.sequencer import AsyncSequencer, Sequencer
from dual_sdk.resources.storage import AsyncStorage, Storage
from dual_sdk.resources.support import AsyncSupport, Support
from dual_sdk.resources.templates import AsyncTemplates, Templates
from dual_sdk.resources.wallets import AsyncWallets, Wallets
from dual_sdk.resources.webhooks import AsyncWebhooks, Webhooks

__all__ = [
    "ApiKeys",
    "AsyncApiKeys",
    "EventBus",
    "AsyncEventBus",
    "Faces",
    "AsyncFaces",
    "Indexer",
    "AsyncIndexer",
    "Notifications",
    "AsyncNotifications",
    "Objects",
    "AsyncObjects",
    "Organizations",
    "AsyncOrganizations",
    "Payments",
    "AsyncPayments",
    "Sequencer",
    "AsyncSequencer",
    "Storage",
    "AsyncStorage",
    "Support",
    "AsyncSupport",
    "Templates",
    "AsyncTemplates",
    "Wallets",
    "AsyncWallets",
    "Webhooks",
    "AsyncWebhooks",
]
