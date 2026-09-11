import pytest

from support.cli import is_servable_path


@pytest.mark.parametrize(
    "request_path, expected",
    [
        ("/viewer/index.html", True),
        ("/graph/graph.json", True),
        ("/", True),
        ("/.env", False),
        ("/.git/config", False),
        ("/mirror/manifest.json", False),
        ("/viewer/../.env", False),
        ("/viewer/../../etc/passwd", False),
    ],
)
def test_is_servable_path(request_path, expected):
    assert is_servable_path(request_path) == expected
