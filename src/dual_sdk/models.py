"""Shared data models for the DUAL SDK.

All models use ``extra="allow"`` so that unknown fields returned by the API
are preserved as extra attributes rather than raising validation errors.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

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

    items: list[T] = Field(default_factory=list)
    cursor: str | None = Field(default=None, alias="next")

    @property
    def next(self) -> str | None:
        """Alias for ``cursor`` — matches the raw API field name."""
        return self.cursor


# ── Auth ────────────────────────────────────────────────────


class TokenPair(_BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class Wallet(_BaseModel):
    id: str
    email: str | None = None
    name: str | None = None
    avatar: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


# ── Templates ───────────────────────────────────────────────


class Template(_BaseModel):
    id: str
    name: str
    description: str | None = None
    organization_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None


class Variation(_BaseModel):
    id: str
    template_id: str
    name: str
    properties: dict[str, Any] = Field(default_factory=dict)


# ── Objects ─────────────────────────────────────────────────


class Object(_BaseModel):
    id: str
    template_id: str
    owner_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None


# ── Organizations ───────────────────────────────────────────


class Organization(_BaseModel):
    id: str
    name: str
    description: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class Member(_BaseModel):
    id: str
    wallet_id: str
    role: str | None = None
    organization_id: str | None = None


class Role(_BaseModel):
    id: str
    name: str
    permissions: list[str] = Field(default_factory=list)


class Invitation(_BaseModel):
    id: str
    email: str | None = None
    organization_id: str | None = None
    status: str = "pending"


# ── Payments ────────────────────────────────────────────────


class PaymentConfig(_BaseModel):
    multi_token_deposit_address: str | None = None
    vee_address: str | None = None
    supported_tokens: list[dict[str, Any]] = Field(default_factory=list)


class Deposit(_BaseModel):
    id: str | None = None
    tx_hash: str | None = None
    token: str | None = None
    amount: str | None = None


# ── Webhooks ────────────────────────────────────────────────


class Webhook(_BaseModel):
    id: str
    url: str
    events: list[str] = Field(default_factory=list)
    secret: str | None = None
    active: bool = True


# ── Event Bus ───────────────────────────────────────────────


class Action(_BaseModel):
    id: str | None = None
    action_type: str | None = None
    status: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class ActionType(_BaseModel):
    id: str
    name: str
    description: str | None = None


# ── Faces ───────────────────────────────────────────────────


class Face(_BaseModel):
    id: str
    template_id: str | None = None
    display_type: str | None = None
    resources: list[str] = Field(default_factory=list)


# ── Storage ─────────────────────────────────────────────────


class FileRecord(_BaseModel):
    id: str
    url: str | None = None
    content_type: str | None = None
    size: int | None = None


# ── Sequencer ───────────────────────────────────────────────


class Batch(_BaseModel):
    id: str
    status: str | None = None
    action_count: int | None = None
    created_at: str | None = None


class Checkpoint(_BaseModel):
    id: str
    batch_id: str | None = None
    merkle_root: str | None = None
    created_at: str | None = None


# ── Notifications ───────────────────────────────────────────


class Message(_BaseModel):
    id: str
    content: str | None = None
    sent_at: str | None = None


class MessageTemplate(_BaseModel):
    id: str
    name: str
    body: str | None = None


# ── API Keys ────────────────────────────────────────────────


class ApiKey(_BaseModel):
    id: str
    name: str | None = None
    key: str | None = None
    created_at: str | None = None


# ── Support ─────────────────────────────────────────────────


class SupportMessage(_BaseModel):
    id: str
    content: str | None = None
    created_at: str | None = None


# ── Public / Indexer ────────────────────────────────────────


class PublicStats(_BaseModel):
    total_templates: int | None = None
    total_objects: int | None = None
    total_organizations: int | None = None
