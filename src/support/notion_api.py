import time
from collections import deque
from dataclasses import dataclass

from notion_client import APIErrorCode, APIResponseError, Client

DEFAULT_MIN_SECONDS_BETWEEN_CALLS = 0.34
DEFAULT_MAX_RATE_LIMIT_RETRIES = 5
DEFAULT_INITIAL_BACKOFF_SECONDS = 1.0

PAGE_BOUNDARY_BLOCK_TYPES = {"child_page", "child_database"}


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

    def __init__(
        self,
        client,
        min_seconds_between_calls=DEFAULT_MIN_SECONDS_BETWEEN_CALLS,
        max_rate_limit_retries=DEFAULT_MAX_RATE_LIMIT_RETRIES,
        initial_backoff_seconds=DEFAULT_INITIAL_BACKOFF_SECONDS,
    ):
        self.client = client
        self.min_seconds_between_calls = min_seconds_between_calls
        self.max_rate_limit_retries = max_rate_limit_retries
        self.initial_backoff_seconds = initial_backoff_seconds
        self.last_call_finished_at = 0.0

    def _throttle(self):
        if self.min_seconds_between_calls <= 0:
            return
        seconds_since_last_call = time.monotonic() - self.last_call_finished_at
        remaining_wait = self.min_seconds_between_calls - seconds_since_last_call
        if remaining_wait > 0:
            time.sleep(remaining_wait)

    def _call_with_rate_limit_retry(self, make_request):
        """Retry a Notion API call with exponential backoff when rate-limited."""
        attempt = 0
        backoff_seconds = self.initial_backoff_seconds

        while True:
            self._throttle()
            try:
                response = make_request()
            except APIResponseError as error:
                is_rate_limited = error.code == APIErrorCode.RateLimited
                if not is_rate_limited or attempt >= self.max_rate_limit_retries:
                    raise
                time.sleep(backoff_seconds)
                backoff_seconds *= 2
                attempt += 1
                continue
            finally:
                self.last_call_finished_at = time.monotonic()
            return response

    def fetch_page(self, page_id):
        page = self._call_with_rate_limit_retry(
            lambda: self.client.pages.retrieve(page_id)
        )
        return page

    def fetch_all_blocks(self, block_id):
        blocks = []
        start_cursor = None

        while True:
            response = self._call_with_rate_limit_retry(
                lambda: self.client.blocks.children.list(
                    block_id=block_id, start_cursor=start_cursor, page_size=100
                )
            )

            blocks.extend(response["results"])
            if not response.get("has_more") or response.get("next_cursor") is None:
                break
            start_cursor = response["next_cursor"]

        for block in blocks:
            if block.get("type") in PAGE_BOUNDARY_BLOCK_TYPES:
                continue
            if block.get("has_children"):
                block["children"] = self.fetch_all_blocks(block["id"])

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

            for block in _find_child_page_blocks(child_blocks):
                child_page_id = block["id"]
                if child_page_id in visited_page_ids:
                    continue

                child_page = self.fetch_page(child_page_id)
                nodes.append(
                    PageNode(
                        page_id=child_page_id,
                        title=block["child_page"].get("title") or "Untitled",
                        parent_id=parent_page_id,
                        last_edited_time=child_page["last_edited_time"],
                    )
                )
                visited_page_ids.add(child_page_id)
                pending_page_ids.append(child_page_id)

        return nodes


def _find_child_page_blocks(blocks):
    """Recursively yield every child_page block found in a block tree."""
    for block in blocks:
        if block.get("type") == "child_page":
            yield block
        yield from _find_child_page_blocks(block.get("children", []))


def build_gateway(config):
    gateway = NotionGateway(Client(auth=config.notion_token))
    return gateway
