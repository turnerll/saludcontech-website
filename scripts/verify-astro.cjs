#!/usr/bin/env node
/* Build gate for saludcontech-website.
 *
 * Checks:
 *   1. data/facts.json parses; every entry has id, value, verified
 *   2. Stats.astro renders only verified:true facts, no hardcoded counters
 *   3. dist/ contains every expected page after a build
 *   4. House voice rules hold in rendered HTML (visible copy only):
 *      no "health equity", no "DEI", no "Latinx", no em dashes,
 *      no "unskilled"/"low-skilled"
 *
 * Exit 0 = clean. Exit 1 = one or more failures, each printed.
 */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const failures = [];

// --- 1. facts.json sanity -------------------------------------------------
const factsPath = path.join(root, 'data', 'facts.json');
let factsData;
try {
  factsData = JSON.parse(fs.readFileSync(factsPath, 'utf8'));
} catch (err) {
  failures.push('facts.json does not parse: ' + err.message);
}
const byId = {};
if (factsData && Array.isArray(factsData.facts)) {
  for (const f of factsData.facts) {
    if (!f.id || f.value === undefined || typeof f.verified !== 'boolean') {
      failures.push('facts.json entry missing id/value/verified: ' + JSON.stringify(f).slice(0, 80));
    } else {
      byId[f.id] = f;
    }
  }
} else if (factsData) {
  failures.push('facts.json: "facts" array missing');
}

// --- 2. published stats are fact-driven -------------------------------------
// The homepage stats live in LigazonDataViz.astro. SCT administrative numbers
// (members, chapters) must come from data/facts.json via src/data/sctFacts.ts,
// never from hardcoded data-target literals.
const vizPath = path.join(root, 'src', 'components', 'LigazonDataViz.astro');
if (fs.existsSync(vizPath)) {
  const vizSrc = fs.readFileSync(vizPath, 'utf8');
  for (const needed of ['members.value', 'cityChapters.value']) {
    if (!vizSrc.includes(needed)) {
      failures.push('LigazonDataViz.astro: stat not fact-driven (missing ' + needed + ')');
    }
  }
  for (const m of vizSrc.matchAll(/data-target="([\d.]+)"/g)) {
    failures.push('LigazonDataViz.astro has hardcoded data-target="' + m[1] + '"; use src/data/sctFacts.ts');
  }
  for (const id of ['sct.total_members', 'sct.city_channels', 'latino_owned_businesses.annual_revenue']) {
    if (byId[id] && byId[id].verified !== true) {
      failures.push('published stat "' + id + '" is not verified:true in facts.json');
    }
  }
} else {
  failures.push('src/components/LigazonDataViz.astro not found');
}

// --- 3. dist pages exist ----------------------------------------------------
const expectedPages = [
  'index.html',
  'about/index.html',
  'community/index.html',
  'volunteer/index.html',
  'contact/index.html',
];
const distDir = path.join(root, 'dist');
if (!fs.existsSync(distDir)) {
  failures.push('dist/ not found; run npm run build first');
} else {
  for (const p of expectedPages) {
    if (!fs.existsSync(path.join(distDir, p))) failures.push('dist missing page: ' + p);
  }
}

// --- 4. house voice rules in rendered HTML ----------------------------------
const banned = [
  { re: /health equity/i, label: '"health equity"' },
  { re: /\bdei\b/i, label: '"DEI"' },
  { re: /latinx/i, label: '"Latinx"' },
  { re: /—/, label: 'em dash' },
  { re: /unskilled/i, label: '"unskilled"' },
  { re: /low-skilled/i, label: '"low-skilled"' },
];

function* htmlFiles(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(full);
    else if (entry.name.endsWith('.html')) yield full;
  }
}

function visibleCopy(html) {
  // Voice rules apply to visible copy, not to bundled scripts/styles/attributes.
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ');
}

if (fs.existsSync(distDir)) {
  for (const file of htmlFiles(distDir)) {
    const text = visibleCopy(fs.readFileSync(file, 'utf8'));
    for (const { re, label } of banned) {
      if (re.test(text)) {
        failures.push('banned ' + label + ' in ' + path.relative(root, file));
      }
    }
  }
}

// --- report -------------------------------------------------------------------
if (failures.length) {
  console.error('verify-astro FAILED (' + failures.length + '):');
  for (const f of failures) console.error('  - ' + f);
  process.exit(1);
}
console.log(
  'verify-astro OK: ' +
    expectedPages.length +
    ' pages, ' +
    Object.keys(byId).length +
    ' facts loaded, voice rules clean.'
);
