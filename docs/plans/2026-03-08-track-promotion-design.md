# Track Promotion Design

**Problem**

`google-play-mcp` currently supports uploading a new AAB to a target track, but it cannot promote an already uploaded release from one Google Play track to another. This causes failures when users want to move an internal release to production without creating a new artifact.

**Decision**

Add a new MCP tool named `promote_track_release`.

This tool will:
- read releases from a source track such as `internal`
- select either the requested version codes or the latest release on that track
- write a matching release into a target track such as `production`
- optionally override release notes while reusing the existing uploaded artifact

**Why A New Tool**

`deploy_track` and `deploy_production` are upload-oriented APIs. Extending them with promotion-only branches would blur their contract and make failure cases harder to understand. A separate promotion tool keeps upload and promotion responsibilities distinct.

**API Shape**

`promote_track_release(source_track, target_track, version_codes_json="", release_notes_ko="", release_notes_en="", status="completed")`

Notes:
- `source_track` and `target_track` accept `internal`, `alpha`, `beta`, `production`
- `version_codes_json` is optional JSON array such as `[24]` or `["24"]`
- when `version_codes_json` is omitted, the tool promotes the latest release from the source track
- release notes are optional overrides; if omitted, the source release notes are preserved
- `status` defaults to `completed` and is applied to the target release body

**Implementation Approach**

1. Add small helper functions in `server.py` for:
   - validating track names
   - building release-notes arrays from Korean and English text
   - fetching source track releases
   - selecting the release to promote
   - constructing the target release payload
2. Add the new `@mcp.tool()` function.
3. Reuse the normal edit lifecycle:
   - create edit
   - read source track
   - update target track
   - commit edit
4. Return a clear success message with source track, target track, promoted version codes, status, and edit ID.

**Error Handling**

The tool should fail clearly when:
- the source or target track name is invalid
- source and target tracks are the same
- the source track has no releases
- requested version codes are not present on the source track
- `version_codes_json` is invalid JSON or not a list

**Testing Strategy**

There is no existing automated test suite in the repository, so start with unit tests around the pure helper functions. The highest-value coverage is:
- release notes override behavior
- latest release selection when version codes are omitted
- exact release matching when version codes are provided
- rejection of invalid track names or missing version codes

**Documentation**

Update `README.md` feature lists and tool examples to document the new promotion flow.
