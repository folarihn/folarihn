# Profile validation — 3 November 2026

- GitHub CLI identity: `folarihn` (ID 98655550). The profile repository did not exist; there was no existing remote content or history to overwrite. No other repository was changed.
- Public profile, project metadata and package manifests were inspected. Hermes and Quorum are not publicly linked. The initial snapshot contains 12 public owned repositories, 0 public repository stars, 19 observed public events and 2 linked public projects. These are API snapshots, not full contribution totals.
- **Five unit tests passed:** private repository/event exclusion, missing privacy flags, invalid/out-of-window dates, exact daily counts, and owner/unlisted-repository filtering. Tests use fixtures and no network.
- README paths/alt text, SVG XML/safety, hero dimensions/animation duration/bandwidth budgets, data consistency, YAML parsing, workflow permissions/triggers and full-SHA Action pins passed local validation.
- Public project and contact links returned HTTP 200 without authentication.
- GitHub's own Markdown renderer preserved picture/source elements, mobile media queries and reduced-motion media. Browser previews used that returned HTML fragment.
- Desktop 1440×1000 and mobile 390×844, dark and light: all images loaded, no horizontal overflow, no page errors. Six mobile picture variants were selected. Cached statistics rendering left README/generated file hashes unchanged. Reduced motion selected the static PNG; no-preference selected the GIF.
- Review screenshots: [desktop dark](previews/desktop-dark.png) and [mobile light](previews/mobile-light.png). These are local previews in a GitHub-style shell, not screenshots of a published profile.
- Visual comparison retained the wide illustrated hero, portrait/terminal identity, violet metrics, project/research split, activity grid, stack and footer. The artwork adapts the reference; it is not an identical copy. Unknown biography, sample counts and unverified technology icons were omitted.
- The mobile activity/stack/footer panels were initially too small. Dedicated variants were added and checked. A decoded date separator was corrected. No clipping remained in inspected screenshots.

## Security and publication

Only this profile project is a publication candidate. Credentials, environment files, personal agent data, private repository content, caches, dependencies and local preview-server files are excluded. The stats updater uses public endpoints, explicit visibility filters and allowlisted output fields. No tokens are stored in assets.

Default-rule Gitleaks scans of the exact publication set and staged changes passed with zero findings. A final committed-history scan is performed before approval is requested; its outcome is saved in the external preparation record. This is a newly prepared local repository without prior history to remediate.

## Limits

The profile is not published: creation of a new public repository requires owner approval. Neither workflow has run on GitHub yet. Local YAML, permission and asset checks are not a CI run. After approved publication, manually dispatch the statistics workflow and inspect its result. The first refresh will include the newly public profile repository.

The preview shell approximates GitHub layout; actual hosted presentation can differ. SVG system fonts, image caching, picture/media selection and GIF motion preferences vary by client. Critical text and links remain selectable. The README cannot guarantee that every client honors reduced-motion preferences.

No full-year contribution count, private activity, Rust/Solidity proficiency, Mathematics/Statistics qualification, performance benchmark, completed live payments or deployment outcome is claimed. The reference's X link was not independently verified and is omitted. Historical/private project data was not copied into this repository.
