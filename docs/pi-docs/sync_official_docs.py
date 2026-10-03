"""Re-sync the local Pi docs mirror from upstream.

Downloads every page listed in upstream docs.json (the same navigation pi.dev/docs/latest
renders), lays them out under official-docs/ by section, rewrites internal links, and
regenerates llm/pi-docs-combined.md.

Usage: uv run python docs/pi-docs/sync_official_docs.py
"""

import json
import re
import shutil
import urllib.request
from datetime import date
from pathlib import Path

REPO = "earendil-works/pi"  # formerly badlogic/pi-mono
RAW = f"https://raw.githubusercontent.com/{REPO}/main/packages/coding-agent/docs"
BLOB = f"https://github.com/{REPO}/blob/main/packages/coding-agent"
IMAGES = ["doom-extension.png", "exy.png", "interactive-mode.png", "tree-view.png"]

HERE = Path(__file__).resolve().parent
OUT = HERE / "official-docs"
COMBINED = HERE / "llm" / "pi-docs-combined.md"

SECTION_DIRS = {
    "Get Started": "01-get-started",
    "Guides/Run Pi": "02-run-pi",
    "Guides/Customize Pi": "03-customize-pi",
    "Guides/Build on Pi": "04-build-on-pi",
    "Reference": "05-reference",
}


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read()


def flatten(items, section):
    for item in items:
        if "path" in item:
            yield section, item["title"], item["path"]
        if "items" in item:
            yield from flatten(item["items"], f"{section}/{item['title']}")


def build_layout(nav):
    """Return [(section, title, upstream_name, local_relpath)] in navigation order."""
    pages, counters = [], {}
    for top in nav:
        for section, title, name in flatten(top.get("items", []), top["title"]):
            if section not in SECTION_DIRS:
                raise ValueError(f"Unknown docs.json section {section!r}; update SECTION_DIRS")
            folder = SECTION_DIRS[section]
            counters[folder] = counters.get(folder, 0) + 1
            pages.append((section, title, name, f"{folder}/{counters[folder]:02d}-{name}"))
    return pages


def rewrite_links(text: str, local_rel: str, mapping: dict, redirects: dict) -> str:
    depth = local_rel.count("/")
    up = "../" * depth

    def md_link(m):
        name, anchor = m.group(1), m.group(2) or ""
        name = redirects.get(name, name)
        if name not in mapping:
            return m.group(0)
        return f"]({up}{mapping[name]}{anchor})"

    # ../examples/... etc. point outside docs/ -> absolute GitHub links.
    # Must run before the page-link rewrite, which itself produces ../ paths.
    text = re.sub(r"\]\(\.\./([^)]+)\)", lambda m: f"]({BLOB}/{m.group(1)})", text)
    text = re.sub(r"\]\(([a-z0-9-]+\.md)(#[^)]*)?\)", md_link, text)
    text = text.replace('src="images/', f'src="{up}images/')
    return text


def main():
    docs_json = json.loads(fetch(f"{RAW}/docs.json"))
    redirects = {r["from"]: r["to"] for r in docs_json.get("redirects", [])}
    pages = build_layout(docs_json["navigation"])
    mapping = {name: rel for _, _, name, rel in pages}

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "images").mkdir(parents=True)
    for img in IMAGES:
        (OUT / "images" / img).write_bytes(fetch(f"{RAW}/images/{img}"))

    bodies = {}
    for _, _, name, rel in pages:
        text = fetch(f"{RAW}/{name}").decode("utf-8")
        text = rewrite_links(text, rel, mapping, redirects)
        (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
        (OUT / rel).write_text(text, encoding="utf-8")
        bodies[rel] = text

    today = date.today().isoformat()
    readme = [
        "# Pi Documentation (Local Mirror)",
        "",
        f"Mirrored from <https://pi.dev/docs/latest> on {today} — source: "
        f"[`{REPO}`](https://github.com/{REPO}/tree/main/packages/coding-agent/docs) "
        "(formerly `badlogic/pi-mono`).",
        "",
        "Organized to match the official navigation in `docs.json`. "
        "Re-sync with `uv run python docs/pi-docs/sync_official_docs.py`.",
    ]
    current = None
    for section, title, name, rel in pages:
        if section != current:
            current = section
            folder = SECTION_DIRS[section]
            readme += ["", f"## {section.split('/')[-1]} — [`{folder}/`]({folder}/)", ""]
        readme.append(f"- [{title}]({rel}) — `{name}`")
    readme_text = "\n".join(readme) + "\n"
    (OUT / "README.md").write_text(readme_text, encoding="utf-8")

    parts = [
        "# Pi Coding Agent — Combined Documentation",
        "",
        "> Combined from `official-docs/` for NotebookLM / LLM upload.",
        f"> Generated: {today}",
        "",
        "---",
        "",
    ]
    for rel, body in [("README.md", readme_text)] + list(bodies.items()):
        sep = "<!-- " + "=" * 60 + " -->"
        parts += ["", sep, f"<!-- SOURCE: {rel} -->", sep, "", body.rstrip(), ""]
    COMBINED.write_text("\n".join(parts), encoding="utf-8")
    print(f"Synced {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()
