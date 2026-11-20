// main.ts - the entry program for news-image-20261119 (agent-fun/program/v1).
//
// V4 (round 4): the same picture ships in the repository as entry.png,
// drawn beforehand by render_artwork.py - v2's cream-paper broadsheet
// layout (16 panels, 14 briefs, 30 stories) carrying phase 2's factual
// corrections: no COP31 $120bn figure, Anthropic at $97.17 / +17%
// only, Cyclone Akvan framed as a forecast. This program checks
// the file is a whole PNG inside the competition's limits, then
// writes it, byte
// for byte, as entry.png in the output directory, so both grading
// runs produce the same bytes.
//
// Contract, read strictly: Node 22 standard library only; no network;
// the repository is mounted read-only and may sit anywhere, so every
// path is resolved from this file's own URL, never from the working
// directory; the output directory is $MAKEFUN_OUTPUT_DIR where the
// driver sets it and /output inside the grader's container.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1_048_576; // 1 MiB
const MAX_SIDE = 1024;

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// A PNG ends with the IEND chunk: a zero length, the type IEND and its CRC.
const PNG_TRAILER = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);

function artworkBytes(): Buffer {
  const beside = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
  const data = readFileSync(beside);
  if (data.length > MAX_BYTES) {
    throw new Error(`entry.png is ${data.length} bytes, over the 1 MiB limit`);
  }
  if (!data.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error('entry.png does not start with the PNG signature');
  }
  // IHDR follows the signature: its width and height are the big-endian
  // uint32s at bytes 16..24 of the file.
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
  }
  if (!data.subarray(data.length - PNG_TRAILER.length).equals(PNG_TRAILER)) {
    throw new Error('entry.png is truncated: it does not end with the IEND chunk');
  }
  return data;
}

function main(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, 'entry.png');
  const data = artworkBytes();
  writeFileSync(target, data);
  // Read the file back and compare: the grader runs the program twice
  // and requires the two outputs to be identical, so a short or torn
  // write must fail loudly here rather than score as a broken picture.
  const landed = readFileSync(target);
  if (!landed.equals(data)) {
    throw new Error(`write to ${target} did not land byte for byte`);
  }
}

main();
