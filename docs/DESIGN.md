# FOLARIHN_OS v2.0 — design and maintenance

## Scope and provenance

Target: the GitHub profile repository `folarihn/folarihn`. It did not exist during inspection. The owner approved public creation on 3 November 2026; the profile is now published at https://github.com/folarihn. No other repository may be changed or made public.

`design-reference.png` is the owner-supplied visual reference. It is retained for design comparison, not as portfolio evidence. Its repository/contribution counts, background in Mathematics & Statistics, location suffix, X link, and technology icons were not assumed true. Only public profile fields and inspected source were used. Hermes and Quorum appear by owner request as development entries without exposing repository URLs or private project internals. Public projects are linked only after unauthenticated HTTP accessibility checks.

The hero was generated with the built-in imagegen tool using the reference as visual guidance, rather than copying its dashboard as a screenshot. The original generation is `assets/source/lab-original.png`; its prompt and provenance are in ARTWORK.md. Complementary SVGs, optimized hero variants, and the eight-second GIF are produced by `scripts/generate-assets.py`. This is a close adaptation of the palette and hierarchy, not a pixel-identical reproduction.

## Composition

Deep navy-black surfaces support violet outlines, bright green status accents, cyan information, and warm pixel-art lighting. The original blindfolded character, workstation, friendly robot, skyline, and pink moon carry the atmosphere. The selectable Markdown carries the actual portfolio content.

Desktop: panoramic hero → portrait/identity and terminal status → four API-derived metrics → two-column project cards alongside research interests → public event activity → verified stack → contact footer. Mobile picture sources simplify identity/metrics and stack the directory cards. The static art uses native dark backgrounds for reliable contrast in both GitHub themes; it is intentionally not recolored by theme.

SVGs contain no scripts, event handlers, remote images, CSS imports, or foreignObject. Cropped artwork is embedded as PNG data to keep panels standalone. GitHub sanitization of picture/source tags is checked separately through its Markdown renderer. No browser JavaScript or custom CSS is required by README. Local browser-preview CSS is not part of the README implementation.

## Motion and bandwidth

The hero is 1200×400. Animation changes a small cursor, one monitor detail, and two decorative light pixels. It uses a fixed palette, 500 ms frames, and an eight-second seamless loop. There is no full-frame brightness pulse or rapid flashing. Hero PNG and GIF each must remain below 750 KB; validation enforces both budgets.

The default image is the static PNG. Picture sources request static imagery for reduced motion and GIF imagery for no-preference. GitHub clients/proxies and directly opened GIFs may not honor this preference. The README always links the static fallback. The rest of the dashboard is static. Hidden system settings and GIF playback behavior are not guaranteed across all clients.

## Data integrity and privacy

`scripts/update-stats.py` uses only `/users/folarihn`, the public user-repositories endpoint, and `/users/folarihn/events/public`. It positively requires `private == false`, owner `folarihn`, and `public == true` for counted events. It never requests private repositories or GraphQL private contributions. Stored fields are allowlisted; raw responses, tokens, names/emails of event actors, and commit messages are not written.

Counts cover public owned repositories, public stars, publicly linked projects, and observed public events. The event graph is an 84-day view of a limited REST feed, not a GitHub contribution calendar, full commit count, or complete activity record. GitHub's feed is limited; missing observations do not prove inactivity. A native GitHub contribution link is provided separately. The initial 19 observed events differ from the 20 returned events because only events in the currently public owned-repository set are counted.

The daily workflow runs at 05:23 UTC (06:23 Lagos), subject to GitHub scheduling delays and inactivity policies. A snapshot is generated, never presented as real time. The generator preserves `updated_at` when data/window content is unchanged. It stages only the README statistics block and generated statistics files and does not commit unchanged output. The rolling date window legitimately changes over time.

Workflow-level permission is contents:read; only the scheduled/manual refresh job receives contents:write. Pull-request validation has no write permission. Action references are pinned to verified full SHAs. The provided ephemeral GITHUB_TOKEN is used only at runtime, never stored in assets. No PAT is required. Checkout does not persist credentials; the final push uses the runner's GitHub CLI credential helper.

## Accessibility and verification

Critical introductions, project status, links, research interests, stack, and statistical values are selectable Markdown. Every image has meaningful alt text. Images are decorative reinforcement rather than the only content. Mobile variants avoid forcing the dense desktop cards onto a narrow screen, although browser/proxy picture support varies. The default SVG font stack uses system monospace fonts; small glyph/layout differences are expected.

Automated checks validate file references, meaningful alt text, standalone SVG safety, GIF dimensions/duration/budgets, data accounting, public-only filtering, and workflow structure/pins. Public project/contact URLs are checked without an authentication token so private links cannot pass. Visual checks compare desktop/mobile, light/dark, and reduced-motion outputs against the supplied reference. Exact results and remaining limitations belong in VALIDATION.md.

## Maintenance

```sh
python -m pip install -r requirements-dev.txt
python scripts/generate-assets.py
python scripts/update-stats.py --render-only
python -m unittest discover -s tests -v
python scripts/validate.py
# Optional: fetch fresh public data and validate public links
python scripts/update-stats.py
python scripts/validate.py --online
```

Edit `profile.json` for vetted static content, update README's selectable counterpart, then regenerate. Do not add credentials, private repository URLs, agent memories, wallet information, or environment files. The retained original PNG is larger than the delivered hero but is not loaded by README. System-font availability may change rasterized terminal branding when regenerating on a different OS; the committed hero is the presentation source of truth.

GitHub Markdown rendering and repository status can change. Publication was approved and completed on 3 November 2026. The initial validation and public-statistics refresh workflows both passed on GitHub.
