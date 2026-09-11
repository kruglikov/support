import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIRROR_DIR = PROJECT_ROOT / "mirror"
RAW_DIR = MIRROR_DIR / ".raw"
MANIFEST_PATH = MIRROR_DIR / "manifest.json"
GRAPH_PATH = PROJECT_ROOT / "graph" / "graph.json"
VIEWER_DIR = PROJECT_ROOT / "viewer"


class ConfigError(Exception):
    """Raised when required environment configuration is absent."""


@dataclass(frozen=True)
class Config:
    notion_token: str
    root_page_id: str


def load_config():
    notion_token = os.environ.get("NOTION_TOKEN")
    if not notion_token:
        raise ConfigError(
            "NOTION_TOKEN is not set. Create a Notion internal integration, "
            "share the root page with it, and export its token."
        )

    root_page_id = os.environ.get("NOTION_ROOT_PAGE_ID")
    if not root_page_id:
        raise ConfigError(
            "NOTION_ROOT_PAGE_ID is not set. Use the ID of the Software Development page."
        )

    config = Config(notion_token=notion_token, root_page_id=root_page_id)
    return config
