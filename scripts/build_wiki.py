#!/usr/bin/env python3
from __future__ import annotations

import html
import hashlib
import json
import re
import shutil
import textwrap
import os
from pathlib import Path

from site_content import icon, render_home_body, render_setup_body, render_docs_body


SCRIPT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = SCRIPT_DIR.parent
PUBLIC_ROOT = WEBSITE_DIR / "public_html"
ASSET_DIR = PUBLIC_ROOT / "assets"
IMAGE_DIR = ASSET_DIR / "images"

GITHUB_REPO = "https://github.com/TaterTotterson/Tater_Tunnel"
ONE_COMMAND_INSTALL = """curl -fsSL https://raw.githubusercontent.com/TaterTotterson/Tater_Tunnel/main/scripts/tater-vps-setup.sh \\
  -o /tmp/tater-vps-setup.sh && sudo bash /tmp/tater-vps-setup.sh"""
ROUTE_EXAMPLES_COMMAND = """Route name: tater
Local target: http://127.0.0.1:8501
Use: http://10.88.0.1:4174/relay/tater/

Route name: emby
Local target: http://10.4.20.204:8096
Use: http://10.88.0.1:4174/relay/emby/"""
SECURITY_CHECKS_COMMAND = """curl -fsS https://tunnel.example.com/api/health
sudo wg show tater0
sudo ufw status verbose"""
HEALTH_CHECKS_COMMAND = """curl -fsS https://tunnel.example.com/api/health
sudo wg show tater0
curl -fsS http://10.88.0.1:4174/api/health
curl -fsS http://10.88.0.1:4174/relay/api/state"""
VPS_SERVICE_COMMAND = """sudo systemctl status tater-tunnel-vps
sudo journalctl -u tater-tunnel-vps -f
sudo systemctl restart tater-tunnel-vps"""

NAV_ITEMS = [
    ("setup", "Get started", "setup/index.html"),
    ("routes", "App routes", "routes/index.html"),
    ("docs", "Docs", "wiki/index.html"),
]

DOC_SOURCES = [
    ("readme", "Project README", "README.md"),
    ("vps-install", "VPS Install", "docs/VPS_INSTALL.md"),
    ("trust-boundaries", "Trust Boundaries", "docs/TRUST_BOUNDARIES.md"),
    ("mvp-spec", "MVP Spec", "docs/MVP_SPEC.md"),
]


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def resolve_path(env_name: str, *candidates: Path) -> Path:
    override = str(os.getenv(env_name, "") or "").strip()
    if override:
        return Path(override).expanduser().resolve()
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[0].resolve()


TUNNEL_SOURCE_DIR = resolve_path(
    "TATER_TUNNEL_SOURCE_DIR",
    WEBSITE_DIR / "Tater_Tunnel",
    WEBSITE_DIR.parent / "Tater_Tunnel",
)


def ensure_dirs() -> None:
    PUBLIC_ROOT.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def copy_root_asset(source: Path, target_name: str) -> None:
    target = IMAGE_DIR / target_name
    if source.exists() and not target.exists():
        shutil.copy2(source, target)


def page_base(depth: int) -> str:
    return "../" * depth


def asset_version(filename: str) -> str:
    return hashlib.sha256((ASSET_DIR / filename).read_bytes()).hexdigest()[:12]


def nav_html(base: str, active: str) -> str:
    links = []
    for key, label, href in NAV_ITEMS:
        current = ' aria-current="page"' if key == active else ''
        links.append(f'<a class="nav-link" href="{base}{href}"{current}>{escape(label)}</a>')
    links.append(f'<a class="nav-link nav-link-github" href="{GITHUB_REPO}">{icon("github")}GitHub</a>')
    return "\n".join(links)


def page_template(title: str, description: str, body: str, *, nav_key: str, depth: int = 0) -> str:
    base = page_base(depth)
    breadcrumb = "" if nav_key == "home" else f'<div class="docs-breadcrumb"><a href="{base}wiki/index.html">Tater Tunnel guides</a><span aria-hidden="true">/</span><span>{escape(title.split("|")[-1].strip())}</span></div>'
    return textwrap.dedent(f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta name="description" content="{escape(description)}">
          <meta name="theme-color" content="#17191b">
          <meta property="og:type" content="website">
          <meta property="og:title" content="{escape(title)}">
          <meta property="og:description" content="{escape(description)}">
          <meta property="og:image" content="https://tatertunnel.com/assets/images/tater-tunnel-hero.png">
          <meta name="twitter:card" content="summary_large_image">
          <title>{escape(title)}</title>
          <link rel="preload" href="{base}assets/fonts/nunito-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
          <link rel="stylesheet" href="{base}assets/site.css?v={asset_version('site.css')}">
          <script src="{base}assets/site.js?v={asset_version('site.js')}" defer></script>
        </head>
        <body data-page="{escape(nav_key)}">
          <a class="skip-link" href="#main-content">Skip to content</a>
          <header class="site-header">
            <a class="brand" href="{base}index.html" aria-label="Tater Tunnel home"><img src="{base}assets/images/tater-logo-primary.png" alt="Tater" width="1535" height="1024"><span>Tunnel</span></a>
            <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">☰</span></button>
            <nav class="site-nav" id="site-nav" aria-label="Main navigation">{nav_html(base, nav_key)}</nav>
          </header>
          <main id="main-content" tabindex="-1">{breadcrumb}{body}</main>
          <footer class="site-footer">
            <div class="footer-main"><div class="footer-brand"><a class="brand" href="{base}index.html" aria-label="Tater Tunnel home"><img src="{base}assets/images/tater-logo-primary.png" alt="Tater" width="1535" height="1024" loading="lazy"><span>Tunnel</span></a><p>A little closer to home.</p></div><div class="footer-column"><h2>Get connected</h2><a href="{base}setup/index.html">Start setup</a><a href="{base}setup/index.html#home-agent">Get the Home Agent</a><a href="{base}routes/index.html">Add an app route</a></div><div class="footer-column"><h2>A little guidance</h2><a href="{base}wiki/index.html">All guides</a><a href="{base}security/index.html">Access &amp; security</a><a href="{base}troubleshooting/index.html">Troubleshooting</a></div><div class="footer-column"><h2>Come say hello</h2><a href="{GITHUB_REPO}">Tunnel on GitHub</a><a href="{GITHUB_REPO}/issues">Ideas &amp; issues</a><a href="https://taterassistant.com">Meet Tater Assistant</a><a href="https://tatertube.tv">Meet Tater Tube</a></div></div>
            <div class="footer-bottom"><p>Your VPS. Your devices. Your way home.</p><a href="https://github.com/TaterTotterson/Tater_Tunnel-Website/blob/main/LICENSE">Open source</a><a href="#">Back to top</a></div>
          </footer>
        </body>
        </html>
        """)


def chip(label: str) -> str:
    return f'<span class="chip">{escape(label)}</span>'


def action_link(label: str, href: str, *, secondary: bool = False) -> str:
    class_name = "button button-secondary" if secondary else "button"
    return f'<a class="{class_name}" href="{escape(href)}">{escape(label)}</a>'


def command_box(command: str, label: str = "Terminal") -> str:
    return textwrap.dedent(
        f"""\
        <div class="command-box">
          <div class="command-head">
            <span>{escape(label)}</span>
            <button type="button" data-copy-code>Copy</button>
          </div>
          <pre><code>{escape(command.strip())}</code></pre>
        </div>
        """
    )


def simple_card(title: str, text: str, chips: list[str] | None = None) -> str:
    chip_html = f'<div class="chip-row">{"".join(chip(item) for item in chips or [])}</div>' if chips else ""
    return textwrap.dedent(
        f"""\
        <article class="info-card">
          <h3>{escape(title)}</h3>
          <p>{escape(text)}</p>
          {chip_html}
        </article>
        """
    )


def image_panel(src: str, alt: str, caption: str, base: str) -> str:
    return textwrap.dedent(
        f"""\
        <figure class="image-panel">
          <img src="{base}assets/images/{escape(src.replace(".png", ".webp"))}" alt="{escape(alt)}">
          <figcaption>{escape(caption)}</figcaption>
        </figure>
        """
    )


def render_home_page() -> str:
    return page_template(
        "Tater Tunnel | Your home apps. Anywhere you go.",
        "Bring Tater and your favorite local apps with you. Connect through a VPS you control without opening ports on your home router.",
        render_home_body(), nav_key="home",
    )


def render_setup_page() -> str:
    return page_template(
        "Tater Tunnel | Get connected",
        "Set up your VPS, get the Tater Tunnel Home Agent for macOS, Python, or Docker, and connect your first device.",
        render_setup_body(command_box, ONE_COMMAND_INSTALL), nav_key="setup", depth=1,
    )


def render_routes_page() -> str:
    base = "../"
    body = f"""
    <section class="sub-hero">
      <span class="eyebrow">Routes</span>
      <h1>Your apps.<br><span>Your little routes.</span></h1>
      <p>Routes are named paths under the VPS relay. The phone opens the VPS tunnel IP, and the Home Agent proxies the request to a Tater service or any local app target you choose.</p>
    </section>

    <section class="section">
      <div class="route-example">
        <div>
          <span class="eyebrow">Default</span>
          <h2>Home Agent and Tunnel UI</h2>
          <p>The built-in tunnel route is available at the base relay path after the phone is connected to WireGuard.</p>
        </div>
        <code>http://10.88.0.1:4174/relay/</code>
      </div>
      <div class="route-example">
        <div>
          <span class="eyebrow">Named route</span>
          <h2>Main Tater app</h2>
          <p>Add a route named <code>tater</code> to the Home Agent UI and point it at the local Tater app port.</p>
        </div>
        <code>http://10.88.0.1:4174/relay/tater/</code>
      </div>
      <div class="route-example">
        <div>
          <span class="eyebrow">LAN target</span>
          <h2>Another local service</h2>
          <p>Targets can also be another LAN machine if the Home Agent machine can reach it, for example an Emby host.</p>
        </div>
        <code>http://10.88.0.1:4174/relay/emby/</code>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Route settings</span>
        <h2>A few settings.<br>A better connection.</h2>
      </div>
      <div class="grid grid-3">
        {simple_card("Target URL", "The local URL the Home Agent can reach, such as http://127.0.0.1:8501 or http://10.4.20.204:8096.", ["Required"])}
        {simple_card("WebSockets", "Enable for apps that keep live UI state over WebSockets, streaming, or long-lived browser sessions.", ["Advanced"])}
        {simple_card("Host header", "Use only when an app expects its own public host or rejects the relay host.", ["Advanced"])}
      </div>
    </section>

    <section class="section split-section split-section-reverse">
      {image_panel("tater-mobile-qr.png", "Tater mascot with mobile QR setup", "Once the phone VPN is on, every route uses the 10.88.0.1 VPS tunnel address.", base)}
      <div class="split-copy">
        <span class="eyebrow">Examples</span>
        <h2>Route names become clean URLs.</h2>
        {command_box(ROUTE_EXAMPLES_COMMAND, "Access route examples")}
      </div>
    </section>
    """
    return page_template(
        "Tater Tunnel | Routes",
        "Add and test approved Tater Tunnel routes for Tater services or other local apps from the Home Agent UI.",
        body,
        nav_key="routes",
        depth=1,
    )


def render_security_page() -> str:
    body = f"""
    <section class="sub-hero">
      <span class="eyebrow">Security</span>
      <h1>Your connections.<br><span>Your control.</span></h1>
      <p>The Home Agent owns device approval, relay tokens, route targets, and revocation. The VPS should hold only enough state to relay traffic and manage WireGuard peers.</p>
    </section>

    <section class="section">
      <div class="grid grid-2">
        {simple_card("TLS for Home Agent to VPS", "The full setup path puts Caddy in front of the VPS Agent so pairing and relay management happen over HTTPS with automatic certificates.", ["Caddy", "443/tcp"])}
        {simple_card("WireGuard for remote devices", "Phones and laptops use WireGuard to reach the VPS tunnel address. This gives the mobile VPN behavior users expect.", ["51888/udp", "QR profile"])}
        {simple_card("Token-protected management", "After claim, sensitive VPS endpoints require the relay management token from the Home Agent.", ["No public state dump"])}
        {simple_card("Revocation removes access", "Revoking a device removes the WireGuard peer and the Home Agent device record.", ["Lost device flow"])}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Firewall shape</span>
        <h2>Blank VPS install keeps the raw agent port private.</h2>
      </div>
      <div class="port-table">
        <div><strong>80/tcp</strong><span>Caddy HTTP and ACME challenge</span></div>
        <div><strong>443/tcp</strong><span>Caddy HTTPS to 127.0.0.1:4174</span></div>
        <div><strong>51888/udp</strong><span>WireGuard device VPN</span></div>
        <div><strong>4174/tcp</strong><span>Localhost for Caddy, and tater0-only for VPN relay use</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Hardening checklist</span>
        <h2>Before calling a setup production-ready.</h2>
      </div>
      <ul class="check-list">
        <li>Use a real DNS name and HTTPS URL for Home Agent to VPS pairing.</li>
        <li>Keep public TCP 4174 closed unless doing a short direct test.</li>
        <li>Open UDP 51888 for WireGuard devices.</li>
        <li>Use the Home Agent UI to revoke old or lost devices.</li>
        <li>Keep route targets narrow. Do not expose raw LAN access by default.</li>
        <li>Update the VPS with the same one-command installer when new tunnel fixes land.</li>
      </ul>
    </section>

    <section class="section">
      {command_box(SECURITY_CHECKS_COMMAND, "Security checks")}
    </section>
    """
    return page_template(
        "Tater Tunnel | Security",
        "Tater Tunnel security model, trust boundaries, TLS, WireGuard, firewall ports, and hardening checklist.",
        body,
        nav_key="security",
        depth=1,
    )


def render_troubleshooting_page() -> str:
    body = f"""
    <section class="sub-hero">
      <span class="eyebrow">Troubleshooting</span>
      <h1>A little help.<br><span>Back on track.</span></h1>
      <p>Most tunnel issues are one of four things: pairing, VPS firewall, WireGuard handshake, or a route target that needs a base URL/WebSocket tweak.</p>
    </section>

    <section class="section">
      <div class="grid grid-2">
        {simple_card("Pairing says disabled", "That is normal after the VPS is claimed. Pairing mode should turn off so random new Home Agents cannot claim the VPS.", ["Expected after claim"])}
        {simple_card("Phone internet IP is not the VPS", "The current profile is for tunnel access to Tater routes, not always-full internet egress. Test 10.88.0.1 routes instead.", ["Split tunnel"])}
        {simple_card("No WireGuard handshake", "Confirm UDP 51888 is open on the VPS firewall and cloud firewall, then check sudo wg show tater0.", ["Firewall first"])}
        {simple_card("Blank route page", "Test the local target from the Home Agent machine. Then enable WebSockets or set the app's own base/public URL if it hard-codes assets.", ["Route health"])}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Quick checks</span>
        <h2>Run the smallest possible test for each hop.</h2>
      </div>
      {command_box(HEALTH_CHECKS_COMMAND, "Health checks")}
      {command_box(VPS_SERVICE_COMMAND, "VPS service")}
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Route debug pattern</span>
        <h2>Use the Home Agent route test before trying the phone.</h2>
      </div>
      <ol class="number-list">
        <li>Confirm the Home Agent UI shows the VPS as claimed and connected.</li>
        <li>Open the local target from the Home Agent machine.</li>
        <li>Use the route Test button in Access Routes.</li>
        <li>Connect the phone to WireGuard and open the displayed Use URL.</li>
        <li>If the page partially loads, enable WebSockets or configure that app's public/base URL.</li>
      </ol>
    </section>
    """
    return page_template(
        "Tater Tunnel | Troubleshooting",
        "Tater Tunnel troubleshooting checks for pairing, WireGuard, firewall, relay routes, and services.",
        body,
        nav_key="troubleshooting",
        depth=1,
    )


def render_inline_markdown(text: str) -> str:
    code_tokens: list[str] = []

    def save_code(match: re.Match[str]) -> str:
        code_tokens.append(f"<code>{escape(match.group(1))}</code>")
        return f"@@CODE{len(code_tokens) - 1}@@"

    tokenized = re.sub(r"`([^`]+)`", save_code, text)
    rendered = escape(tokenized)

    def link_replace(match: re.Match[str]) -> str:
        label = match.group(1)
        href = match.group(2)
        return f'<a href="{escape(href)}">{escape(label)}</a>'

    rendered = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replace, rendered)
    for index, code_html in enumerate(code_tokens):
        rendered = rendered.replace(f"@@CODE{index}@@", code_html)
    return rendered


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    html_parts: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    ordered_items: list[str] = []
    code_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        if paragraph:
            html_parts.append(f"<p>{render_inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            html_parts.append("<ul>" + "".join(f"<li>{render_inline_markdown(item)}</li>" for item in list_items) + "</ul>")
            list_items.clear()
        if ordered_items:
            html_parts.append("<ol>" + "".join(f"<li>{render_inline_markdown(item)}</li>" for item in ordered_items) + "</ol>")
            ordered_items.clear()

    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith("```"):
            if in_code:
                html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                flush_paragraph()
                flush_list()
                in_code = True
            continue
        if in_code:
            code_lines.append(stripped)
            continue
        if not stripped:
            flush_paragraph()
            flush_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            html_parts.append(f"<h{level}>{render_inline_markdown(heading.group(2))}</h{level}>")
            continue
        bullet = re.match(r"^-\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            ordered_items.clear()
            list_items.append(bullet.group(1))
            continue
        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            flush_paragraph()
            list_items.clear()
            ordered_items.append(numbered.group(1))
            continue
        paragraph.append(stripped)

    if in_code:
        html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    flush_paragraph()
    flush_list()
    return "\n".join(html_parts)


def doc_summary(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", "```", "Website:")):
            return stripped
    return "Generated from the current Tater Tunnel source tree."


def render_docs_index(docs: list[dict[str, str]]) -> str:
    return page_template(
        "Tater Tunnel | Docs",
        "Setup guides and reference for your VPS, Home Agent, app routes, and devices.",
        render_docs_body(docs), nav_key="docs", depth=1,
    )


def render_doc_page(doc: dict[str, str]) -> str:
    content = re.sub(r"^<h1>.*?</h1>\s*", "", doc["html"], count=1)
    content = re.sub(r"^<p>Website:.*?</p>\s*", "", content, count=1)
    introduction = f'<p>{render_inline_markdown(doc["summary"])}</p>'
    if content.startswith(introduction):
        content = content[len(introduction):].lstrip()
    body = f"""
    <section class="sub-hero doc-sub-hero">
      <span class="eyebrow">Tater Tunnel reference</span>
      <h1>{escape(doc['title'])}</h1>
      <p>{escape(doc['summary'])}</p>
    </section>
    <article class="section doc-content">
      {content}
    </article>
    """
    return page_template(
        f"Tater Tunnel | {doc['title']}",
        doc["summary"],
        body,
        nav_key="docs",
        depth=1,
    )


def write_file(relative_path: str, contents: str) -> None:
    target = PUBLIC_ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(contents, encoding="utf-8")


def build_docs() -> list[dict[str, str]]:
    docs: list[dict[str, str]] = []
    for slug, title, relative_path in DOC_SOURCES:
        path = TUNNEL_SOURCE_DIR / relative_path
        if not path.exists():
            continue
        markdown = re.sub(r"\bpython3\.\d+\b", "python3", path.read_text(encoding="utf-8"))
        docs.append(
            {
                "slug": slug,
                "title": title,
                "source": relative_path,
                "summary": doc_summary(markdown),
                "html": render_markdown(markdown),
            }
        )
    return docs


def main() -> None:
    ensure_dirs()
    copy_root_asset(TUNNEL_SOURCE_DIR / "assets" / "tater-logo-primary.png", "tater-logo-primary.png")

    docs = build_docs()
    write_file("index.html", render_home_page())
    write_file("setup/index.html", render_setup_page())
    write_file("routes/index.html", render_routes_page())
    write_file("security/index.html", render_security_page())
    write_file("troubleshooting/index.html", render_troubleshooting_page())
    write_file("wiki/index.html", render_docs_index(docs))
    for doc in docs:
        write_file(f"wiki/{doc['slug']}.html", render_doc_page(doc))

    manifest = {
        "generator": "scripts/build_wiki.py",
        "sourceRoot": str(TUNNEL_SOURCE_DIR.name),
        "pages": [
            "index.html",
            "setup/index.html",
            "routes/index.html",
            "security/index.html",
            "troubleshooting/index.html",
            "wiki/index.html",
            *[f"wiki/{doc['slug']}.html" for doc in docs],
        ],
        "docs": [{"title": doc["title"], "source": doc["source"], "output": f"wiki/{doc['slug']}.html"} for doc in docs],
    }
    write_file("site-manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(f"Built Tater Tunnel website at {PUBLIC_ROOT}")


if __name__ == "__main__":
    main()
