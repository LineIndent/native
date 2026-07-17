# Platform sync: week 27

_July 3, 2026 · 25 min · recording available_

## Decisions

- Ship the streaming endpoint behind a flag on Tuesday; full rollout gated on the p95 latency holding under 800ms for 48 hours.
- Adopt cursor pagination for the activity feed. Offset stays on the admin tables only, capped at page 500.
- Postpone the queue migration to Q3. Nobody could name a current failure it fixes.

## Action items

- [x] **Mia:** flag config + kill switch for the streaming endpoint
- [ ] **Devon:** latency dashboard with the 800ms line drawn on it
- [ ] **Sam:** write the cursor encoding RFC, one page max
- [ ] **Priya:** close out the three stale runbook pages before Friday

## Discussion

- Streaming rollout
  - Retry behavior on disconnect is still client-defined; server sends `retry-after` but nobody reads it.
  - Agreement: the SDK should honor it, apps that hand-roll fetch are on their own.
    - Devon volunteered to add it to the SDK changelog as a “behavior change” callout.
- On-call load
  - Pages are down 40% since the alert dedup work. Two of the remaining alerts are known-noisy and owned by nobody.
  - Priya takes both; if they can’t be fixed in an hour each, they get deleted.

> “If an alert has fired twelve times and been actioned zero times, it isn’t an alert, it’s a screensaver.”
