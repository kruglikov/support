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
    if (node.is_toggle) {
      contentElement.append(renderToggle(node));
    } else {
      contentElement.append(renderBody(node));
    }
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

  const relatedIds = [...new Set(state.relatedBySource.get(nodeId) || [])];
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

function renderLinks(text) {
  return text.replace(/\[([^\]\n]*)\]\(([^)\s]+)\)/g, (match, label, target) => {
    if (target.startsWith("notion://")) {
      const nodeId = target.slice("notion://".length);
      return `<a href="#" class="xref" data-node-id="${nodeId}">${label}</a>`;
    }
    if (/^https?:\/\//.test(target)) {
      return `<a href="${target}" target="_blank" rel="noopener noreferrer">${label}</a>`;
    }
    return match;
  });
}

function renderChunk(chunk) {
  if (/^%%CODEBLOCK\d+%%$/.test(chunk)) {
    return chunk;
  }

  const lines = chunk.split("\n");
  const parts = [];
  let listItems = [];
  let listTag = null;
  let textLines = [];

  const flushList = () => {
    if (listItems.length) {
      parts.push(`<${listTag}>${listItems.join("")}</${listTag}>`);
      listItems = [];
      listTag = null;
    }
  };

  const flushText = () => {
    if (textLines.length) {
      parts.push(`<p>${textLines.join("<br>")}</p>`);
      textLines = [];
    }
  };

  for (const line of lines) {
    const bulletMatch = line.match(/^\s*[-*]\s+(.*)$/);
    const numberMatch = line.match(/^\s*\d+\.\s+(.*)$/);
    const headingMatch = line.match(/^(#{1,6})\s+(.*\S)\s*$/);

    if (bulletMatch) {
      flushText();
      if (listTag && listTag !== "ul") {
        flushList();
      }
      listTag = "ul";
      listItems.push(`<li>${bulletMatch[1]}</li>`);
      continue;
    }

    if (numberMatch) {
      flushText();
      if (listTag && listTag !== "ol") {
        flushList();
      }
      listTag = "ol";
      listItems.push(`<li>${numberMatch[1]}</li>`);
      continue;
    }

    if (headingMatch) {
      flushText();
      flushList();
      const level = Math.min(headingMatch[1].length + 1, 6);
      parts.push(`<h${level}>${headingMatch[2]}</h${level}>`);
      continue;
    }

    flushList();
    textLines.push(line);
  }

  flushText();
  flushList();
  return parts.join("");
}

function renderMarkdown(markdownText) {
  const escaped = escapeHtml(markdownText);

  const codeBlocks = [];
  const withPlaceholders = escaped.replace(
    /```[^\n]*\n([\s\S]*?)```/g,
    (match, body) => {
      const placeholder = `%%CODEBLOCK${codeBlocks.length}%%`;
      codeBlocks.push(`<pre><code>${body}</code></pre>`);
      return placeholder;
    }
  );

  const withInlineCode = withPlaceholders.replace(/`([^`\n]+)`/g, "<code>$1</code>");
  const withLinks = renderLinks(withInlineCode);
  const withBold = withLinks.replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");
  const withItalic = withBold.replace(/(^|[^*\w])\*([^*\n]+)\*(?![*\w])/g, "$1<em>$2</em>");

  const withBlocks = withItalic.split(/\n{2,}/).map(renderChunk).join("");

  const withCodeBlocks = withBlocks.replace(
    /%%CODEBLOCK(\d+)%%/g,
    (match, index) => codeBlocks[Number(index)]
  );
  return withCodeBlocks;
}

function escapeHtml(text) {
  const element = document.createElement("div");
  element.textContent = text;
  return element.innerHTML;
}

function cssEscape(value) {
  return value.replace(/["\\]/g, "\\$&");
}

document.getElementById("content").addEventListener("click", (event) => {
  const crossReference = event.target.closest("a.xref");
  if (!crossReference) {
    return;
  }
  event.preventDefault();
  const nodeId = crossReference.dataset.nodeId;
  if (state.nodesById.has(nodeId)) {
    select(nodeId);
  }
});

load();
