"""Tests for `native.templates._meta_tags.generate_site_meta_tags`.

The helper builds the `og:url` / `twitter:url` canonical-URL meta tags for
every page on the site. It joins a trailing-slash-less `BURIDAN_URL` with a
caller-supplied `url`. Two callers exist:

  * static pages pass `url` *with* a leading slash (e.g. `"/dashboards"`).
  * the doc-page loop in `native/export.py` passes `url=f"{doc.url}"` where
    `doc.url` is a bare relative path like `"docs/resources/state"` (no
    leading slash), built in `native/engine/generator.py` as
    `url_path = "docs/" + ...`.

Previously the helper did `f"{BURIDAN_URL}{url}"` with no separator, which
silently corrupted the host for any caller that omitted the leading slash:
`"https://native.buridan.dev" + "docs/resources/state"` parsed (via
`urllib.parse.urlparse`) as `netloc="native.buridan.devdocs"` and
`path="/resources/state"` — an unresolvable host that dropped the
canonicalization hint for every doc page.

These tests pin the helper's slash-normalization contract so the fix stays
fixed and neither caller form regresses.
"""

from __future__ import annotations

from urllib.parse import urlparse

import pytest

from native.engine.generator import generate_docs_library
from native.templates._meta_tags import BURIDAN_URL, generate_site_meta_tags


def _tags_by_key(
    url: str,
    title: str = "T",
    description: str = "D",
    social_card: str = "card.webp",
) -> dict[str, str]:
    """Return the meta-tag list as a {key: content} dict.

    `key` is the `property` value when present, otherwise the `name` value,
    matching how a consumer resolves a meta tag.
    """
    return {
        (tag["property"] if "property" in tag else tag["name"]): tag["content"]
        for tag in generate_site_meta_tags(title, url, description, social_card)
    }


# (url input, expected absolute canonical URL)
URL_CASES = [
    # The doc-page caller passes a bare `docs/...` path (no leading slash) —
    # the regression being fixed.
    ("docs/resources/state", f"{BURIDAN_URL}/docs/resources/state"),
    # The same path with a leading slash must normalize identically, so the
    # helper is robust to both caller forms (static pages use leading slash).
    ("/docs/resources/state", f"{BURIDAN_URL}/docs/resources/state"),
    # Static-page callers (leading slash) must not regress.
    ("/dashboards", f"{BURIDAN_URL}/dashboards"),
    # A bare static-style value (no leading slash) must also normalize, so a
    # future caller that omits the leading slash cannot reintroduce the bug.
    ("dashboards", f"{BURIDAN_URL}/dashboards"),
    # Root page: a naive `f"{base}/{path}"` would yield a double slash here.
    ("/", f"{BURIDAN_URL}/"),
]


class TestUrlNormalization:
    @pytest.mark.parametrize(("url_input", "expected"), URL_CASES)  # pyright: ignore[reportUntypedFunctionDecorator]
    def test_og_url_and_twitter_url_are_well_formed(self, url_input, expected):
        tags = _tags_by_key(url_input)
        assert tags["og:url"] == expected
        assert tags["twitter:url"] == expected

    @pytest.mark.parametrize(("url_input", "_expected"), URL_CASES)  # pyright: ignore[reportUntypedFunctionDecorator]
    def test_host_is_not_corrupted(self, url_input, _expected):
        """The host must be exactly `native.buridan.dev`.

        Before the fix, a missing leading slash caused the first path segment
        to be swallowed into the netloc (e.g. `native.buridan.devdocs`),
        producing an unresolvable host. Guard against that exact regression.
        """
        tags = _tags_by_key(url_input)
        assert urlparse(tags["og:url"]).netloc == "native.buridan.dev"
        assert "devdocs" not in tags["og:url"]


# ---------------------------------------------------------------------------
# Integration: the real doc-page caller path (native/export.py:142)
# ---------------------------------------------------------------------------

_ALL_DOCS = generate_docs_library()


def _doc_id(doc) -> str:
    return doc.url


def test_docs_library_is_not_empty():
    """Sanity guard so the parametrized test below cannot silently collect
    zero cases (mirrors the pattern in tests/test_docs_error.py)."""
    assert _ALL_DOCS, "generate_docs_library() returned no docs"


class TestDocsLibraryMetaTags:
    """Exercises the exact call shape used by `native/export.py:142`:

        meta = generate_site_meta_tags(title=..., url=f"{doc.url}", ...)

    where `doc.url` has no leading slash. Every emitted doc page must produce
    a well-formed canonical URL on the `native.buridan.dev` host whose path
    matches the route the Reflex router serves (`/{doc.url}`).
    """

    @pytest.mark.parametrize("doc", _ALL_DOCS, ids=_doc_id)  # pyright: ignore[reportUntypedFunctionDecorator]
    def test_doc_canonical_url_is_well_formed(self, doc):
        tags = _tags_by_key(doc.url, title=doc.url, description=doc.description)
        expected = f"{BURIDAN_URL}/{doc.url}"
        assert tags["og:url"] == expected
        assert tags["twitter:url"] == expected
        parsed = urlparse(tags["og:url"])
        assert parsed.scheme == "https"
        assert parsed.netloc == "native.buridan.dev"
        assert parsed.path == f"/{doc.url}"
