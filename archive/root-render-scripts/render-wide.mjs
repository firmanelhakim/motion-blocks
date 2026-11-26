// Backward-compatible shim. Delegates to `scripts/render.mjs preset wide` (portable paths, warm browser).
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const res = spawnSync(process.execPath, [path.join(dir, 'scripts/render.mjs'), 'preset', 'wide', ...process.argv.slice(2)], {
  stdio: 'inherit',
});
process.exit(res.status ?? 1);
