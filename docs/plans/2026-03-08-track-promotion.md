# Track Promotion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a dedicated MCP tool that promotes an already uploaded Google Play release from one track to another without re-uploading an AAB.

**Architecture:** Keep upload and promotion responsibilities separate by introducing a new `promote_track_release` tool in `server.py`. Extract a few pure helper functions for track validation, release-note building, release selection, and payload construction so the promotion path can be tested without hitting the live Android Publisher API.

**Tech Stack:** Python 3, FastMCP, Google Android Publisher API v3, pytest

---

### Task 1: Add failing tests for promotion helper behavior

**Files:**
- Create: `tests/test_track_promotion.py`
- Modify: `requirements.txt`

**Step 1: Write the failing test**

```python
from server import _select_release_to_promote


def test_select_release_uses_latest_when_no_version_codes():
    releases = [
        {"versionCodes": ["24"], "status": "completed"},
        {"versionCodes": ["23"], "status": "completed"},
    ]

    result = _select_release_to_promote(releases, None)

    assert result["versionCodes"] == ["24"]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_track_promotion.py -q`
Expected: FAIL because the helper does not exist yet.

**Step 3: Write minimal implementation**

Add pure helper functions in `server.py` for:
- `_validate_track_name(track: str) -> str`
- `_build_release_notes(...) -> list[dict]`
- `_parse_version_codes_json(...) -> list[str] | None`
- `_select_release_to_promote(...) -> dict`
- `_build_promoted_release(...) -> dict`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_track_promotion.py -q`
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/test_track_promotion.py requirements.txt server.py
git commit -m "test: cover track promotion helpers"
```

### Task 2: Implement the MCP promotion tool

**Files:**
- Modify: `server.py`
- Test: `tests/test_track_promotion.py`

**Step 1: Write the failing test**

```python
from server import _build_promoted_release


def test_build_promoted_release_overrides_release_notes_and_status():
    source = {
        "versionCodes": ["24"],
        "status": "completed",
        "releaseNotes": [{"language": "en-US", "text": "Old"}],
    }

    result = _build_promoted_release(
        source_release=source,
        status="inProgress",
        release_notes=[{"language": "ko-KR", "text": "버그 핫픽스"}],
    )

    assert result == {
        "versionCodes": ["24"],
        "status": "inProgress",
        "releaseNotes": [{"language": "ko-KR", "text": "버그 핫픽스"}],
    }
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_track_promotion.py -q`
Expected: FAIL.

**Step 3: Write minimal implementation**

Implement `promote_track_release()` in `server.py` to:
- create an edit
- fetch `source_track`
- select the source release
- build a target release body
- update `target_track`
- commit the edit
- delete the edit on failure

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_track_promotion.py -q`
Expected: PASS.

**Step 5: Commit**

```bash
git add server.py tests/test_track_promotion.py
git commit -m "feat: add Google Play track promotion tool"
```

### Task 3: Update documentation and verify basic behavior

**Files:**
- Modify: `README.md`
- Test: `tests/test_track_promotion.py`

**Step 1: Write the failing test**

No extra failing test required. This task is documentation and verification focused.

**Step 2: Update docs**

Document:
- the new `promote_track_release` feature in the README feature list
- a short example for internal to production promotion
- the fact that this reuses an existing uploaded version code and does not upload an AAB

**Step 3: Run verification**

Run: `pytest tests/test_track_promotion.py -q`
Expected: PASS.

Run: `python3 -m py_compile server.py`
Expected: no output.

**Step 4: Commit**

```bash
git add README.md docs/plans/2026-03-08-track-promotion-design.md docs/plans/2026-03-08-track-promotion.md
git commit -m "docs: document track promotion design and usage"
```
