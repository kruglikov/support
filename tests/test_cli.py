import pytest

from support.cli import is_servable_path


@pytest.mark.parametrize(
    "request_path, expected",
    [
        ("/viewer/index.html", True),
        ("/viewer/app.js", True),
        ("/viewer/style.css", True),
        ("/graph/graph.json", True),
        ("/", True),
        ("/viewer", True),
        ("/graph", True),
        ("/viewer/", True),
        ("/viewer/index.html?x=../../.env", True),
        ("/.env", False),
        ("/.git/config", False),
        ("/mirror/manifest.json", False),
        ("/viewer/../.env", False),
        ("/viewer/../../etc/passwd", False),
        ("//.env", False),
        ("/viewerX/secret", False),
        ("/graph/../mirror/manifest.json", False),
        ("/viewer/%2e%2e/.env", False),
        ("/viewer/%2E%2E/.env", False),
        ("/viewer/%2e%2e%2f.env", False),
        ("/graph/%2e%2e/mirror/manifest.json", False),
        ("/viewer/%69ndex.html", True),
    ],
)
def test_is_servable_path(request_path, expected):
    assert is_servable_path(request_path) == expected
