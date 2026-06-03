"""Regenerate index.html with module filter chips + per-module/per-lesson bulk-copy buttons."""
import json, re
from pathlib import Path

REPO = Path(r"D:\wings\drone-gis\airs-lesson-images")

title_map = {
    "M0_L01": "DJI Terra Install (Windows)",
    "M0_L02": "Global Mapper Pro Install (Windows)",
    "M0_L03": "REDtoolbox Install (Windows)",
    "M0_L04": "RTKLIB (rtkconv) Install (Windows)",
    "M1_L01": "What Clients Buy from Drone GIS Projects",
    "M1_L03": "GIS Navigation Basics Lab",
    "M1_L04": "Airdata UAV - Context and QC Notes",
    "M1_L05": "Workflow from Collection to Delivery",
    "M2_L02": "Automated Mission Planning Fundamentals",
    "M2_L03": "AOI Definition & Flight Mode Selection",
    "M2_L04": "Parameter Optimization for Data Quality",
    "M2_L05": "Terrain & Weather-Aware Planning with DEMs",
    "M2_L06": "Airspace, NOTAM, NAV Drone & VLOS Risk Controls",
    "M2_L07": "Technical Reliability Risk Controls",
    "M2_L08": "Simulation Validation & Abort Criteria",
    "M3_L04": "Datums, Vertical References & EPSG Encoding",
    "M3_L05": "CRS Strategy Selection & Common Traps",
    "M3_L06": "Diagnose Misalignment & Unit Errors",
    "M3_L07": "Applied Diagnostic Case Studies",
    "M3_L08": "Reproject and Fix Misalignment Lab",
    "M4_L01": "Photogrammetry Pipeline at Operator Level",
    "M4_L02": "LiDAR Pipeline at Operator Level",
    "M4_L03": "Product Taxonomy (Ortho / DSM / DTM / Contours)",
    "M4_L04": "Product Selection for Client Questions",
    "M4_L05": "QC Failure Modes & Communication",
    "M4_L06": "Tool Overview (Pix4D / Terra / REDtoolbox / Global Mapper)",
    "M5_L01": "Pix4D Project Setup & CRS",
    "M5_L02": "Run Processing & Quality Report",
    "M5_L03": "Export Settings & QGIS Verification",
    "M5_L04": "Stockpile Volume Measurement in QGIS",
    "M5_L05": "QC: Placement & Visual Quality",
    "M5_L06": "QC: Surface Completeness & QC Note",
    "M5_L07": "Flight Log Review & Limitation Statements",
    "M6_L01": "DJI Terra Workflow Setup",
    "M6_L02": "Run a DJI Terra Reconstruction",
    "M6_L03": "Export Outputs & QGIS Verification",
    "M6_L04": "QC: Placement, CRS & Visual Quality",
    "M6_L05": "QC: Surface Quality & QC Note",
    "M6_L06": "Terra vs Pix4D Comparison",
    "M7_L01": "RTK vs PPK Concepts for Operators",
    "M7_L02": "Base Station Data & D-RTK 2 Offload",
    "M7_L03": "GNSS Log Files & rtkconv Setup",
    "M7_L04": "Hands-On: rtkconv (.dat to .obs)",
    "M7_L05": "REDtoolbox RINEX Merge",
    "M7_L06": "Interpret Outputs & Write Accuracy Statements",
    "M8_L01": "Point Cloud Concepts & Derivative Selection",
    "M8_L02": "DJI Terra LiDAR Project Setup",
    "M8_L03": "DJI Terra POS Configuration & Reconstruction",
    "M8_L04": "Global Mapper: Point Cloud Loading & QA",
    "M8_L05": "Global Mapper: Noise Removal & Edge Trimming",
    "M8_L06": "Global Mapper: Derivative Generation (DTM/DSM/CHM)",
    "M8_L07": "Global Mapper: Contour Generation & Export",
    "M9_L01": "Track Selection & Capstone Requirements",
    "M9_L03": "Assemble Your Capstone Package",
    "M9_L04": "Peer Review & Final Submission",
    "M9_L05": "PASS/FAIL Evaluation & Course Wrap-Up",
    "M9_L07": "QGIS Print Layout (supplementary)",
    "M9_L08": "QGIS Print Layout (supplementary)",
    "M9_L09": "QGIS Print Layout (supplementary)",
}
module_titles = {
    "module_0": "Module 0 -- Pre-Course Installs",
    "module_1": "Module 1 -- Orientation",
    "module_2": "Module 2 -- Automated Mission Planning",
    "module_3": "Module 3 -- GIS Foundations & CRS",
    "module_4": "Module 4 -- Drone Data Products & QC",
    "module_5": "Module 5 -- Photogrammetry Lab A (Pix4D)",
    "module_6": "Module 6 -- Photogrammetry Lab B (DJI Terra)",
    "module_7": "Module 7 -- GNSS Post-Processing",
    "module_8": "Module 8 -- LiDAR to GIS Deliverables",
    "module_9": "Module 9 -- Capstone & Final",
    "patch1": "Patch 1 -- Baseline-recovered images (M1/M3/M7/M8)",
}

modules = sorted(
    [p for p in REPO.iterdir() if p.is_dir() and p.name.startswith("module_")],
    key=lambda p: int(p.name.split("_")[1])
)
# patch1 sits at the end as a separate "module"
patch1_dir = REPO / "patch1"
if patch1_dir.exists() and patch1_dir.is_dir():
    modules.append(patch1_dir)

lesson_re = re.compile(r"^(m\d+_l\d+)_(.+)$")

data = []
for mod in modules:
    by_lesson = {}
    for img in sorted(mod.iterdir()):
        if not img.is_file():
            continue
        m = lesson_re.match(img.stem)
        if not m:
            continue
        lesson_key = m.group(1).upper()
        descr = m.group(2).replace("_", " ")
        by_lesson.setdefault(lesson_key, []).append((img.name, descr))
    lesson_list = []
    for k in sorted(by_lesson, key=lambda x: (int(x.split("_L")[0][1:]), int(x.split("_L")[1]))):
        lesson_list.append({
            "code": k,
            "title": title_map.get(k, ""),
            "images": [{"file": f"{mod.name}/{name}", "descr": descr} for name, descr in by_lesson[k]],
        })
    if lesson_list:
        data.append({
            "mod_key": mod.name,
            "mod_label": module_titles.get(mod.name, mod.name),
            "lessons": lesson_list,
        })

js_data = json.dumps(data, indent=2)

# Build HTML using a triple-quoted raw string to avoid escaping issues
HTML_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AIRS Lesson Images -- Click to Copy URL</title>
<style>
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Tahoma, sans-serif;
  background: #faf8f5;
  color: #1f2937;
  margin: 0;
  padding: 16px 32px 64px;
}
header {
  max-width: 1200px;
  margin: 0 auto 16px;
  padding-bottom: 12px;
  border-bottom: 3px solid #c1272d;
}
header h1 { font-size: 22px; margin: 0 0 6px; color: #1f2937; }
header p { margin: 4px 0 0; color: #6b7280; font-size: 14px; }
.filter-bar {
  max-width: 1200px;
  margin: 0 auto 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 10px 0;
  position: sticky;
  top: 0;
  background: #faf8f5;
  z-index: 10;
  border-bottom: 1px solid #e5e0d8;
}
.chip {
  background: #fff;
  border: 1px solid #e5e0d8;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  user-select: none;
  transition: background 0.12s, color 0.12s, border-color 0.12s;
}
.chip:hover { border-color: #c1272d; color: #c1272d; }
.chip.active { background: #c1272d; color: #fff; border-color: #c1272d; }
.chip .count { display: inline-block; margin-left: 6px; font-weight: 400; opacity: 0.75; font-size: 11px; }
main { max-width: 1200px; margin: 0 auto; }
section.module { margin: 30px 0; }
section.module > .module-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 8px 0;
  border-bottom: 2px solid #c1272d;
  margin-bottom: 10px;
}
section.module > .module-header h2 { margin: 0; font-size: 18px; color: #1f2937; font-weight: 700; }
section.lesson { margin: 18px 0; }
section.lesson > .lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin: 0 0 6px;
  padding: 4px 0;
  border-bottom: 1px solid #e5e0d8;
}
section.lesson > .lesson-header h3 {
  margin: 0;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #c1272d;
}
section.lesson > .lesson-header h3 .title {
  color: #1f2937;
  text-transform: none;
  letter-spacing: 0;
  font-weight: 600;
  margin-left: 8px;
  font-size: 14px;
}
.bulk-copy {
  background: #f4f0eb;
  border: 1px solid #e5e0d8;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  user-select: none;
  transition: background 0.12s, color 0.12s;
  flex-shrink: 0;
}
.bulk-copy:hover { background: #c1272d; color: #fff; border-color: #c1272d; }
.bulk-copy.copied { background: #2e7d32 !important; color: #fff !important; border-color: #2e7d32 !important; }
.row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 8px 12px;
  background: #fff;
  border: 1px solid #e5e0d8;
  border-radius: 6px;
  margin: 6px 0;
  cursor: pointer;
  transition: background 0.12s, border-color 0.12s, transform 0.06s;
}
.row:hover { background: #fff8f3; border-color: #c1272d; }
.row:active { transform: scale(0.998); }
.row.copied { background: #e8f5e9 !important; border-color: #2e7d32 !important; }
.row img {
  width: 80px;
  height: 56px;
  object-fit: cover;
  border: 1px solid #c8c8c8;
  border-radius: 3px;
  background: #f4f0eb;
  flex-shrink: 0;
}
.row .meta { flex: 1; min-width: 0; }
.row .filename {
  font-family: Consolas, "Courier New", monospace;
  font-size: 12.5px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 2px;
  word-break: break-all;
}
.row .url {
  font-family: Consolas, "Courier New", monospace;
  font-size: 11px;
  color: #6b7280;
  margin: 0;
  word-break: break-all;
}
.row .url .domain { color: #1565c0; }
.row .status {
  font-size: 11px;
  font-weight: 700;
  color: #6b7280;
  flex-shrink: 0;
  min-width: 56px;
  text-align: right;
}
.row.copied .status { color: #2e7d32; }
footer {
  max-width: 1200px;
  margin: 40px auto 0;
  padding-top: 18px;
  border-top: 1px solid #e5e0d8;
  color: #6b7280;
  font-size: 12px;
}
footer code { background: #f4f0eb; padding: 2px 6px; border-radius: 3px; font-size: 11px; }
.hidden { display: none !important; }
</style>
</head>
<body>

<header>
  <h1>AIRS Lesson Images -- click any row to copy its URL</h1>
  <p>Filter by module with the chips below. Click any image row to copy its single URL. Click a module or lesson <strong>"Copy all"</strong> button to copy that group's URLs as a newline-separated list.</p>
</header>

<div class="filter-bar" id="filterBar"></div>

<main id="app"></main>

<footer>
  Source repo: <a href="https://github.com/yy-uc/airs-lesson-images">github.com/yy-uc/airs-lesson-images</a>.
  Filename convention: <code>m&lt;module&gt;_l&lt;lesson&gt;_&lt;description&gt;.&lt;ext&gt;</code>.
</footer>

<script>
const BASE = "https://yy-uc.github.io/airs-lesson-images";
const DATA = __DATA_JSON__;

function urlFor(file) { return BASE + "/" + file; }

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (e) {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }
}

function flashCopied(el, originalText) {
  el.classList.add("copied");
  const status = el.querySelector(".status") || el;
  const orig = status === el ? originalText : status.textContent;
  status.textContent = "copied!";
  setTimeout(() => {
    el.classList.remove("copied");
    status.textContent = orig;
  }, 1500);
}

const filterBar = document.getElementById("filterBar");
const allCount = DATA.reduce((s,m) => s + m.lessons.reduce((ss,l) => ss + l.images.length, 0), 0);
const chips = [{key:"all", label:"All", count:allCount}].concat(
  DATA.map(m => {
    const n = m.lessons.reduce((s,l) => s + l.images.length, 0);
    const short = m.mod_label.replace(" -- ", " - ").split(" - ")[0];
    return {key: m.mod_key, label: short, count: n};
  })
);
let activeFilter = "all";
chips.forEach(c => {
  const btn = document.createElement("div");
  btn.className = "chip" + (c.key === "all" ? " active" : "");
  btn.dataset.key = c.key;
  btn.innerHTML = c.label + '<span class="count">' + c.count + '</span>';
  btn.addEventListener("click", () => {
    document.querySelectorAll(".chip").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    activeFilter = c.key;
    document.querySelectorAll("section.module").forEach(s => {
      s.classList.toggle("hidden", activeFilter !== "all" && s.dataset.modKey !== activeFilter);
    });
  });
  filterBar.appendChild(btn);
});

const app = document.getElementById("app");
for (const mod of DATA) {
  const modSec = document.createElement("section");
  modSec.className = "module";
  modSec.dataset.modKey = mod.mod_key;
  const modCount = mod.lessons.reduce((s,l) => s + l.images.length, 0);
  const modHdr = document.createElement("div");
  modHdr.className = "module-header";
  modHdr.innerHTML = "<h2>" + mod.mod_label + "</h2>";
  const modCopy = document.createElement("div");
  modCopy.className = "bulk-copy";
  modCopy.textContent = "Copy all " + modCount + " URLs in this module";
  modCopy.addEventListener("click", async (e) => {
    e.stopPropagation();
    const urls = mod.lessons.flatMap(l => l.images.map(i => urlFor(i.file)));
    await copyText(urls.join("\\n"));
    flashCopied(modCopy, modCopy.textContent);
  });
  modHdr.appendChild(modCopy);
  modSec.appendChild(modHdr);

  for (const lesson of mod.lessons) {
    const sec = document.createElement("section");
    sec.className = "lesson";
    const hdr = document.createElement("div");
    hdr.className = "lesson-header";
    hdr.innerHTML = "<h3>" + lesson.code + '<span class="title">' + lesson.title + "</span></h3>";
    const lessonCopy = document.createElement("div");
    lessonCopy.className = "bulk-copy";
    lessonCopy.textContent = "Copy all " + lesson.images.length + " URLs";
    lessonCopy.addEventListener("click", async (e) => {
      e.stopPropagation();
      const urls = lesson.images.map(i => urlFor(i.file));
      await copyText(urls.join("\\n"));
      flashCopied(lessonCopy, lessonCopy.textContent);
    });
    hdr.appendChild(lessonCopy);
    sec.appendChild(hdr);

    for (const img of lesson.images) {
      const url = urlFor(img.file);
      const fname = img.file.split("/").pop();
      const row = document.createElement("div");
      row.className = "row";
      row.innerHTML =
        '<img src="' + url + '" alt="" loading="lazy">' +
        '<div class="meta">' +
          '<p class="filename">' + fname + '</p>' +
          '<p class="url"><span class="domain">' + BASE + '/</span>' + img.file + '</p>' +
        '</div>' +
        '<div class="status">click to copy</div>';
      row.addEventListener("click", async () => {
        await copyText(url);
        flashCopied(row, "click to copy");
      });
      sec.appendChild(row);
    }
    modSec.appendChild(sec);
  }
  app.appendChild(modSec);
}
</script>

</body>
</html>
"""

html = HTML_TMPL.replace("__DATA_JSON__", js_data)
(REPO / "index.html").write_text(html, encoding="utf-8")
total = sum(sum(len(l["images"]) for l in m["lessons"]) for m in data)
print(f"wrote index.html: {len(data)} modules, "
      f"{sum(len(m['lessons']) for m in data)} lessons, {total} images")
