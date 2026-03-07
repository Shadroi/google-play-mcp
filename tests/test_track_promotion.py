from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from server import (
    _build_promoted_release,
    _build_release_notes,
    _parse_version_codes_json,
    _select_release_to_promote,
)


def test_select_release_uses_latest_when_version_codes_omitted():
    releases = [
        {"versionCodes": ["24"], "status": "completed"},
        {"versionCodes": ["23"], "status": "completed"},
    ]

    result = _select_release_to_promote(releases, None)

    assert result["versionCodes"] == ["24"]


def test_select_release_requires_requested_version_codes_to_match():
    releases = [
        {"versionCodes": ["24"], "status": "completed"},
        {"versionCodes": ["23"], "status": "completed"},
    ]

    result = _select_release_to_promote(releases, ["23"])

    assert result["versionCodes"] == ["23"]


def test_build_promoted_release_overrides_status_and_release_notes():
    source_release = {
        "versionCodes": ["24"],
        "status": "completed",
        "releaseNotes": [{"language": "en-US", "text": "Old note"}],
        "name": "keep-ignored-fields-out",
    }

    result = _build_promoted_release(
        source_release=source_release,
        status="inProgress",
        release_notes=[{"language": "ko-KR", "text": "버그 핫픽스"}],
    )

    assert result == {
        "versionCodes": ["24"],
        "status": "inProgress",
        "releaseNotes": [{"language": "ko-KR", "text": "버그 핫픽스"}],
    }


def test_build_promoted_release_preserves_existing_release_notes_when_not_overridden():
    source_release = {
        "versionCodes": ["24"],
        "status": "completed",
        "releaseNotes": [{"language": "en-US", "text": "Existing"}],
    }

    result = _build_promoted_release(
        source_release=source_release,
        status="completed",
        release_notes=[],
    )

    assert result == {
        "versionCodes": ["24"],
        "status": "completed",
        "releaseNotes": [{"language": "en-US", "text": "Existing"}],
    }


def test_parse_version_codes_json_returns_stringified_codes():
    assert _parse_version_codes_json('[24, "25"]') == ["24", "25"]


def test_build_release_notes_returns_language_entries():
    assert _build_release_notes(
        release_notes_ko="버그 핫픽스",
        release_notes_en="Bug hotfix",
    ) == [
        {"language": "ko-KR", "text": "버그 핫픽스"},
        {"language": "en-US", "text": "Bug hotfix"},
    ]
