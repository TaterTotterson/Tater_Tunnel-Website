# Tater Tunnel Website

This folder contains the static website and generated docs for Tater Tunnel.

## Editing the site

- `scripts/site_content.py` contains the homepage, guided setup, and searchable guide directory.
- `scripts/build_wiki.py` generates the pages, shared header and footer, route/security guides, and source documentation.
- `public_html/assets/site.css` defines the shared orange-and-charcoal Tater design, responsive layouts, and self-hosted Nunito font.
- `public_html/assets/site.js` handles the mobile menu, keyboard-accessible setup tabs, guide search, and command copying.

Edit the source modules rather than the generated HTML. CSS and JavaScript URLs use content hashes so rebuilds refresh browser caches. The existing Python build and update commands still work; there is no frontend package installation step.

## Build

```bash
python3 scripts/build_wiki.py
```

The output is written to:

```text
public_html/
```

## Update

Run the update wrapper after changing the app docs or website script:

```bash
python3 scripts/update_site.py
```

Use `--check` in CI or before pushing when you want the command to fail if the
generated site output differs from the committed tree.

```bash
python3 scripts/update_site.py --check
```

## Preview

The site is plain static HTML. You can open `public_html/index.html`
directly, or serve the folder with any static server.

```bash
python3 -m http.server 8080 -d public_html
```

## Source Sync

The builder reads source docs from a Tater Tunnel checkout. By default it uses
`./Tater_Tunnel` if present, then a sibling `../Tater_Tunnel` checkout. To clone
or update `./Tater_Tunnel`, run:

```bash
python3 scripts/sync_wiki_sources.py
```

You can point at a different checkout without cloning:

```bash
TATER_TUNNEL_SOURCE_DIR=/path/to/Tater_Tunnel python3 scripts/build_wiki.py
```

## Generated Images

Mascot images were generated with the built-in image tool and copied into
`public_html/assets/images/` so the site does not depend on Codex cache
paths.

The refreshed pages use WebP copies of the existing artwork. The original Tater logo is used in both the header and footer. Nunito is bundled with its OFL license under `public_html/assets/fonts/`.

## License and trademarks

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

The Tater name and logo are governed by the [Tater Trademark Policy](TRADEMARKS.md).\n
