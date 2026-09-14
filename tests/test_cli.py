import httpx
import pytest
from notion_client import APIErrorCode, APIResponseError

from support import cli
from support.cli import (
    ReusableTCPServer,
    RootedHandler,
    _serve_forever_quietly,
    is_servable_path,
    main,
    root_redirect_target,
)


def make_api_response_error(code, status):
    return APIResponseError(
        code=code,
        status=status,
        message="boom",
        headers=httpx.Headers(),
        raw_body_text="",
    )


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


def test_root_redirect_target_redirects_the_bare_root():
    assert root_redirect_target("/") == "/viewer/index.html"
    assert root_redirect_target("/?x=1") == "/viewer/index.html"


def test_root_redirect_target_leaves_other_paths_alone():
    assert root_redirect_target("/viewer/index.html") is None
    assert root_redirect_target("/graph/graph.json") is None
    assert root_redirect_target("/viewer") is None


def test_root_request_is_redirected_instead_of_listed():
    handler = object.__new__(RootedHandler)
    handler.path = "/"
    calls = []
    handler.send_response = lambda code: calls.append(("send_response", code))
    handler.send_header = lambda key, value: calls.append(("send_header", key, value))
    handler.end_headers = lambda: calls.append(("end_headers",))

    def fail_if_called(path):
        raise AssertionError("must not serve a directory listing for /")

    handler.list_directory = fail_if_called

    result = handler.send_head()

    assert result is None
    assert ("send_response", 302) in calls
    assert ("send_header", "Location", "/viewer/index.html") in calls
    assert ("end_headers",) in calls


def test_list_directory_is_disabled_as_defense_in_depth():
    handler = object.__new__(RootedHandler)
    errors = []
    handler.send_error = lambda code, message=None: errors.append(code)

    result = handler.list_directory("/some/path")

    assert result is None
    assert errors == [404]


def test_reusable_tcp_server_allows_address_reuse():
    assert ReusableTCPServer.allow_reuse_address is True


def test_serve_forever_quietly_swallows_keyboard_interrupt():
    class FakeServerThatIsInterrupted:
        def serve_forever(self):
            raise KeyboardInterrupt

    _serve_forever_quietly(FakeServerThatIsInterrupted())  # must not raise


def test_main_reports_an_unauthorized_notion_token_clearly_and_exits_1(monkeypatch, capsys):
    monkeypatch.setenv("NOTION_TOKEN", "bad-token")
    monkeypatch.setenv("NOTION_ROOT_PAGE_ID", "root")

    class FakeGatewayThatRejectsTheToken:
        def walk_page_tree(self, root_page_id):
            raise make_api_response_error(APIErrorCode.Unauthorized, 401)

    monkeypatch.setattr(cli, "build_gateway", lambda config: FakeGatewayThatRejectsTheToken())

    exit_status = main(["status"])

    captured = capsys.readouterr()
    assert exit_status == 1
    assert "unauthorized" in captured.out.lower() or "invalid" in captured.out.lower()
    assert "token" in captured.out.lower()


def test_main_reports_other_notion_api_errors_and_exits_1(monkeypatch, capsys):
    monkeypatch.setenv("NOTION_TOKEN", "a-token")
    monkeypatch.setenv("NOTION_ROOT_PAGE_ID", "root")

    class FakeGatewayThatFails:
        def walk_page_tree(self, root_page_id):
            raise make_api_response_error(APIErrorCode.InternalServerError, 500)

    monkeypatch.setattr(cli, "build_gateway", lambda config: FakeGatewayThatFails())

    exit_status = main(["status"])

    captured = capsys.readouterr()
    assert exit_status == 1
    assert "error" in captured.out.lower()
