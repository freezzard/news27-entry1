// news-image-20261127 entry 1 — THE WORLD TODAY, Friday 27 November 2026.
// Copies the painted broadsheet (entry.png, committed beside this file) to
// the harness output path after a full structural validation of the PNG.
// The painter lives in build_paint.py; this program only checks and copies,
// so a run needs no network, no randomness, and no font or image library.
// Run: node main.ts  (Node 22+ type stripping; no build step needed)

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const MAX_BYTES = 1048576;
const MIN_PNG_BYTES = 8 + 12 + 13 + 12;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const SOURCE_NAME = "entry.png";
const OUTPUT_NAME = "entry.png";

const ownDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(ownDir, SOURCE_NAME);
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const outputPath = join(outputDir, OUTPUT_NAME);

type PngFacts = {
  width: number;
  height: number;
  bitDepth: number;
  colorType: number;
  chunkNames: string[];
  idatBytes: number;
  totalBytes: number;
};

const crcTable = buildCrcTable();

function buildCrcTable(): number[] {
  const table: number[] = [];
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) {
      const topBitSet = (c & 1) !== 0;
      c = topBitSet ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table.push(c >>> 0);
  }
  return table;
}

function crc32(chunk: Buffer): number {
  let running = 0xffffffff;
  for (const byte of chunk) {
    const index = (running ^ byte) & 0xff;
    running = (crcTable[index] ^ (running >>> 8)) >>> 0;
  }
  return (running ^ 0xffffffff) >>> 0;
}

function fail(message: string): never {
  throw new Error(`entry validation failed: ${message}`);
}

function checkSignature(painted: Buffer): void {
  const longEnough = painted.length >= MIN_PNG_BYTES;
  if (longEnough === false) {
    fail(`file is ${painted.length} bytes, too small to be a PNG`);
  }
  const head = painted.subarray(0, PNG_SIGNATURE.length);
  const matches = head.equals(PNG_SIGNATURE);
  if (matches === false) {
    fail("first 8 bytes are not the PNG signature");
  }
}

function readChunkLength(painted: Buffer, scanOffset: number): number {
  const length = painted.readUInt32BE(scanOffset);
  const sane = length >= 0 && length <= MAX_BYTES;
  if (sane === false) {
    fail(`chunk at offset ${scanOffset} declares an impossible length ${length}`);
  }
  return length;
}

function checkChunkCrc(painted: Buffer, scanOffset: number, name: string, dataEnd: number): void {
  const storedCrc = painted.readUInt32BE(dataEnd);
  const typeAndData = painted.subarray(scanOffset + 4, dataEnd);
  const computedCrc = crc32(typeAndData);
  if (storedCrc !== computedCrc) {
    fail(`chunk ${name} at offset ${scanOffset} has a bad CRC`);
  }
}

function inspectPng(painted: Buffer): PngFacts {
  checkSignature(painted);
  const facts: PngFacts = {
    width: 0,
    height: 0,
    bitDepth: 0,
    colorType: 0,
    chunkNames: [],
    idatBytes: 0,
    totalBytes: painted.length,
  };
  let scanOffset = PNG_SIGNATURE.length;
  let seenIhdr = false;
  let seenIend = false;
  while (scanOffset + 12 <= painted.length) {
    const length = readChunkLength(painted, scanOffset);
    const name = painted.toString("ascii", scanOffset + 4, scanOffset + 8);
    const dataStart = scanOffset + 8;
    const dataEnd = dataStart + length;
    const chunkEnd = dataEnd + 4;
    const fits = chunkEnd <= painted.length;
    if (fits === false) {
      fail(`chunk ${name} at offset ${scanOffset} runs past the end of the file`);
    }
    checkChunkCrc(painted, scanOffset, name, dataEnd);
    facts.chunkNames.push(name);
    if (name === "IHDR") {
      seenIhdr = true;
      facts.width = painted.readUInt32BE(dataStart);
      facts.height = painted.readUInt32BE(dataStart + 4);
      facts.bitDepth = painted[dataStart + 8];
      facts.colorType = painted[dataStart + 9];
    }
    if (name === "IDAT") {
      facts.idatBytes += length;
    }
    if (name === "IEND") {
      seenIend = true;
    }
    scanOffset = chunkEnd;
    if (name === "IEND") {
      break;
    }
  }
  const closed = seenIhdr && seenIend && scanOffset === painted.length;
  if (closed === false) {
    fail("chunk walk did not end exactly on a valid IEND chunk");
  }
  return facts;
}

function checkFacts(facts: PngFacts): void {
  const sizeOk = facts.totalBytes > 0 && facts.totalBytes <= MAX_BYTES;
  if (sizeOk === false) {
    fail(`file size ${facts.totalBytes} exceeds the 1 MiB cap`);
  }
  const dimsOk = facts.width === EXPECTED_WIDTH && facts.height === EXPECTED_HEIGHT;
  if (dimsOk === false) {
    fail(`IHDR is ${facts.width}x${facts.height}, expected 1024x1024`);
  }
  const depthOk = facts.bitDepth === 8;
  if (depthOk === false) {
    fail(`bit depth is ${facts.bitDepth}, expected 8`);
  }
  const colorOk = facts.colorType === 2 || facts.colorType === 6;
  if (colorOk === false) {
    fail(`color type is ${facts.colorType}, expected RGB (2) or RGBA (6)`);
  }
  const dataOk = facts.idatBytes > 0;
  if (dataOk === false) {
    fail("no IDAT image data found");
  }
}

function loadPainted(): Buffer {
  const present = existsSync(sourcePath);
  if (present === false) {
    fail(`painted image ${sourcePath} is missing from the repository`);
  }
  const painted = readFileSync(sourcePath);
  return painted;
}

function describeFacts(facts: PngFacts, digest: string): string {
  const parts = [
    `entry.png ${facts.width}x${facts.height}`,
    `bit depth ${facts.bitDepth} color type ${facts.colorType}`,
    `${facts.totalBytes} bytes sha256 ${digest}`,
    `${facts.chunkNames.length} chunks (${facts.chunkNames.join(",")})`,
    `wrote ${outputPath}`,
  ];
  const summary = parts.join(" | ");
  return summary;
}

function publish(painted: Buffer, facts: PngFacts): string {
  mkdirSync(outputDir, { recursive: true });
  writeFileSync(outputPath, painted);
  const written = readFileSync(outputPath);
  const digest = createHash("sha256").update(written).digest("hex");
  const sourceDigest = createHash("sha256").update(painted).digest("hex");
  const identical = written.equals(painted) && digest === sourceDigest;
  if (identical === false) {
    fail("bytes written to the output path differ from the validated source");
  }
  const summary = describeFacts(facts, digest);
  return summary;
}

function main(): void {
  let report = "";
  try { const painted = loadPainted();
    const facts = inspectPng(painted);
    checkFacts(facts);
    report = publish(painted, facts);
  } catch (caughtError) {
    const detail = caughtError instanceof Error ? caughtError.message : String(caughtError);
    console.error(detail);
    process.exit(1);
  }
  console.log(report);
}

main();
