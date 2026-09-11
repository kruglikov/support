const state = {
  nodesById: new Map(),
  childrenBySource: new Map(),
  relatedBySource: new Map(),
  selectedId: null,
};

async function load() {
  const treeElement = document.getElementById("tree");
  let document_;

  try {
    const response = await fetch("../graph/graph.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    document_ = await response.json();
  } catch (error) {
    treeElement.innerHTML =
      '<p class="error">graph.json could not be loaded. Run <code>support build-graph</code> first.</p>';
    return;
  }

  for (const node of document_.nodes) {
    state.nodesById.set(node.id, node);
  }

  for (const edge of document_.edges) {
    const bucket = edge.kind === "contains" ? state.childrenBySource : state.relatedBySource;
    if (!bucket.has(edge.source)) {
      bucket.set(edge.source, []);
    }
    bucket.get(edge.source).push(edge.target);
  }

  const childIds = new Set();
  for (const edge of document_.edges) {
    if (edge.kind === "contains") {
      childIds.add(edge.target);
    }
  }
  const rootIds = document_.nodes
    .filter((node) => !childIds.has(node.id))
    .map((node) => node.id);

  treeElement.replaceChildren(renderBranch(rootIds, true, new Set()));
}

function renderBranch(nodeIds, isExpanded, visitedIds) {
  const container = document.createElement("div");
  container.className = "children";
  container.hidden = !isExpanded;

  for (const nodeId of nodeIds) {
    if (visitedIds.has(nodeId)) {
      continue;
    }

    const node = state.nodesById.get(nodeId);
    if (!node) {
      continue;
    }

    const childIds = state.childrenBySource.get(nodeId) || [];
    const row = document.createElement("button");
    row.className = "row" + (node.is_priority ? " priority" : "");
    row.dataset.nodeId = nodeId;
    row.innerHTML =
      `<span class="caret">${childIds.length ? "\u203a" : ""}</span>` +
      escapeHtml(node.title);

    const childContainer = childIds.length
      ? renderBranch(childIds, false, new Set(visitedIds).add(nodeId))
      : null;

    row.addEventListener("click", () => {
      if (childContainer) {
        childContainer.hidden = !childContainer.hidden;
        row.querySelector(".caret").textContent = childContainer.hidden ? "\u203a" : "\u2304";
      }
      select(nodeId);
    });

    container.append(row);
    if (childContainer) {
      container.append(childContainer);
    }
  }

  return container;
}

function select(nodeId) {
  state.selectedId = nodeId;

  for (const row of document.querySelectorAll(".row.selected")) {
    row.classList.remove("selected");
  }
  const activeRow = document.querySelector(`.row[data-node-id="${cssEscape(nodeId)}"]`);
  if (activeRow) {
    expandAncestors(activeRow);
    activeRow.classList.add("selected");
    activeRow.scrollIntoView({ block: "nearest" });
  }

  const node = state.nodesById.get(nodeId);
  const contentElement = document.getElementById("content");
  contentElement.replaceChildren();

  const heading = document.createElement("h1");
  heading.textContent = node.title;
  contentElement.append(heading);

  if (node.content_md) {
    contentElement.append(renderBody(node));
  }

  const childIds = state.childrenBySource.get(nodeId) || [];
  for (const childId of childIds) {
    const childNode = state.nodesById.get(childId);
    if (childNode && childNode.is_toggle) {
      contentElement.append(renderToggle(childNode));
    }
  }

  contentElement.append(renderRelated(nodeId));
}

function expandAncestors(row) {
  let container = row.parentElement;

  while (container && container.id !== "tree") {
    if (container.classList.contains("children") && container.hidden) {
      container.hidden = false;
      const ancestorRow = container.previousElementSibling;
      if (ancestorRow) {
        const caret = ancestorRow.querySelector(".caret");
        if (caret) {
          caret.textContent = "⌄";
        }
      }
    }
    container = container.parentElement;
  }
}

function renderBody(node) {
  const body = document.createElement("div");
  body.innerHTML = renderMarkdown(node.content_md);
  return body;
}

function renderToggle(node) {
  const details = document.createElement("details");
  details.className = "toggle-section";

  const summary = document.createElement("summary");
  summary.textContent = node.title;
  details.append(summary);

  const body = document.createElement("div");
  body.innerHTML = renderMarkdown(node.content_md);
  details.append(body);

  return details;
}

function renderRelated(nodeId) {
  const container = document.createElement("div");
  container.className = "related";

  const relatedIds = state.relatedBySource.get(nodeId) || [];
  const heading = document.createElement("h3");
  heading.textContent = relatedIds.length ? "Related" : "No related topics";
  container.append(heading);

  for (const relatedId of relatedIds) {
    const relatedNode = state.nodesById.get(relatedId);
    if (!relatedNode) {
      continue;
    }
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.textContent = `${relatedNode.title} — ${relatedNode.page_title}`;
    chip.addEventListener("click", () => select(relatedId));
    container.append(chip);
  }

  return container;
}

function renderMarkdown(markdownText) {
  const escaped = escapeHtml(markdownText);
  const withCodeBlocks = escaped.replace(
    /```[a-z]*\n([\s\S]*?)```/g,
    (match, body) => `<pre><code>${body}</code></pre>`
  );
  const withInlineCode = withCodeBlocks.replace(/`([^`\n]+)`/g, "<code>$1</code>");
  const withBold = withInlineCode.replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");
  const withParagraphs = withBold
    .split(/\n{2,}/)
    .map((chunk) => (chunk.startsWith("<pre>") ? chunk : `<p>${chunk.replace(/\n/g, "<br>")}</p>`))
    .join("");
  return withParagraphs;
}

function escapeHtml(text) {
  const element = document.createElement("div");
  element.textContent = text;
  return element.innerHTML;
}

function cssEscape(value) {
  return value.replace(/["\\]/g, "\\$&");
}

load();
