# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-03-17

### Added
- Initial release of the DUAL Python SDK.
- Sync (`DualClient`) and async (`AsyncDualClient`) client interfaces.
- 14 resource modules covering 100 API endpoints.
- Typed Pydantic v2 response models with `extra="allow"` for forward compatibility.
- `PaginatedResponse[T]` generic for cursor-based pagination.
- `AuthMode` enum for explicit auth strategy (`API_KEY`, `BEARER`, `BOTH`).
- Automatic retry with exponential backoff on 429/5xx responses.
- Typed error hierarchy: `DualError`, `DualAuthError`, `DualNotFoundError`, `DualRateLimitError`.
- Multipart file upload support for storage endpoints.
- Full test suite using pytest + pytest-httpx.

### Security
- API keys are never logged or included in error messages.
- TLS certificate verification enabled by default via httpx.
