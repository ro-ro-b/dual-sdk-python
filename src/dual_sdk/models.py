"""Shared data models for the DUAL SDK.

All models use ``extra="allow"`` so that unknown fields returned by the API
are preserved as extra attributes rather than raising validation errors.
"""

from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class _BaseModel(BaseModel):
    """SDK base model — tolerates extra fields from the API."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# ── Pagination ──────────────────────────────────────────────


class PaginatedResponse(_BaseModel, Generic[T]):
    """Cursor-based paginated response wrapper.

    The API returns ``"next"`` in JSON; the SDK exposes it as ``.cursor``.
    Both names are accepted when constructing the model (``populate_by_name=True``).

    Attributes:
        items: List of result objects.
        cursor: Opaque cursor for the next page, or ``None`` if this is the last page.
               Aliased from the ``"next"`` key in the API JSON response.
    """

    items: List[T] = Field(default_factory=list)
    cursor: Optional[str] = Field(default=None, alias="next")

    @property
    def next(self) -> Optional[str]:
        """Alias for ``cursor`` — matches the raw API field name."""
        return self.cursor


# ── Auth ────────────────────────────────────────────────────


class TokenPair(_BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"


class Wallet(_BaseModel):
    id: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class StatusResult(_BaseModel):
    """Generic status response for fire-and-forget operations."""

    success: bool = True
    message: Optional[str] = None


# ── Templates ───────────────────────────────────────────────


class Template(_BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    organization_id: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class Variation(_BaseModel):
    id: str
    template_id: str
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)


# ── Objects ─────────────────────────────────────────────────


class ObjectCount(_BaseModel):
    count: int = 0


class Object(_BaseModel):
    id: str
    template_id: str
    owner_id: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ── Organizations ───────────────────────────────────────────


class Organization(_BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class Member(_BaseModel):
    id: str
    wallet_id: str
    role: Optional[str] = None
    organization_id: Optional[str] = None


class Role(_BaseModel):
    id: str
    name: str
    permissions: List[str] = Field(default_factory=list)


class Invitation(_BaseModel):
    id: str
    email: Optional[str] = None
    organization_id: Optional[str] = None
    status: str = "pending"


class Balance(_BaseModel):
    currency: Optional[str] = None
    amount: Optional[str] = None
    available: Optional[str] = None


class BalanceTransaction(_BaseModel):
    id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    type: Optional[str] = None
    created_at: Optional[str] = None


class AcceptInvitationResult(_BaseModel):
    organization_id: Optional[str] = None
    member_id: Optional[str] = None
    status: Optional[str] = None


# ── Payments ────────────────────────────────────────────────


class PaymentConfig(_BaseModel):
    multi_token_deposit_address: Optional[str] = None
    vee_address: Optional[str] = None
    supported_tokens: List[Dict[str, Any]] = Field(default_factory=list)


class Deposit(_BaseModel):
    id: Optional[str] = None
    tx_hash: Optional[str] = None
    token: Optional[str] = None
    amount: Optional[str] = None


# ── Webhooks ────────────────────────────────────────────────


class Webhook(_BaseModel):
    id: str
    url: str
    events: List[str] = Field(default_factory=list)
    secret: Optional[str] = None
    active: bool = True


class WebhookTestResult(_BaseModel):
    success: bool = False
    status_code: Optional[int] = None
    response_body: Optional[str] = None


# ── Event Bus ───────────────────────────────────────────────


class Action(_BaseModel):
    id: Optional[str] = None
    action_type: Optional[str] = None
    status: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


class ActionType(_BaseModel):
    id: str
    name: str
    description: Optional[str] = None


# ── Faces ───────────────────────────────────────────────────


class Face(_BaseModel):
    id: str
    template_id: Optional[str] = None
    display_type: Optional[str] = None
    resources: List[str] = Field(default_factory=list)


# ── Storage ─────────────────────────────────────────────────


class FileRecord(_BaseModel):
    id: str
    url: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None


# ── Sequencer ───────────────────────────────────────────────


class Batch(_BaseModel):
    id: str
    status: Optional[str] = None
    action_count: Optional[int] = None
    created_at: Optional[str] = None


class Checkpoint(_BaseModel):
    id: str
    batch_id: Optional[str] = None
    merkle_root: Optional[str] = None
    created_at: Optional[str] = None


# ── Notifications ───────────────────────────────────────────


class Message(_BaseModel):
    id: str
    content: Optional[str] = None
    sent_at: Optional[str] = None


class MessageTemplate(_BaseModel):
    id: str
    name: str
    body: Optional[str] = None


# ── API Keys ────────────────────────────────────────────────


class ApiKey(_BaseModel):
    id: str
    name: Optional[str] = None
    key: Optional[str] = None
    created_at: Optional[str] = None


# ── Support ─────────────────────────────────────────────────


class SupportMessage(_BaseModel):
    id: str
    content: Optional[str] = None
    created_at: Optional[str] = None


# ── Public / Indexer ────────────────────────────────────────


class PublicStats(_BaseModel):
    total_templates: Optional[int] = None
    total_objects: Optional[int] = None
    total_organizations: Optional[int] = None
