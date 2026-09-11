import time
from collections import deque
from dataclasses import dataclass

from notion_client import Client

DEFAULT_MIN_SECONDS_BETWEEN_CALLS = 0.34


@dataclass(frozen=True)
class PageNode:
    page_id: str
    title: str
    parent_id: str | None
    last_edited_time: str


def extract_title(page):
    properties = page.get("properties", {})
    title_property = properties.get("title", {})
    title_fragments = title_property.get("title", [])
    joined_title = "".join(fragment.get("plain_text", "") for fragment in title_fragments)
    return joined_title or "Untitled"


class NotionGateway:
    """Read-only access to Notion, throttled to stay under the rate limit."""

    def __init__(self, client, min_seconds_between_calls=DEFAULT_MIN_SECONDS_BETWEEN_CALLS):
        self.client = client
        self.min_seconds_between_calls = min_seconds_between_calls
        self.last_call_finished_at = 0.0

    def _throttle(self):
        if self.min_seconds_between_calls <= 0:
            return
        seconds_since_last_call = time.monotonic() - self.last_call_finished_at
        remaining_wait = self.min_seconds_between_calls - seconds_since_last_call
        if remaining_wait > 0:
            time.sleep(remaining_wait)

    def fetch_page(self, page_id):
        self._throttle()
        page = self.client.pages.retrieve(page_id)
        self.last_call_finished_at = time.monotonic()
        return page

    def fetch_all_blocks(self, block_id):
        blocks = []
        start_cursor = None

        while True:
            self._throttle()
            response = self.client.blocks.children.list(
                block_id=block_id, start_cursor=start_cursor, page_size=100
            )
            self.last_call_finished_at = time.monotonic()

            blocks.extend(response["results"])
            if not response.get("has_more"):
                break
            start_cursor = response["next_cursor"]

        return blocks

    def walk_page_tree(self, root_page_id):
        root_page = self.fetch_page(root_page_id)
        root_node = PageNode(
            page_id=root_page_id,
            title=extract_title(root_page),
            parent_id=None,
            last_edited_time=root_page["last_edited_time"],
        )

        nodes = [root_node]
        visited_page_ids = {root_page_id}
        pending_page_ids = deque([root_page_id])

        while pending_page_ids:
            parent_page_id = pending_page_ids.popleft()
            child_blocks = self.fetch_all_blocks(parent_page_id)

            for block in child_blocks:
                if block.get("type") != "child_page":
                    continue
                child_page_id = block["id"]
                if child_page_id in visited_page_ids:
                    continue

                child_page = self.fetch_page(child_page_id)
                nodes.append(
                    PageNode(
                        page_id=child_page_id,
                        title=block["child_page"]["title"],
                        parent_id=parent_page_id,
                        last_edited_time=child_page["last_edited_time"],
                    )
                )
                visited_page_ids.add(child_page_id)
                pending_page_ids.append(child_page_id)

        return nodes


def build_gateway(config):
    gateway = NotionGateway(Client(auth=config.notion_token))
    return gateway
