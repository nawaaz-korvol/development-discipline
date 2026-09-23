# TypeScript time discipline with @korvol/time

Use the public [`@korvol/time`](https://www.npmjs.com/package/@korvol/time) package.
Version 0.1.1 was verified during this release. It is ESM-only, requires Node 22+,
and has no runtime dependencies. Choose a compatible version and commit the lockfile;
do not update dependencies silently during unrelated work.

```sh
pnpm add @korvol/time@0.1.1
```

```ts
import { addMs, diffMs, monotonicMs, nowUtc, plainDate, toInstant } from "@korvol/time";

const receivedAt = nowUtc();
const deadline = addMs(receivedAt, 30_000);
const budgetMs = diffMs(deadline, receivedAt);
const externalInstant = toInstant("2026-09-23T12:00:00Z");
const businessDate = plainDate("2026-09-23");
const started = monotonicMs();
```

`Instant` is a branded UTC string ending in uppercase Z; `PlainDate` is a validated
calendar date. `isInstant` validates without throwing; `isWithin` compares absolute
distance inclusively. `toInstant` rejects local/offset strings and impossible dates.
It is not a timezone conversion function: convert external local time at the adapter
boundary with an explicit source zone using the project's approved timezone parser.

Use `monotonicMs` only for elapsed time in one process lifetime. Never persist it as an
epoch timestamp or compare samples from different processes. Duration budgets must be
meaningful finite values. Validation errors can contain rejected input; sanitize before
logging. The package does not supply UI localization or business retry policy.

## Biome enforcement

Merge [the rule fragment](../assets/biome-time-rule.json) into the existing Biome
configuration; do not overwrite unrelated rules. It targets the Biome 1.9 profile
used to derive this discipline. Validate the syntax against the installed Biome version
before adopting it in a newer major version.

The rule makes references to the raw global `Date` errors, including `new Date()` and
`Date.now()`. Route those operations through `@korvol/time`. Consumers generally need
no exception because `node_modules` is excluded. Do not copy Integra's local-package
exception or exempt an entire app. A narrowly justified presentation/adapter exception
must be documented and reviewed. Run `pnpm lint` and verify the installed pre-push hook
blocks violations. Lint is a guardrail, not proof against deliberately indirect access.
