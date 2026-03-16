"""Shared data models for the DUAL SDK."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# ── Pagination ──────────────────────────────────────────────


class PaginatedResponse(BaseModel, Generic[T]):
    """Cursor-based paginated response wrapper.

    Attributes:
        items: List of result objects.
        next: Opaque cursor for the next page, or ``None`` if this is the last page.
    """

    items: list[T] = Field(default_factory=list)
    next: str | None = None


# ── Auth ────────────────────────────────────────────────────


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class Wallet(BaseModel):
    id: str
    email: str | None = None
    name: str | None = None
    avatar: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


# ── Templates ───────────────────────────────────────────────


class Template(BaseModel):
    id: str
    name: str
    description: str | None = None
    organization_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None


class Variation(BaseModel):
    id: str
    template_id: str
    name: str
    properties: dict[str, Any] = Field(default_factory=dict)


# ── Objects ─────────────────────────────────────────────────


class Object(BaseModel):
    id: str
    template_id: str
    owner_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None


# ── Organizations ───────────────────────────────────────────


class Organization(BaseModel):
    id: str
    name: str
    description: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class Member(BaseModel):
    id: str
    wallet_id: str
    role: str | None = None
    organization_id: str | None = None


class Role(BaseModel):
    id: str
    name: str
    permissions: list[str] = Field(default_factory=list)


class Invitation(BaseModel):
    id: str
    email: str | None = None
    organization_id: str | None = None
    status: str = "pending"


# ── Payments ────────────────────────────────────────────────


class PaymentConfig(BaseModel):
    multi_token_deposit_address: str | None = None
    vee_address: str | None = None
    supported_tokens: list[dict[str, Any]] = Field(default_factory=list)


class Deposit(BaseModel):
    id: str | None = None
    tx_hash: str | None = None
    token: str | None = None
    amount: str | None = None


# ── Webhooks ────────────────────────────────────────────────


class Webhook(BaseModel):
    id: str
    url: str
    events: list[str] = Field(default_factory=list)
    secret: str | None = None
    active: bool = True


# ── Event Bus ───────────────────────────────────────────────


class Action(BaseModel):
    id: str | None = None
    action_type: str | None = None
    status: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class ActionType(BaseModel):
    id: str
    name: str
    description: str | None = None


# ── Faces ───────────────────────────────────────────────────


class Face(BaseModel):
    id: str
    template_id: str | None = None
    display_type: str | None = None
    resources: list[str] = Field(default_factory=list)


# ── Storage ─────────────────────────────────────────────────


class FileRecord(BaseModel):
    id: str
    url: str | None = None
    content_type: str | None = None
    size: int | None = None


# ── Sequencer ───────────────────────────────────────────────


class Batch(BaseModel):
    id: str
    status: str | None = None
    action_count: int | None = None
    created_at: str | None = None


class Checkpoint(BaseModel):
    id: str
    batch_id: str | None = None
    merkle_root: str | None = None
    created_at: str | None = None


# ── Notifications ───────────────────────────────────────────


class Message(BaseModel):
    id: str
    content: str | None = None
    sent_at: str | None = None


class MessageTemplate(BaseModel):
    id: str
    name: str
    body: str | None = None


# ── API Keys ────────────────────────────────────────────────


class ApiKey(BaseModel):
    id: str
    name: str | None = None
    key: str | None = None
    created_at: str | None = None


# ── Support ─────────────────────────────────────────────────


class SupportMessage(BaseModel):
    id: str
    content: str | None = None
    created_at: str | None = None


# ── Public / Indexer ────────────────────────────────────────


class PublicStats(BaseModel):
    total_templates: int | None = None
    total_objects: int | None = None
    total_organizations: int | None = None
