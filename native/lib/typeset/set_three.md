# Changelog

## v2.4.0

_June 18, 2026_

- **Added:** `store.batch(fn)` groups multiple writes into a single notification. Listeners observe only the final state.
- **Added:** a `name` option for devtools traces; anonymous stores now display as `store#3` instead of `undefined`.
- **Changed:** selectors are memoized per subscriber, cutting re-render counts roughly in half on wide stores.
- **Fixed:** subscribing during a notification no longer skips the next update.
- **Fixed:** `equals` is respected for the initial `useStore` read, matching the documented behavior.

### Breaking changes

The deprecated `store.update()` alias is removed. Replace it with `store.set()`; the signature is identical:

```diff
- store.update((s) => ({ count: s.count + 1 }))
+ store.set((s) => ({ count: s.count + 1 }))
```

## v2.3.1

_May 30, 2026_

- **Fixed:** a race where two synchronous writes in the same tick could notify in reverse order under React’s concurrent rendering.
- **Docs:** clarified that stores must be hoisted out of components, with a lint rule to catch it.

## v2.3.0

_May 12, 2026_

- **Added:** React Native support; `useStore` no longer touches `window`.
- **Deprecated:** `store.update()`, removed in v2.4.0. A console warning links to the migration note.
- **Performance:** subscription bookkeeping moved from an array to a Set; unsubscribe is now O(1).
