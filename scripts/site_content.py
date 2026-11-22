"""The friendly introduction and setup flow; source docs stay in build_wiki.py."""
from __future__ import annotations

from html import escape
from typing import Callable


REPO = "https://github.com/TaterTotterson/Tater_Tunnel"


def icon(name: str) -> str:
    paths = {
        "link": '<path d="M9 7H7a5 5 0 0 0 0 10h2m6-10h2a5 5 0 0 1 0 10h-2M8 12h8"/>',
        "home": '<path d="m3 10 9-7 9 7v11h-7v-7h-4v7H3Z"/>',
        "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M10 5h4m-3 14h2"/>',
        "server": '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6h.01M7 17h.01M12 6h5m-5 11h5"/>',
        "apps": '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
        "key": '<circle cx="8" cy="8" r="5"/><path d="m12 12 9 9m-5-5 3-3m-6 0 3-3"/>',
        "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
        "book": '<path d="M12 5v16M2 3h5a5 5 0 0 1 5 3 5 5 0 0 1 5-3h5v16h-5a5 5 0 0 0-5 2 5 5 0 0 0-5-2H2Z"/>',
        "check": '<path d="m5 12 4 4L19 6"/>',
        "spark": '<path d="m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3Z"/>',
        "github": '<path d="M9 19c-5 2-5-3-7-3m14 6v-4a4 4 0 0 0-1-3c4-.5 6-2 6-6a5 5 0 0 0-1-3 5 5 0 0 0 0-4s-2-.5-4 1a14 14 0 0 0-8 0C6 1.5 4 2 4 2a5 5 0 0 0 0 4 5 5 0 0 0-1 3c0 4 2 5.5 6 6a4 4 0 0 0-1 3v4"/>',
    }
    return f'<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def render_home_body() -> str:
    return f'''
    <section class="tunnel-welcome">
      <div class="welcome-copy"><span class="welcome-tag">A little closer to home.</span>
        <h1>Your home apps.<br><span>Anywhere you go.</span></h1>
        <p>Bring Tater and your favorite local apps along for the day. Connect through a server you control, without opening ports on your home router.</p>
        <div class="action-row"><a class="button button-primary" href="setup/index.html">{icon('download')}Get started</a><a class="button button-secondary" href="#how-it-works">See how it works</a></div>
        <div class="welcome-notes"><span>{icon('home')}Self-hosted</span><span>{icon('phone')}Phone friendly</span><span>{icon('key')}Your devices</span></div>
      </div>
      <div class="welcome-art"><div class="art-orbit" aria-hidden="true"></div><img src="assets/images/tater-tunnel-hero.webp" alt="Tater bringing two network cables together" width="1717" height="916" fetchpriority="high"><span class="art-spark" aria-hidden="true">✳</span><div class="hello-sticker">Home, to go.<span>A little Tater connection.</span></div></div>
    </section>
    <div class="values-strip" aria-label="Run it your way"><p>Your VPS.</p><span aria-hidden="true">{icon('link')}</span><p>Your devices.</p><span aria-hidden="true">{icon('link')}</span><p>Your way home.</p><span aria-hidden="true">{icon('link')}</span></div>

    <section class="section connection-section" id="how-it-works">
      <div class="section-intro centered"><span class="eyebrow">Meet Tater Tunnel</span><h2>A familiar way<br>back home.</h2><p>Your VPS is a small server you rent. It connects your devices to a Home Agent running beside your apps.</p></div>
      <div class="connection-map" aria-label="Your device connects through your VPS to the Home Agent and the apps you choose">
        <div class="connection-node">{icon('phone')}<h3>Your device</h3><p>Connect with WireGuard.</p></div>
        <div class="connection-node">{icon('server')}<h3>Your VPS</h3><p>A meeting place online.</p></div>
        <div class="connection-node">{icon('home')}<h3>Your Home Agent</h3><p>A connection from home.</p></div>
        <div class="connection-node">{icon('apps')}<h3>Your apps</h3><p>Only the routes you add.</p></div>
      </div>
      <p class="connection-note">The Home Agent connects out to your VPS. Your home router stays as it is.</p>
    </section>

    <section class="section benefits" aria-label="A little more connected">
      <article>{icon('spark')}<h3>Take Tater with you.</h3><p>Reach your Tater setup from your phone or laptop when you're away.</p></article>
      <article>{icon('apps')}<h3>A path to your apps.</h3><p>Add named routes to the local services you want to use. <a href="routes/index.html">Explore app routes</a>.</p></article>
      <article>{icon('key')}<h3>Keep your circle small.</h3><p>Add devices from your Home Agent and revoke a device when it no longer belongs.</p></article>
    </section>

    <section class="section getting-started">
      <div class="section-intro"><span class="eyebrow">A little setup</span><h2>Two little pieces.<br>One way home.</h2><p>A VPS online. A Home Agent at home. A connection that brings them together.</p><ul class="bring-list"><li>{icon('check')}A Debian or Ubuntu VPS and a domain</li><li>{icon('check')}A home computer running your apps</li><li>{icon('check')}WireGuard on your phone or laptop</li></ul><a class="button" href="setup/index.html">Let's get connected</a><p class="small-note">You choose and manage your VPS. Hosting is separate.</p></div>
      <div class="setup-overview"><article><span class="step-number">1</span><div><h3>Give Tunnel a home online.</h3><p>The VPS installer gets your relay ready.</p></div></article><article><span class="step-number">2</span><div><h3>Bring your home along.</h3><p>Start the Home Agent and pair it with your VPS.</p></div></article><article><span class="step-number">3</span><div><h3>Make a little connection.</h3><p>Add your device, scan its WireGuard QR, and open an app route.</p></div></article><div class="overview-bottom">macOS app <span aria-hidden="true">·</span> Python <span aria-hidden="true">·</span> Docker</div></div>
    </section>

    <section class="section mobile-section"><figure><img src="assets/images/tater-mobile-qr.webp" alt="Illustration of Tater holding a phone with a QR pattern" width="1536" height="1024" loading="lazy"><figcaption>A little illustration. Your real QR comes from your Home Agent.</figcaption></figure><div class="section-intro"><span class="eyebrow">Made for out and about</span><h2>Scan. Connect.<br>Feel at home.</h2><p>Create a device profile in your Home Agent, then scan its QR with the WireGuard app. Turn on the connection and use your approved app routes.</p><a class="text-link" href="setup/index.html#add-device">Set up your first device</a></div></section>

    <section class="section faq-section"><div class="section-intro"><span class="eyebrow">A few good questions</span><h2>Curious potatoes<br>welcome.</h2></div><div class="faq-list">
      <details><summary>Do I need my own VPS?</summary><p>Yes. Tater Tunnel uses a VPS you choose and manage, plus a Home Agent on your home computer. The setup guide covers a fresh Debian or Ubuntu VPS and an existing server.</p></details>
      <details><summary>Do I need to open ports at home?</summary><p>The Home Agent makes an outbound connection to your VPS, so you do not need inbound port forwarding on your home router. The VPS still needs the ports described in the setup guide.</p></details>
      <details><summary>Does this connect my entire home network?</summary><p>The default path is for the app routes you choose. It does not give a device unrestricted access to every machine on your network, and it is not a full-internet VPN service.</p></details>
      <details><summary>What can run the Home Agent?</summary><p>There is a macOS menu bar app, plus Python and Docker options. Remote phones and laptops connect with a WireGuard profile generated by the Home Agent.</p></details>
      <details><summary>What if I lose my phone?</summary><p>Revoke that device in your Home Agent. This removes its device record and the corresponding WireGuard peer on your VPS. <a href="security/index.html">Read about access and security</a>.</p></details>
    </div></section>
    <section class="section community-band"><span class="community-spark" aria-hidden="true">✳</span><div><span class="eyebrow">Good things grow together</span><h2>Let's stay connected.</h2><p>Have a question or an idea for Tunnel? Come build along.</p></div><a class="button button-secondary" href="{REPO}">{icon('github')}Find Tunnel on GitHub</a></section>
    '''


def render_setup_body(command_box: Callable[[str, str], str], install_command: str) -> str:
    terminal = f"git clone {REPO}.git\ncd Tater_Tunnel\npython3 -m tater_tunnel.home_agent --host 127.0.0.1 --port 4173"
    docker = "docker run -d --name tater-tunnel-home \\\n  -p 127.0.0.1:4173:4173 \\\n  -v tater-tunnel-home-data:/data \\\n  -v tater-tunnel-home-config:/config \\\n  ghcr.io/tatertotterson/tater-tunnel:latest home"
    root_command = install_command.replace("sudo bash", "bash")
    return f'''
    <section class="sub-hero"><span class="eyebrow">Let's get connected</span><h1>A little setup.<br><span>A way back home.</span></h1><p>Start with your VPS, add the Home Agent, then connect your first device.</p><div class="prerequisites"><span>{icon('server')}Debian or Ubuntu VPS</span><span>{icon('home')}A home computer</span><span>{icon('phone')}WireGuard app</span></div></section>
    <div class="section setup-layout"><aside class="setup-toc" aria-label="Setup steps"><span class="eyebrow">Your path home</span><a href="#vps-setup">1. Prepare your VPS</a><a href="#home-agent">2. Get the Home Agent</a><a href="#pair-vps">3. Pair them together</a><a href="#add-device">4. Add your device</a></aside>
    <div class="setup-guide">
      <section class="setup-step" id="vps-setup"><span class="step-label">Step 1 · On your VPS</span><h2>Give Tunnel a place online.</h2><p>SSH into your Debian or Ubuntu VPS. Have a domain pointed at it, then run the setup command as a user with sudo access.</p>{command_box(install_command, 'Run on your VPS')}
        <p>The installer walks you through the setup. Choose the path that fits your server:</p><ul class="choice-list"><li><strong>Blank VPS full install</strong><span>Sets up the agent, WireGuard, Caddy HTTPS, and firewall rules.</span></li><li><strong>Advanced existing VPS</strong><span>Installs the agent. You manage your existing reverse proxy and firewall.</span></li><li><strong>Update existing install</strong><span>Refreshes the code while preserving pairing and device state.</span></li></ul>
        <details class="guide-disclosure"><summary>Starting as root on a brand-new VPS?</summary><p>Run the command without sudo. The menu helps create a sudo user and explains how to reconnect before installing Tunnel.</p>{command_box(root_command, 'Fresh VPS, logged in as root')}</details>
        <p>Keep the pairing code from the installer. <a href="../wiki/vps-install.html">Read the full VPS guide</a> for DNS, HTTPS, and firewall details.</p>
      </section>
      <section class="setup-step" id="home-agent"><span class="step-label">Step 2 · At home</span><h2>Bring your home along.</h2><p>Run the Home Agent on a computer that can reach the apps you want to use.</p>
        <div class="setup-picker" data-tabs><div class="setup-tabs" role="tablist" aria-label="Home Agent installation"><a role="tab" id="tab-mac" href="#home-mac" aria-controls="home-mac" aria-selected="true">macOS app</a><a role="tab" id="tab-python" href="#home-python" aria-controls="home-python" aria-selected="false">Python</a><a role="tab" id="tab-docker" href="#home-docker" aria-controls="home-docker" aria-selected="false">Docker</a></div>
          <section class="setup-panel" role="tabpanel" id="home-mac" aria-labelledby="tab-mac" tabindex="0"><h3>A little app in your menu bar.</h3><p>Download the macOS release, open the DMG, and install Tater Tunnel. The app starts the Home Agent for you.</p><p class="small-note">Requires macOS 13 or newer.</p><a class="button" href="{REPO}/releases/latest">{icon('download')}Get the Mac app</a></section>
          <section class="setup-panel" role="tabpanel" id="home-python" aria-labelledby="tab-python" tabindex="0"><h3>Run it from your terminal.</h3><p>With Git and Python 3.11 or newer installed, clone the project and start the Home Agent. Keep it running while you use Tunnel.</p>{command_box(terminal, 'On your home computer')}</section>
          <section class="setup-panel" role="tabpanel" id="home-docker" aria-labelledby="tab-docker" tabindex="0"><h3>A spot in your Docker setup.</h3><p>With Docker installed, run the Home Agent with persistent state and config volumes.</p>{command_box(docker, 'On your Docker host')}<p class="small-note">For routes to other containers, use an address reachable from this container. Its localhost is separate from the host's.</p></section>
        </div><p>Open <code>http://127.0.0.1:4173/</code> on the computer running the Home Agent.</p>
      </section>
      <section class="setup-step" id="pair-vps"><span class="step-label">Step 3 · Bring them together</span><h2>Make the first connection.</h2><p>In your Home Agent, enter the VPS address and the pairing code from the installer.</p><dl class="pairing-values"><div><dt>VPS IP or Domain</dt><dd><code>https://tunnel.example.com</code></dd></div><div><dt>Pairing Code</dt><dd>The code from your VPS installer</dd></div><div><dt>Security Mode</dt><dd>standard</dd></div></dl><p>Use your own domain in place of the example. Once the VPS is claimed and connected, you're ready to add a device.</p></section>
      <section class="setup-step" id="add-device"><span class="step-label">Step 4 · On your phone or laptop</span><h2>Your home, to go.</h2><ol class="number-list"><li>Add a device in your Home Agent to generate a WireGuard profile.</li><li>Scan its QR or import its config in your device's WireGuard app.</li><li>Enable the connection and open the relay health address below.</li></ol>{command_box('http://10.88.0.1:4174/api/health', 'Open on the connected device')}<p>Next, <a href="../routes/index.html">add an app route</a> in your Home Agent and open its displayed Use URL from your device.</p></section>
      <div class="help-callout"><div><h3>Need a hand getting home?</h3><p>Follow the checks for pairing, WireGuard, or app routes.</p></div><a class="button button-secondary" href="../troubleshooting/index.html">Find a fix</a></div>
    </div></div>'''


def render_docs_body(docs: list[dict[str, str]]) -> str:
    guides = [
        ("Get connected", "VPS setup, your Home Agent, and your first device.", "../setup/index.html", "macos python docker install pairing qr"),
        ("Add an app route", "Choose the apps you want to reach while you're away.", "../routes/index.html", "local target websocket emby home assistant"),
        ("Access & security", "Understand devices, your relay, and firewall ports.", "../security/index.html", "wireguard trust revoke vpn https caddy"),
        ("Find a fix", "Get unstuck with pairing, connections, or an app page.", "../troubleshooting/index.html", "help troubleshoot handshake blank firewall"),
    ]
    summaries = {
        "readme": "The full project guide, runtime options, and release links.",
        "vps-install": "Detailed server installation, updates, and maintenance.",
        "trust-boundaries": "How the Home Agent and VPS share responsibilities.",
        "mvp-spec": "Project scope, current direction, and the technical model.",
    }
    for doc in docs:
        guides.append((doc['title'], summaries.get(doc['slug'], doc['summary']), f"{doc['slug']}.html", "reference source " + doc['slug'].replace('-', ' ')))
    cards = ''.join(f'<a class="guide-link" href="{escape(href)}" data-guide data-keywords="{escape(keywords)}"><h2>{escape(title)}</h2><p>{escape(summary)}</p><span>Read guide</span></a>' for title, summary, href, keywords in guides)
    return f'''<section class="sub-hero docs-intro"><span class="eyebrow">The Tater Tunnel field guide</span><h1>A little guidance.<br><span>A closer connection.</span></h1><p>From your first VPS to your favorite home app. Find the help you need.</p><label class="guide-search"><span>Find a guide</span><input type="search" placeholder="Try Docker, pairing, or routes…" data-guide-search></label><p class="small-note" role="status" data-guide-count>{len(guides)} guides to help you get connected.</p></section><section class="section guide-grid" aria-label="Guides">{cards}</section><p class="section guide-empty" data-guide-empty hidden>No matching guides. Try a device, feature, or setup step.</p>'''
