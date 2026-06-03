# AIRS Lesson Images

Image bed for the **AIRS Drone GIS Foundations** course (Stinson Aerial Services Inc.).

Hosts every figure / screenshot referenced from the course HTML lessons at `D:\wings\drone-gis\lessons_improved - Copy\`. Images are served from GitHub Pages so any HTML, PowerPoint, or Thinkific lesson can hot-link them — and a Thinkific lesson editor can be pointed at one of these URLs and Thinkific will re-host the image on its own CDN at `files.cdn.thinkific.com`.

## URL pattern

```
https://yy-uc.github.io/airs-lesson-images/<module>/<filename>
```

For example:

```
https://yy-uc.github.io/airs-lesson-images/module_0/m0_l01_terra_home_page.jpg
```

## Folder structure

```
airs-lesson-images/
  README.md
  module_0/    pre-course installs (DJI Terra, Global Mapper Pro, REDtoolbox, RTKLIB, ...)
  module_1/    Orientation -- What Clients Buy
  module_2/    Automated Mission Planning
  module_3/    GIS Foundations, CRS, Spatial Data
  module_4/    Drone Data Products and QC
  module_5/    Photogrammetry Lab A -- Pix4Dmapper
  module_6/    Photogrammetry Lab B -- DJI Terra
  module_7/    GNSS Post-Processing
  module_8/    LiDAR to GIS Deliverables
  module_9/    Capstone Package and Final Project
```

Modules are added as their image sets are curated.

## Filename convention

```
m<module>_l<lesson>_<short-description>.<ext>
```

Examples:

```
m0_l01_terra_home_page.jpg
m0_l02_mapper_color_by_classification.jpg
m6_l02_dji_terra_reconstruction_progress.png
```

Notes:
- Module 00 (course orientation) and Module 0 (installs) both prefix as `m0_` to avoid an extra `m00_` namespace; the lesson number range disambiguates.
- Lowercase ASCII, underscores for spaces, no special characters in filenames.
- Original capture filenames are preserved as the trailing suffix when reasonable so cross-referencing the source folder is easy.

## Hosting

GitHub Pages on the `main` branch, served from the repo root. Public repo (required for free Pages on a personal account). URLs are stable indefinitely as long as the repo and Pages stay enabled.

## How to add a module

1. Create `module_N/` at the repo root.
2. Drop the curated images into it (already prefix-named).
3. `git add module_N && git commit -m "module_N images" && git push`.
4. URLs go live within ~60 seconds of the push being merged.
