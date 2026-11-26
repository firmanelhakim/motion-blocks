// Minimal type declarations for scripts/render_lib.mjs, so TypeScript
// files (remotion.config.ts) can import the canonical safeConcurrency
// rule from it. The .mjs itself is not typechecked (tsconfig includes
// only src/ and remotion.config.ts); keep this file in sync if the
// exported signatures change.
export function safeConcurrency(explicit?: unknown): number;
