# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2026-03-14

### Fixed

- **Subscription creation API error**: Fixed `create_subscription_product` failing with `TYPE_BOOL` validation error. The `newSubscriberAvailability` field in subscription `regionalConfigs` was incorrectly set to the string `"AVAILABLE"` instead of a boolean `true`, causing all subscription creation calls to fail with a 400 error.
- **Python version compatibility**: The CLI now automatically detects and uses the best available Python version (3.13 → 3.10) when creating the virtual environment. Previously it defaulted to the macOS system Python (3.9.6), which is too old for `mcp[cli]>=1.0.0` (requires Python 3.10+).
- **Pip upgrade on setup**: The CLI now upgrades pip before installing dependencies, preventing stale pip from failing to resolve packages.

## [1.0.1] - Initial release

### Added

- MCP server for Google Play Developer API
- App deployment tools (internal, track, promote)
- In-app product management (create, batch create, activate, deactivate, list)
- Subscription product management (create, list)
- Store listing management (get, update, upload images)
- Automatic regional price conversion for 170+ currencies
- Interactive setup wizard (`init-key`)
- Korean and English language support
