import argparse
import http.server
import posixpath
import socketserver
from urllib.parse import unquote

from support import config as project_config
from support.config import ConfigError, load_config
from support.notion_api import build_gateway


def is_servable_path(request_path):
    """True only for the viewer and graph files the page needs."""
    path = request_path.split("?", 1)[0].split("#", 1)[0]
    decoded_path = unquote(path)
    normalised_path = posixpath.normpath(decoded_path)

    if normalised_path in ("/", "/viewer", "/graph"):
        return True

    return normalised_path.startswith("/viewer/") or normalised_path.startswith("/graph/")


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

    node_count, edge_count = build_graph(
        project_config.MIRROR_DIR,
        project_config.MANIFEST_PATH,
        project_config.GRAPH_PATH,
    )
    print(f"nodes: {node_count}")
    print(f"edges: {edge_count}")
    return 0


def _command_serve(args):
    handler = http.server.SimpleHTTPRequestHandler
    directory = str(project_config.PROJECT_ROOT)

    class RootedHandler(handler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=directory, **handler_kwargs)

        def send_head(self):
            if not is_servable_path(self.path):
                self.send_error(404, "File not found")
                return None
            return super().send_head()

    with socketserver.TCPServer(("127.0.0.1", args.port), RootedHandler) as server:
        print(f"Viewer: http://127.0.0.1:{args.port}/viewer/index.html")
        server.serve_forever()
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
