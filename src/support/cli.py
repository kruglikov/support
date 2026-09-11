import argparse
import http.server
import posixpath
import socketserver
from urllib.parse import unquote

from support import config as project_config
from support.config import ConfigError, load_config
from support.notion_api import build_gateway

try:
    from notion_client.errors import APIResponseError
except Exception:  # pragma: no cover - defensive against client module layout changes

    class APIResponseError(Exception):
        """Fallback stand-in so the CLI still imports if notion_client changes shape."""

        code = None
        status = None


def is_servable_path(request_path):
    """True only for the viewer and graph files the page needs."""
    path = request_path.split("?", 1)[0].split("#", 1)[0]
    decoded_path = unquote(path)
    normalised_path = posixpath.normpath(decoded_path)

    if normalised_path in ("/", "/viewer", "/graph"):
        return True

    return normalised_path.startswith("/viewer/") or normalised_path.startswith("/graph/")


def root_redirect_target(request_path):
    """Return "/viewer/index.html" for a bare root request, else None."""
    path = request_path.split("?", 1)[0].split("#", 1)[0]
    decoded_path = unquote(path)
    normalised_path = posixpath.normpath(decoded_path)

    if normalised_path == "/":
        return "/viewer/index.html"
    return None


def _command_sync(args):
    configuration = load_config()
    gateway = build_gateway(configuration)
    from support.sync import run_sync

    report = run_sync(
        gateway,
        configuration.root_page_id,
        project_config.MIRROR_DIR,
        project_config.RAW_DIR,
        project_config.MANIFEST_PATH,
        force_full=args.full,
    )

    print(f"written: {len(report.written_page_ids)}")
    print(f"skipped: {len(report.skipped_page_ids)}")
    print(f"pruned:  {len(report.pruned_page_ids)}")
    for warning in report.warnings:
        print(f"warning: {warning}")
    return 0


def _command_status(args):
    configuration = load_config()
    gateway = build_gateway(configuration)
    from support.sync import run_status

    plan = run_status(gateway, configuration.root_page_id, project_config.MANIFEST_PATH)

    print(f"new:       {len(plan.new_page_ids)}")
    print(f"changed:   {len(plan.changed_page_ids)}")
    print(f"unchanged: {len(plan.unchanged_page_ids)}")
    print(f"removed:   {len(plan.removed_page_ids)}")
    return 0


def _command_build_graph(args):
    from support.graph import build_graph

    node_count, edge_count, warnings = build_graph(
        project_config.MIRROR_DIR,
        project_config.MANIFEST_PATH,
        project_config.GRAPH_PATH,
    )
    print(f"nodes: {node_count}")
    print(f"edges: {edge_count}")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


class RootedHandler(http.server.SimpleHTTPRequestHandler):
    """Serves only the viewer and graph files, redirecting "/" instead of listing it."""

    def __init__(self, *handler_args, directory=None, **handler_kwargs):
        directory = directory or str(project_config.PROJECT_ROOT)
        super().__init__(*handler_args, directory=directory, **handler_kwargs)

    def send_head(self):
        if not is_servable_path(self.path):
            self.send_error(404, "File not found")
            return None

        redirect_target = root_redirect_target(self.path)
        if redirect_target is not None:
            self.send_response(302)
            self.send_header("Location", redirect_target)
            self.end_headers()
            return None

        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, "File not found")
        return None


class ReusableTCPServer(socketserver.TCPServer):
    """A TCPServer that can be restarted without waiting out TIME_WAIT."""

    allow_reuse_address = True


def _serve_forever_quietly(server):
    """Run the server until Ctrl+C, exiting quietly instead of with a traceback."""
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def _command_serve(args):
    with ReusableTCPServer(("127.0.0.1", args.port), RootedHandler) as server:
        print(f"Viewer: http://127.0.0.1:{args.port}/viewer/index.html")
        _serve_forever_quietly(server)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="support")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="fetch changed Notion pages")
    sync_parser.add_argument("--full", action="store_true", help="refetch every page")
    sync_parser.set_defaults(handler=_command_sync)

    status_parser = subparsers.add_parser("status", help="report what sync would do")
    status_parser.set_defaults(handler=_command_status)

    graph_parser = subparsers.add_parser("build-graph", help="rebuild graph.json")
    graph_parser.set_defaults(handler=_command_build_graph)

    serve_parser = subparsers.add_parser("serve", help="serve the viewer locally")
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.set_defaults(handler=_command_serve)

    args = parser.parse_args(argv)

    try:
        return args.handler(args)
    except ConfigError as error:
        print(f"error: {error}")
        return 1
    except APIResponseError as error:
        is_auth_error = getattr(error, "status", None) == 401 or getattr(
            error, "code", None
        ) == "unauthorized"
        if is_auth_error:
            print(
                "error: Notion rejected the request as unauthorized. Check that "
                "NOTION_TOKEN is a valid integration token and that the root page "
                "has been shared with that integration."
            )
        else:
            print(f"error: Notion API request failed: {error}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
