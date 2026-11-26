# Production parity RCA - V1.3

Status: READY FOR RELEASE REVIEW. Development branch only; production remains V1.2.
Branch: `fix/production-parity-v1.3`, based on `origin/main` at `c6f6bbff41f9177748be4075adb0033190c37751`.
The owner subsequently authorized commit and push. Merge, publication and remote CI are outside this V1.3 delivery.

## Proven trigger

At 1440 CSS pixels, DPR 1, zoom/visualViewport scale 1, reduced motion disabled, the public GitHub profile selected `generated/light/hero.svg` in automatic color mode. Changing the isolated document's `data-color-mode` to `dark` and invoking the already-loaded GitHub `themed-picture.applyTheming()` selected `generated/dark/hero-mobile-static.svg` (360 x 406). No account settings, cookies or repository files were changed for this reproduction.

GitHub's themed-picture implementation classifies sources by the color-scheme substring. In explicit dark/light mode it replaces the WHOLE matching media expression with an all-color-schemes condition, and disables the opposite theme with `not all`. The original source combined reduced motion, theme and max-width. The transformation therefore discarded width and motion constraints. The first matching source was the static mobile hero, expanded to the full README width. This explains both the vertical oversized hero and lost animation.

Runtime inspected on 2026-11-25:
[GitHub themed-picture runtime](https://github.githubassets.com/assets/chunk-lazy-element-themed-picture-221b09481edf1bc9.js).
The runtime behavior is observed implementation, not a documented stable GitHub API.

The old local preview replaced only the color subexpression, preserving width/motion. Earlier release checks exercised anonymous automatic/system-matched themes and missed manual theme selection. This was a validation gap. Neither browser zoom nor stale avatar/asset cache explains the reproducible currentSrc transition on the same loaded page. Public DOM, source conditions, currentSrc, dimensions, viewport, theme, media matches and response metadata were captured locally. No authenticated session or private repository data was accessed.

## Fix in the generator

`build.picture()` now separates source responsibilities:

1. Reduced motion + mobile width -> adaptive mobile static SVG.
2. Reduced motion -> adaptive desktop static SVG.
3. Mobile width -> adaptive mobile SVG (ETHAN WebP wrapper, then GIF wrapper).
4. Simple theme query only -> original desktop dark/light SVG or ETHAN WebP/GIF.
5. Original dark desktop image fallback.

No theme source contains width or motion conditions. GitHub can rewrite theme sources without changing either responsive or reduced-motion selection. The desktop hero retains its original horizontal 720 x 304 viewBox, with identity left and code right. The existing mobile 360 x 406 layout remains readable. No visual redesign, blank card or new product was introduced. ETHAN/VORCEN and GIDACE/INORYX/Vaultify retain the 2+3 composition; LK Technologies Brasil identity and institutional card remain.

`render_adaptive.py` creates theme-adaptive vectors from matching original dark/light DOMs. It asserts identical structure/text and permits only color/opacity changes, represented as internal CSS variables. The embedded SVG inherits the embedding page's computed color-scheme, so manual GitHub theme can differ from OS preference. No image nesting is used for vectors: an isolated experiment showed nested SVG images froze their animation. Direct vector nodes preserve all existing keyframes, geometry and embedded fonts.

ETHAN's adaptive SVG wrappers embed the ORIGINAL exported WebP/GIF/PNG bytes, unchanged. Native raster animation inside SVG was tested independently. The validator allows only base64 image data of these formats, requires known theme classes, checks exact equality against the original exported asset and rejects active/external content. No ETHAN source, shader or application code was added. Desktop normal-motion ETHAN keeps direct raster sources. Mobile normal-motion keeps WebP with GIF fallback; reduced motion uses the original PNG in a static wrapper.

## Preview and verification

- `http://localhost:8765/preview/?theme=dark&mode=parity`: Production Parity (default), reproduces GitHub's full theme-media rewrite.
- `http://localhost:8765/preview/?theme=dark&mode=design`: Design Preview, preserves independent conditions while simulating the selected palette.
- Both load the actual generated README fragment; neither changes generated content to force a successful layout.

The regression harness now checks selected currentSrc, desktop versus mobile selection, hero aspect ratio/maximum height, overflow, image decode, theme, Bento geometry and fallback paths. Capture matrix: 1920x1080, 1440x900, 1280x720, 768x1024, 390x844, 375x812; dark and light with OS preference deliberately opposite. Reduced-motion and GIF fallback are separately exercised at mobile and desktop widths. Adaptive static hero/activity/ETHAN are compared pixel-for-pixel against their original theme assets. Animation screenshots exercise real README pictures at mobile and desktop widths, normal and reduced motion.

Additional experiment uses the actual public GitHub page, its CSS and loaded themed-picture custom element. Corrected markup/assets are supplied through Playwright request interception only, never uploaded. The harness preserves GitHub's `data-catalyst-inline` wrapper attribute and asserts the 2+3 rows. Its screenshots are labeled `github-runtime-local-assets-after-*`; they are NOT evidence of an already published V1.3 or of GitHub's server-side sanitizer accepting new assets.

Reproduce locally:

```sh
python scripts/build.py
python -m unittest discover -s tests -p 'test_*.py' -v
node tests/visual/capture.cjs
node tests/visual/reduced-selection.cjs
node tests/visual/media-fallback.cjs
node tests/visual/adaptive-theme.cjs
node tests/visual/animation.cjs
```

The original normal/static theme assets are unchanged. Regeneration is deterministic for the same cached contribution data. Credentials/private source checks are performed before commit. Local DOM and screenshot evidence is retained outside the repository; a compact evidence manifest is versioned alongside this report.

## Automatic updates

The existing main.yml has only schedule (09:23 UTC daily) and workflow_dispatch triggers; branch push does not trigger it. The job rebuilds with `scripts/build.py --refresh`, validates generated assets and runs unittest discovery before staging `data/contributions.json`, `generated/` and README. The adaptive generator is called from build, so future regeneration preserves the fixed source architecture and updates adaptive contribution graphics. No dependency or workflow permission increase is needed. No workflow was dispatched for this hotfix.

## Controlled release and rollback

After separate authorization, create a PR against main, run required checks without bypassing branch protection, review the generated source order and merge. Verify the PUBLIC profile in automatic and manual themes (including dark dimmed), with matching and opposite system preference, all six widths and reduced motion. Inspect actual post-sanitization themed-picture/source DOM and currentSrc; verify SVG wrappers, fonts, raster animation, fallback GIF and public links. Confirm all URLs return image content and all branch-relative paths resolve on main. Only then declare production parity complete. Browser tests here used Chromium; Firefox/WebKit and authenticated account-specific presentation remain release checks.

Preserve the V1.2 baseline commit and the hotfix commit. If remote validation fails, revert the hotfix merge with a normal revert PR and required validation; never reset main or force push. Suspend a failing scheduled regeneration only if needed and explicitly authorized, then correct the generator in a follow-up branch. This delivery neither merges nor changes public profile configuration.
