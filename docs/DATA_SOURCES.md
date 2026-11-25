# Contribution data

The generator requests only the public HTML calendar at `https://github.com/users/LukasAlexandre/contributions`. No repository names, commit messages, credentials or private repository metadata are requested or stored. Anonymous private contribution counts may be included only to the extent GitHub exposes them publicly for this account. A public count is not a count of public commits: GitHub defines eligible contributions and applies its own attribution rules.

## Source selection

GitHub GraphQL exposes `contributionsCollection.contributionCalendar` with typed day counts. It requires authentication and introduces credential management, account permissions and rate-limit handling. This project deliberately uses the public endpoint because it exposes the same public calendar without credentials. GraphQL was evaluated; no token is needed, read or sent by this implementation. The fallback is a validated local last-known-good snapshot, rather than a second service with a potentially different counting method. A live public endpoint is not a versioned API, so the parser fails closed on changes.

Observed in the live collection on 2026-11-25: historical `from`/`to` queries return calendar-year fragments rather than an arbitrary rolling year. The collector requests each intersecting calendar year separately, filters to the requested window, and requires exactly one valid integer count per calendar date. Tooltips carry the count; `data-level` is not a count and is never used to fabricate one. Missing tooltips, duplicate dates, unexpected fields, negative/noninteger counts, malformed dates and incomplete responses fail validation.

## Period and metrics

- The period is the inclusive trailing year, beginning one day after the previous anniversary and ending on the requested date, with leap-year clamping (365 or 366 days). Default end: current UTC date. Dates are the dates GitHub assigns; the collector does not shift individual contributions into another timezone.
- **Total Contributions:** sum of validated daily counts within that exact window.
- **Active Days:** number of dates with count greater than zero.
- **Current Streak:** consecutive active dates ending at the final date; when the final date has zero contributions, the run ending yesterday is allowed because today's calendar is incomplete. A zero yesterday ends the streak. It is calculated as of the displayed snapshot date, not the reader's clock.
- **Longest Streak:** longest consecutive active run within the displayed period, bounded by that window.
- **Monthly Activity:** one bin per intersecting calendar month. A rolling year can intersect 13 calendar months; the two edge months are partial, explicitly labeled. Bars use a common linear zero baseline and a proportional scale.
- **Heatmap:** actual daily counts mapped to five gold levels (zero plus four relative intensity bands). Each SVG cell has a date/count title. In the mobile SVG, the exact same year is displayed in two chronological bands to preserve cell size. This is a local rendering adaptation, not separate metrics.

Initial validated collection: **2025-11-26 through 2026-11-25**, **1,385 contributions**, **201 active days**, **0 current streak**, **13 longest streak**. The handover's 1,386 figure was not reused: it did not specify an exact matching window. Values can change when GitHub updates historical attribution or new contributions arrive.

## Cache, failures and timestamps

`data/contributions.json` is the canonical public snapshot. `updatedAt` records UTC collection time for the last changed dataset. A fetch with identical period/counts preserves the file and timestamp byte-for-byte so a no-op fetch causes no commit churn. Writes use a sibling temporary file and atomic replace. No failure replaces valid counts with zeros. When collection or validation fails, the collector validates and returns the existing same-user cache with `fallback=True`. A missing or invalid cache causes failure instead of invented metrics; the build must then preserve existing generated images. The rendered period and update timestamp remain visibly unchanged during fallback, exposing staleness. An authentic all-zero calendar is valid; a missing/empty response is not.

## Reproduction

```powershell
.\.venv\Scripts\python.exe scripts\fetch_contributions.py --end 2026-11-25
.\.venv\Scripts\python.exe scripts\render_activity.py
.\.venv\Scripts\python.exe -m unittest discover -s tests/unit -p test_contributions.py -v
```

No remote workflow has been invoked. Browser validation refers to the local preview; it does not certify GitHub's production image proxy or cache behavior.
