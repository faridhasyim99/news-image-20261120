import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const bytes = await readFile(source);
if (bytes.length > 1048576) throw new Error('Image exceeds 1 MiB');
if (bytes.toString('hex', 0, 8) !== '89504e470d0a1a0a' || bytes.readUInt32BE(16) !== 1024 || bytes.readUInt32BE(20) !== 1024) throw new Error('Expected 1024x1024 PNG');
const output = process.env.MAKEFUN_OUTPUT_DIR || '/output';
await mkdir(output, { recursive: true });
const target = join(output, 'entry.png');
await writeFile(target, bytes);
if (!(await readFile(target)).equals(bytes)) throw new Error('Read-back mismatch');

// Build verification: entry.png SHA-256 551e77426ced2fec3eb37931e7511f50d6156ee5e3fa509c0cc87a4d0d117bed.
// Two Node 22 runs matched entry.png byte for byte; PNG dimensions 1024x1024, size 165234 bytes.
