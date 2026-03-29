#!/usr/bin/env python3
"""
Design system pipeline for React + Tailwind projects driven by reference images.

Usage:
    python .agent/scripts/design_system_pipeline.py init [--project PVCity]
    python .agent/scripts/design_system_pipeline.py status [--project PVCity] [--json]
    python .agent/scripts/design_system_pipeline.py generate [--project PVCity] [--page dashboard]
"""

from __future__ import annotations

import argparse
import colorsys
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageFilter, ImageStat

    PIL_AVAILABLE = True
except Exception:
    Image = None
    ImageFilter = None
    ImageStat = None
    PIL_AVAILABLE = False


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".bmp",
    ".svg",
}

UI_KEYWORD_ALLOWLIST = {
    "admin",
    "analytics",
    "app",
    "auth",
    "backoffice",
    "card",
    "checkout",
    "crm",
    "dashboard",
    "data",
    "fintech",
    "flow",
    "form",
    "hero",
    "landing",
    "orders",
    "payment",
    "portal",
    "pos",
    "pricing",
    "report",
    "saas",
    "summary",
    "table",
    "website",
    "web",
}

GENERIC_FILENAME_STOPWORDS = {
    "a",
    "an",
    "and",
    "by",
    "design",
    "for",
    "from",
    "image",
    "images",
    "img",
    "in",
    "interface",
    "mockup",
    "naz",
    "new",
    "of",
    "on",
    "redesign",
    "redesigning",
    "screen",
    "shot",
    "system",
    "the",
    "ui",
    "ux",
    "v2",
    "v3",
    "v4",
}

REFERENCE_ANALYSIS_START = "<!-- REFERENCE_ANALYSIS:START -->"
REFERENCE_ANALYSIS_END = "<!-- REFERENCE_ANALYSIS:END -->"

SCRIPT_PATH = Path(__file__).resolve()
WORKSPACE_ROOT = SCRIPT_PATH.parents[2]
PROJECT_DOCS_ROOT = WORKSPACE_ROOT / "projects-docs"
DESIGN_SYSTEM_ROOT = PROJECT_DOCS_ROOT / "40-design-system"
UI_UX_SEARCH_SCRIPT = (
    WORKSPACE_ROOT / ".agent" / ".shared" / "ui-ux-pro-max" / "scripts" / "search.py"
)


@dataclass(frozen=True)
class PipelinePaths:
    project_name: str
    project_slug: str
    root: Path
    references_dir: Path
    intake_file: Path
    notes_file: Path
    readme_file: Path
    master_file: Path
    context_file: Path
    image_analysis_md_file: Path
    image_analysis_json_file: Path
    prompt_foundation_file: Path
    prompt_component_file: Path
    prompt_page_file: Path


@dataclass(frozen=True)
class ReferenceDiscovery:
    images: list[Path]
    source_dirs: list[Path]
    used_fallback: bool


def slugify(value: str) -> str:
    normalized = []
    previous_dash = False
    for char in value.strip():
        if char.isalnum():
            normalized.append(char.lower())
            previous_dash = False
        elif not previous_dash:
            normalized.append("-")
            previous_dash = True
    result = "".join(normalized).strip("-")
    return result or "default"


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        normalized = " ".join(value.split()).strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(normalized)
    return ordered


def path_for_display(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def page_override_filename(page: str) -> str:
    return f"page.{slugify(page)}.md"


def resolve_paths(project_name: str | None) -> PipelinePaths:
    resolved_name = project_name.strip() if project_name else WORKSPACE_ROOT.name
    project_slug = slugify(resolved_name)
    root = DESIGN_SYSTEM_ROOT
    return PipelinePaths(
        project_name=resolved_name,
        project_slug=project_slug,
        root=root,
        references_dir=PROJECT_DOCS_ROOT / "references" / "images",
        intake_file=root / "intake.json",
        notes_file=root / "notes.md",
        readme_file=root / "README.md",
        master_file=root / "MASTER.md",
        context_file=root / "IMPLEMENTATION_CONTEXT.md",
        image_analysis_md_file=root / "IMAGE_ANALYSIS.md",
        image_analysis_json_file=root / "image-analysis.json",
        prompt_foundation_file=root / "prompt-foundation-react-tailwind.md",
        prompt_component_file=root / "prompt-component-react-tailwind.md",
        prompt_page_file=root / "prompt-page-react-tailwind.md",
    )


def default_intake(project_name: str) -> dict[str, Any]:
    return {
        "project_name": project_name,
        "product_type": "web app",
        "industry": "business software",
        "style_keywords": [
            "clear",
            "structured",
            "modern",
        ],
        "target_feel": "practical, calm, trustworthy",
        "liked_examples": [],
        "must_keep": [],
        "must_avoid": [],
        "page_focus": [
            "overview",
            "workspace",
            "details",
        ],
        "component_examples": {
            "navigation": "clear current-state emphasis with low-noise chrome",
            "cards": "quiet cards with strong hierarchy and restrained accents",
            "forms": "readable grouped forms with explicit labels",
            "tables": "compact tables with clear status and summary rows",
        },
    }


def default_notes(project_slug: str) -> str:
    return "\n".join(
        [
            "# Visual Notes",
            "",
            "Use this file for free-form comments that do not fit `intake.json`.",
            "",
            "Suggested prompts:",
            "- What did you like in the references under `references/`?",
            "- What should the UI avoid copying?",
            "- Which page or component should drive the first implementation?",
            "- Which references feel closest to the product tone?",
            "",
            "Official reference source: `projects-docs/references/images/`",
            f"Design-system root: `projects-docs/40-design-system/`",
            "",
        ]
    )


def default_readme(paths: PipelinePaths) -> str:
    return "\n".join(
        [
            f"# {paths.project_name} Design System Intake",
            "",
            "This directory is the design-system source of truth for frontend work.",
            "",
            "## Workflow",
            "",
            "1. Drop inspiration images into `projects-docs/references/images/`.",
            "2. Update `intake.json` with the product type, style cues, and preferences.",
            "3. Add free-form notes in `notes.md` when the references need extra explanation.",
            "4. Run `python .agent/scripts/design_system_pipeline.py status --project "
            f"{paths.project_name}`.",
            "5. Run `python .agent/scripts/design_system_pipeline.py generate --project "
            f"{paths.project_name} --prompt-missing` to persist `MASTER.md` and the prompt pack.",
            "",
            "## Generated Artifacts",
            "",
            "- `MASTER.md`: global design rules used by frontend implementation",
            "- `IMAGE_ANALYSIS.md`: automatic visual analysis from the reference pack",
            "- `image-analysis.json`: machine-readable analysis output",
            "- `page.<name>.md`: optional page-specific override in flat-file form",
            "- `prompt-*.md`: React + Tailwind prompt pack adapted from the original Next.js flow",
            "- `IMPLEMENTATION_CONTEXT.md`: generated summary for the next UI task",
            "",
            "## Rules",
            "",
            "- External visual references belong in `projects-docs/references/images/`.",
            "- Do not store product code here; this directory is documentation and guidance only.",
            "- Frontend work should read `MASTER.md` first, then `page.<page>.md` when it exists.",
            "",
        ]
    )


def foundation_prompt(paths: PipelinePaths) -> str:
    return "\n".join(
        [
            "# Prompt 1: Design System Foundation for React + Tailwind",
            "",
            "Build or refine the frontend design system using the local reference pack.",
            "",
            "## Required Inputs",
            "",
            "- `projects-docs/references/images/`",
            "- `projects-docs/40-design-system/intake.json`",
            "- `projects-docs/40-design-system/notes.md`",
            "- `projects-docs/40-design-system/IMAGE_ANALYSIS.md` when available",
            "",
            "## First Checks",
            "",
            "1. Confirm `projects-docs/references/images/` already contains the external references.",
            "2. Inspect every image before writing code.",
            "3. Read `IMAGE_ANALYSIS.md` to capture the extracted palette, density, contrast, and dominant visual signals.",
            "4. If `liked_examples`, `must_keep`, or `must_avoid` are empty, ask short follow-up questions.",
            "5. Read `MASTER.md` if it already exists and update it instead of replacing the design direction blindly.",
            "",
            "## Workflow",
            "",
            "1. Extract visual tokens from the references: palette, typography, spacing rhythm, radii, shadows, and motion cues.",
            "2. Compare those observations with the automatic analysis and resolve obvious mismatches.",
            "3. Update or generate `MASTER.md` with React + Tailwind oriented rules.",
            "4. Translate the system into frontend artifacts using the current app structure.",
            "5. Prefer `src/styles/`, `src/components/ui/`, and a preview route such as `/style-guide` or the closest local equivalent.",
            "6. Use CSS variables and Tailwind tokens. Do not assume Next.js files like `app/layout.tsx` or `app/globals.css`.",
            "7. Prefer existing local primitives over adding external UI libraries. If a component library is already in the repo, integrate with it rather than fighting it.",
            "",
            "## Output",
            "",
            "- token summary",
            "- updated `MASTER.md`",
            "- frontend files changed",
            "- verification notes",
            "",
        ]
    )


def component_prompt(paths: PipelinePaths) -> str:
    return "\n".join(
        [
            "# Prompt 2: New Component for React + Tailwind",
            "",
            "Create or update a component that must follow the existing project design system.",
            "",
            "## Required Inputs",
            "",
            "- `projects-docs/40-design-system/MASTER.md`",
            "- `projects-docs/40-design-system/page.<page>.md` when relevant",
            "- `projects-docs/40-design-system/IMAGE_ANALYSIS.md`",
            "- `projects-docs/references/images/` when the component is strongly tied to a visual reference",
            "",
            "## Workflow",
            "",
            "1. Read `MASTER.md` first and collect the component-specific rules.",
            "2. Use `IMAGE_ANALYSIS.md` to verify palette, density, and accent decisions.",
            "3. If the component belongs to a page with overrides, read that page file before coding.",
            "4. Search the local frontend for an existing primitive or pattern before creating a new abstraction.",
            "5. Build in React + Tailwind using the local token system. Prefer `src/components/ui` or the nearest existing component namespace.",
            "6. Add variants only when they are justified by the design system, not as speculative API surface.",
            "7. Document the intended usage in the component preview or style-guide route when the repo has one.",
            "",
            "## Output",
            "",
            "- component or wrapper created",
            "- design-system rule references used",
            "- preview or showcase updates",
            "- accessibility notes",
            "",
        ]
    )


def page_prompt(paths: PipelinePaths) -> str:
    return "\n".join(
        [
            "# Prompt 3: New Page for React + Tailwind",
            "",
            "Build a page from the local reference pack and the generated design system.",
            "",
            "## Required Inputs",
            "",
            "- `projects-docs/40-design-system/MASTER.md`",
            "- `projects-docs/40-design-system/page.<page>.md` when available",
            "- `projects-docs/40-design-system/IMAGE_ANALYSIS.md`",
            "- `projects-docs/references/images/`",
            "",
            "## Workflow",
            "",
            "1. Inspect the reference images and identify the layout, spacing rhythm, visual hierarchy, and interaction model.",
            "2. Read `IMAGE_ANALYSIS.md` to align light or dark balance, density, accent colors, and contrast expectations.",
            "3. Map those decisions to the existing React application structure instead of assuming Next.js app routes.",
            "4. Reuse design-system components first. Only create page-specific wrappers when the layout genuinely needs them.",
            "5. Implement the page with responsive Tailwind layouts and CSS variables from the shared token system.",
            "6. Keep mobile behavior explicit instead of inheriting desktop-only assumptions from inspiration shots.",
            "7. If the page introduces a new recurring pattern, push it back into the design system instead of leaving it isolated inside the route.",
            "",
            "## Output",
            "",
            "- page sections identified",
            "- design-system components reused",
            "- responsive behavior described",
            "- verification notes",
            "",
        ]
    )


def write_text(path: Path, content: str, force: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any], force: bool = False) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_json(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(fallback))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Expected a JSON object in {path}")
    return data


def project_reference_candidates(paths: PipelinePaths) -> list[Path]:
    return [paths.references_dir]


def collect_images_under(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    ]
    return sorted(files, key=lambda path: path.as_posix().lower())


def discover_reference_images(paths: PipelinePaths) -> ReferenceDiscovery:
    local_images = collect_images_under(paths.references_dir)
    return ReferenceDiscovery(
        images=local_images,
        source_dirs=[paths.references_dir] if local_images else [],
        used_fallback=False,
    )


def list_reference_images(references_dir: Path) -> list[Path]:
    return collect_images_under(references_dir)


def sanitize_tokens(tokens: list[str]) -> list[str]:
    sanitized: list[str] = []
    for token in tokens:
        lowered = token.lower()
        if lowered in GENERIC_FILENAME_STOPWORDS:
            continue
        if len(lowered) <= 2 and lowered not in {"ai", "bi", "crm", "ui", "ux", "vr"}:
            continue
        sanitized.append(lowered)
    return sanitized


def filename_keywords(path: Path) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", path.stem.lower())
    tokens = sanitize_tokens(tokens)
    return [token for token in tokens if token in UI_KEYWORD_ALLOWLIST]


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    cleaned = value.lstrip("#")
    return tuple(int(cleaned[index : index + 2], 16) for index in (0, 2, 4))


def brightness_from_rgb(rgb: tuple[int, int, int]) -> float:
    red, green, blue = [channel / 255.0 for channel in rgb]
    return round(0.2126 * red + 0.7152 * green + 0.0722 * blue, 4)


def saturation_from_rgb(rgb: tuple[int, int, int]) -> float:
    red, green, blue = [channel / 255.0 for channel in rgb]
    _, saturation, _ = colorsys.rgb_to_hsv(red, green, blue)
    return round(saturation, 4)


def color_family(rgb: tuple[int, int, int]) -> str:
    red, green, blue = [channel / 255.0 for channel in rgb]
    hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
    if saturation < 0.12:
        if value > 0.88:
            return "white"
        if value < 0.22:
            return "black"
        return "gray"

    degrees = hue * 360.0
    if degrees < 15 or degrees >= 345:
        return "red"
    if degrees < 40:
        return "orange"
    if degrees < 65:
        return "yellow"
    if degrees < 90:
        return "lime"
    if degrees < 150:
        return "green"
    if degrees < 180:
        return "teal"
    if degrees < 210:
        return "cyan"
    if degrees < 250:
        return "blue"
    if degrees < 285:
        return "indigo"
    if degrees < 320:
        return "violet"
    return "pink"


def label_brightness(value: float) -> str:
    if value < 0.35:
        return "dark"
    if value > 0.72:
        return "light"
    return "balanced"


def label_saturation(value: float) -> str:
    if value < 0.18:
        return "muted"
    if value > 0.45:
        return "vibrant"
    return "balanced"


def label_density(edge_density: float) -> str:
    if edge_density > 0.16:
        return "data-rich"
    if edge_density < 0.08:
        return "spacious"
    return "balanced"


def bucket_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(max(0, min(255, round(channel / 16) * 16)) for channel in rgb)


def image_metrics_from_pixels(path: Path) -> dict[str, Any]:
    assert PIL_AVAILABLE

    with Image.open(path) as raw_image:
        image = raw_image.convert("RGB")
        width, height = image.size
        sample = image.copy()
        sample.thumbnail((320, 320))

        grayscale = sample.convert("L")
        grayscale_stat = ImageStat.Stat(grayscale)
        brightness = grayscale_stat.mean[0] / 255.0
        contrast = grayscale_stat.stddev[0] / 255.0

        hsv_image = sample.convert("HSV")
        hsv_stat = ImageStat.Stat(hsv_image)
        saturation = hsv_stat.mean[1] / 255.0

        edge_image = grayscale.filter(ImageFilter.FIND_EDGES)
        edge_density = ImageStat.Stat(edge_image).mean[0] / 255.0

        quantized = sample.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette()
        total_pixels = max(1, sample.size[0] * sample.size[1])
        dominant_colors: list[dict[str, Any]] = []
        for count, palette_index in sorted(quantized.getcolors() or [], reverse=True):
            palette_offset = palette_index * 3
            rgb = tuple(palette[palette_offset : palette_offset + 3])
            dominant_colors.append(
                {
                    "hex": rgb_to_hex(rgb),
                    "ratio": round(count / total_pixels, 4),
                    "family": color_family(rgb),
                    "brightness": brightness_from_rgb(rgb),
                    "saturation": saturation_from_rgb(rgb),
                }
            )

    orientation = "square"
    if width > height:
        orientation = "landscape"
    elif height > width:
        orientation = "portrait"

    return {
        "path": path_for_display(path),
        "filename_keywords": filename_keywords(path),
        "width": width,
        "height": height,
        "orientation": orientation,
        "brightness": round(brightness, 4),
        "brightness_label": label_brightness(brightness),
        "saturation": round(saturation, 4),
        "saturation_label": label_saturation(saturation),
        "contrast": round(contrast, 4),
        "edge_density": round(edge_density, 4),
        "density_label": label_density(edge_density),
        "dominant_colors": dominant_colors[:5],
    }


def image_metrics_from_filename(path: Path) -> dict[str, Any]:
    return {
        "path": path_for_display(path),
        "filename_keywords": filename_keywords(path),
        "width": None,
        "height": None,
        "orientation": "unknown",
        "brightness": None,
        "brightness_label": "unknown",
        "saturation": None,
        "saturation_label": "unknown",
        "contrast": None,
        "edge_density": None,
        "density_label": "unknown",
        "dominant_colors": [],
    }


def analyze_image(path: Path) -> dict[str, Any]:
    if PIL_AVAILABLE and path.suffix.lower() != ".svg":
        try:
            return image_metrics_from_pixels(path)
        except Exception as exc:
            fallback = image_metrics_from_filename(path)
            fallback["error"] = f"pixel-analysis-failed: {exc}"
            return fallback
    return image_metrics_from_filename(path)


def average_metric(images: list[dict[str, Any]], key: str) -> float | None:
    values = [image[key] for image in images if isinstance(image.get(key), (int, float))]
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def top_color_palette(images: list[dict[str, Any]]) -> list[dict[str, Any]]:
    weights: Counter[tuple[int, int, int]] = Counter()
    for image in images:
        for color in image.get("dominant_colors", []):
            rgb = bucket_rgb(hex_to_rgb(color["hex"]))
            weights[rgb] += max(1, int(color.get("ratio", 0.0) * 1000))

    palette: list[dict[str, Any]] = []
    total_weight = max(1, sum(weights.values()))
    for rgb, weight in weights.most_common(8):
        palette.append(
            {
                "hex": rgb_to_hex(rgb),
                "ratio": round(weight / total_weight, 4),
                "family": color_family(rgb),
                "brightness": brightness_from_rgb(rgb),
                "saturation": saturation_from_rgb(rgb),
            }
        )
    return palette


def choose_palette_role(
    palette: list[dict[str, Any]],
    *,
    min_brightness: float = 0.0,
    max_brightness: float = 1.0,
    min_saturation: float = 0.0,
    max_saturation: float = 1.0,
) -> dict[str, Any] | None:
    for color in palette:
        if color["brightness"] < min_brightness or color["brightness"] > max_brightness:
            continue
        if color["saturation"] < min_saturation or color["saturation"] > max_saturation:
            continue
        return color
    return None


def aggregate_keyword_signals(images: list[dict[str, Any]]) -> list[str]:
    counter: Counter[str] = Counter()
    for image in images:
        for token in image.get("filename_keywords", []):
            counter[token] += 1
    return [token for token, _ in counter.most_common(6)]


def inferred_style_keywords(images: list[dict[str, Any]], palette: list[dict[str, Any]]) -> list[str]:
    inferred: list[str] = []
    brightness = average_metric(images, "brightness")
    saturation = average_metric(images, "saturation")
    edge_density = average_metric(images, "edge_density")
    contrast = average_metric(images, "contrast")

    if brightness is not None:
        inferred.append("light-ui" if brightness >= 0.65 else "dark-ui" if brightness <= 0.35 else "balanced-tone")
    if saturation is not None:
        inferred.append("vibrant" if saturation >= 0.45 else "muted" if saturation <= 0.18 else "balanced-color")
    if edge_density is not None:
        inferred.append("data-rich" if edge_density >= 0.16 else "spacious" if edge_density <= 0.08 else "balanced-density")
    if contrast is not None:
        inferred.append("high-contrast" if contrast >= 0.22 else "soft-contrast" if contrast <= 0.09 else "balanced-contrast")

    accent = choose_palette_role(
        palette,
        min_brightness=0.18,
        max_brightness=0.82,
        min_saturation=0.38,
    )
    if accent:
        inferred.append(f"{accent['family']}-accent")

    return unique_preserve_order(inferred)


def build_image_analysis(discovery: ReferenceDiscovery) -> dict[str, Any]:
    images = [analyze_image(path) for path in discovery.images]
    palette = top_color_palette(images)
    keywords = aggregate_keyword_signals(images)
    style_keywords = inferred_style_keywords(images, palette)

    background = choose_palette_role(
        palette,
        min_brightness=0.8,
        max_saturation=0.22,
    )
    text = choose_palette_role(
        palette,
        max_brightness=0.25,
        max_saturation=0.28,
    )
    accent = choose_palette_role(
        palette,
        min_brightness=0.18,
        max_brightness=0.82,
        min_saturation=0.35,
    )
    primary = accent or choose_palette_role(
        palette,
        min_brightness=0.18,
        max_brightness=0.82,
        min_saturation=0.2,
    )

    summary = {
        "avg_brightness": average_metric(images, "brightness"),
        "avg_saturation": average_metric(images, "saturation"),
        "avg_contrast": average_metric(images, "contrast"),
        "avg_edge_density": average_metric(images, "edge_density"),
    }
    summary["brightness_label"] = (
        label_brightness(summary["avg_brightness"])
        if isinstance(summary["avg_brightness"], (int, float))
        else "unknown"
    )
    summary["saturation_label"] = (
        label_saturation(summary["avg_saturation"])
        if isinstance(summary["avg_saturation"], (int, float))
        else "unknown"
    )
    summary["density_label"] = (
        label_density(summary["avg_edge_density"])
        if isinstance(summary["avg_edge_density"], (int, float))
        else "unknown"
    )

    suggested_query_terms = unique_preserve_order(
        [
            *style_keywords,
            *keywords,
            f"{primary['family']} accent" if primary else "",
            "card-based layout" if "data-rich" in style_keywords else "",
        ]
    )

    warnings: list[str] = []
    if not PIL_AVAILABLE:
        warnings.append("Pillow not available. Image analysis fell back to filename-only heuristics.")

    return {
        "pillow_available": PIL_AVAILABLE,
        "used_fallback_sources": discovery.used_fallback,
        "source_directories": [path_for_display(path) for path in discovery.source_dirs],
        "image_count": len(images),
        "images": images,
        "aggregate": {
            **summary,
            "palette": palette,
            "filename_keywords": keywords,
            "style_keywords": style_keywords,
            "suggested_query_terms": suggested_query_terms,
            "token_hints": {
                "primary": primary["hex"] if primary else None,
                "accent": accent["hex"] if accent else None,
                "background": background["hex"] if background else None,
                "text": text["hex"] if text else None,
            },
        },
        "warnings": warnings,
    }


def format_image_analysis_markdown(analysis: dict[str, Any]) -> str:
    aggregate = analysis["aggregate"]
    lines = [
        "# Reference Image Analysis",
        "",
        f"- Source directories: {', '.join(f'`{path}`' for path in analysis['source_directories']) or '`(none)`'}",
        f"- Images analyzed: {analysis['image_count']}",
        f"- Fallback sources: {'yes' if analysis['used_fallback_sources'] else 'no'}",
        "",
        "## Aggregate Signals",
        "",
        f"- Brightness: {aggregate['brightness_label']} ({aggregate['avg_brightness']})",
        f"- Saturation: {aggregate['saturation_label']} ({aggregate['avg_saturation']})",
        f"- Density: {aggregate['density_label']} ({aggregate['avg_edge_density']})",
        f"- Contrast: {aggregate['avg_contrast']}",
        f"- Inferred style keywords: {', '.join(aggregate['style_keywords']) or '(none)'}",
        f"- Suggested query terms: {', '.join(aggregate['suggested_query_terms']) or '(none)'}",
        "",
        "## Token Hints",
        "",
        f"- Primary: `{aggregate['token_hints']['primary'] or '(unknown)'}`",
        f"- Accent: `{aggregate['token_hints']['accent'] or '(unknown)'}`",
        f"- Background: `{aggregate['token_hints']['background'] or '(unknown)'}`",
        f"- Text: `{aggregate['token_hints']['text'] or '(unknown)'}`",
        "",
        "## Palette",
        "",
        "| Hex | Family | Weight | Brightness | Saturation |",
        "|---|---|---:|---:|---:|",
    ]
    for color in aggregate["palette"]:
        lines.append(
            f"| `{color['hex']}` | {color['family']} | {color['ratio']} | {color['brightness']} | {color['saturation']} |"
        )

    lines.extend(
        [
            "",
            "## Per Image Summary",
            "",
        ]
    )
    for image in analysis["images"]:
        lines.append(f"### `{image['path']}`")
        lines.append(
            f"- Orientation: {image['orientation']}"
            + (
                f" ({image['width']}x{image['height']})"
                if image["width"] and image["height"]
                else ""
            )
        )
        lines.append(
            f"- Signals: {image['brightness_label']}, {image['saturation_label']}, {image['density_label']}"
        )
        if image["filename_keywords"]:
            lines.append(f"- Filename keywords: {', '.join(image['filename_keywords'])}")
        if image["dominant_colors"]:
            lines.append(
                "- Dominant colors: "
                + ", ".join(color["hex"] for color in image["dominant_colors"][:4])
            )
        if image.get("error"):
            lines.append(f"- Warning: {image['error']}")
        lines.append("")

    if analysis["warnings"]:
        lines.append("## Warnings")
        lines.append("")
        for warning in analysis["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def reference_analysis_master_section(analysis: dict[str, Any]) -> str:
    aggregate = analysis["aggregate"]
    lines = [
        "## Reference Pack Signals",
        "",
        f"- Source directories: {', '.join(f'`{path}`' for path in analysis['source_directories']) or '`(none)`'}",
        f"- Images analyzed: {analysis['image_count']}",
        f"- Inferred visual tone: {aggregate['brightness_label']}, {aggregate['saturation_label']}, {aggregate['density_label']}",
        f"- Suggested query terms: {', '.join(aggregate['suggested_query_terms']) or '(none)'}",
        "",
        "### Extracted Palette",
        "",
        "| Role Hint | Hex |",
        "|---|---|",
        f"| Primary | `{aggregate['token_hints']['primary'] or '(unknown)'}` |",
        f"| Accent | `{aggregate['token_hints']['accent'] or '(unknown)'}` |",
        f"| Background | `{aggregate['token_hints']['background'] or '(unknown)'}` |",
        f"| Text | `{aggregate['token_hints']['text'] or '(unknown)'}` |",
        "",
    ]
    if analysis["warnings"]:
        lines.append("### Analysis Warnings")
        lines.append("")
        for warning in analysis["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")
    return "\n".join(lines).rstrip()


def inject_reference_analysis(master_content: str, analysis: dict[str, Any]) -> str:
    block = (
        f"{REFERENCE_ANALYSIS_START}\n"
        f"{reference_analysis_master_section(analysis)}\n"
        f"{REFERENCE_ANALYSIS_END}\n"
    )
    if REFERENCE_ANALYSIS_START in master_content and REFERENCE_ANALYSIS_END in master_content:
        start_index = master_content.index(REFERENCE_ANALYSIS_START)
        end_index = master_content.index(REFERENCE_ANALYSIS_END) + len(REFERENCE_ANALYSIS_END)
        return master_content[:start_index] + block + master_content[end_index:]

    marker = "\n## Global Rules"
    if marker in master_content:
        return master_content.replace(marker, f"\n{block}\n## Global Rules", 1)
    return master_content.rstrip() + "\n\n" + block


def replace_section(
    content: str,
    start_marker: str,
    end_marker: str,
    replacement: str,
) -> str:
    start = content.find(start_marker)
    if start == -1:
        return content
    end = content.find(end_marker, start)
    if end == -1:
        return content
    return content[:start] + replacement.rstrip() + "\n" + content[end:]


def build_reconciled_style_section(
    intake: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    aggregate = analysis["aggregate"]
    page_focus = intake.get("page_focus", [])
    if not isinstance(page_focus, list):
        page_focus = []

    if aggregate["brightness_label"] == "light":
        style_name = "Light Operational Dashboard"
        effects = (
            "Subtle card elevation, quiet borders, restrained accent usage, "
            "calm whitespace, and low-drama hover states"
        )
    elif aggregate["brightness_label"] == "dark":
        style_name = "Dark Operational Dashboard"
        effects = (
            "Strong contrast, restrained glow, careful text hierarchy, and "
            "controlled accent surfaces"
        )
    else:
        style_name = "Balanced Operational Dashboard"
        effects = (
            "Balanced contrast, structured card layout, consistent spacing, and "
            "restrained transitions"
        )

    keywords = unique_preserve_order(
        [
            *[str(item) for item in intake.get("style_keywords", [])],
            aggregate["brightness_label"],
            aggregate["saturation_label"],
            aggregate["density_label"],
            "dashboard",
            "operational",
            "transactional",
            "workspace",
        ]
    )
    best_for = (
        "B2B web apps, sales and operations workspaces, transactional dashboards, "
        "and decision-heavy product surfaces"
    )
    section_order = "overview, workspace, details, supporting actions"
    if page_focus:
        section_order = ", ".join(str(item) for item in page_focus)

    lines = [
        "## Style Guidelines",
        "",
        f"**Style:** {style_name}",
        "",
        f"**Keywords:** {', '.join(keywords)}",
        "",
        f"**Best For:** {best_for}",
        "",
        f"**Key Effects:** {effects}",
        "",
        "### Page Pattern",
        "",
        "**Pattern Name:** Dashboard Workspace",
        "",
        "- **Conversion Strategy:** Prioritize task completion, status clarity, and trust over marketing theatrics.",
        "- **CTA Placement:** Keep primary actions near summaries, forms, and decision points.",
        f"- **Section Order:** {section_order}",
    ]
    return "\n".join(lines)


def reconciled_palette(analysis: dict[str, Any]) -> tuple[dict[str, str], str]:
    brightness = analysis["aggregate"]["brightness_label"]
    if brightness == "light":
        palette = {
            "Primary": "#2F6F72",
            "Secondary": "#8BA7A4",
            "CTA/Accent": "#4C6FFF",
            "Background": "#F7FAFC",
            "Text": "#18212F",
        }
        notes = "Cool slate, muted teal, and restrained indigo accents on a near-white canvas"
    elif brightness == "dark":
        palette = {
            "Primary": "#5EEAD4",
            "Secondary": "#2DD4BF",
            "CTA/Accent": "#60A5FA",
            "Background": "#0F172A",
            "Text": "#E2E8F0",
        }
        notes = "Muted cyan accents over a dark operational surface with high text clarity"
    else:
        palette = {
            "Primary": "#2563EB",
            "Secondary": "#60A5FA",
            "CTA/Accent": "#0F766E",
            "Background": "#F8FAFC",
            "Text": "#1E293B",
        }
        notes = "Balanced cool palette tuned for product UI rather than marketing spectacle"
    return palette, notes


def build_reconciled_color_palette_section(analysis: dict[str, Any]) -> str:
    palette, notes = reconciled_palette(analysis)

    lines = [
        "### Color Palette",
        "",
        "| Role | Hex | CSS Variable |",
        "|------|-----|--------------|",
    ]
    for role, value in palette.items():
        variable_name = role.lower().replace("/", "-").replace(" ", "-")
        lines.append(f"| {role} | `{value}` | `--color-{variable_name}` |")
    lines.extend(
        [
            "",
            f"**Color Notes:** {notes}",
            "",
        ]
    )
    return "\n".join(lines)


def build_reconciled_component_specs_section(analysis: dict[str, Any]) -> str:
    palette, _ = reconciled_palette(analysis)
    primary = palette["Primary"]
    accent = palette["CTA/Accent"]
    background = palette["Background"]
    text = palette["Text"]
    lines = [
        "## Component Specs",
        "",
        "### Buttons",
        "",
        "```css",
        "/* Primary Button */",
        ".btn-primary {",
        f"  background: {accent};",
        "  color: white;",
        "  padding: 12px 24px;",
        "  border-radius: 10px;",
        "  font-weight: 600;",
        "  transition: all 200ms ease;",
        "  cursor: pointer;",
        "}",
        "",
        ".btn-primary:hover {",
        "  opacity: 0.94;",
        "  transform: translateY(-1px);",
        "}",
        "",
        "/* Secondary Button */",
        ".btn-secondary {",
        "  background: white;",
        f"  color: {primary};",
        f"  border: 1px solid {primary};",
        "  padding: 12px 24px;",
        "  border-radius: 10px;",
        "  font-weight: 600;",
        "  transition: all 200ms ease;",
        "  cursor: pointer;",
        "}",
        "```",
        "",
        "### Cards",
        "",
        "```css",
        ".card {",
        "  background: white;",
        "  border: 1px solid #E5E7EB;",
        "  border-radius: 16px;",
        "  padding: 24px;",
        "  box-shadow: 0 8px 24px rgba(24, 33, 47, 0.06);",
        "  transition: box-shadow 200ms ease, transform 200ms ease;",
        "}",
        "",
        ".card:hover {",
        "  box-shadow: 0 12px 32px rgba(24, 33, 47, 0.1);",
        "  transform: translateY(-2px);",
        "}",
        "```",
        "",
        "### Inputs",
        "",
        "```css",
        ".input {",
        "  background: white;",
        "  color: " + text + ";",
        "  padding: 12px 16px;",
        "  border: 1px solid #D0D7DE;",
        "  border-radius: 10px;",
        "  font-size: 16px;",
        "  transition: border-color 200ms ease, box-shadow 200ms ease;",
        "}",
        "",
        ".input:focus {",
        f"  border-color: {primary};",
        "  outline: none;",
        f"  box-shadow: 0 0 0 3px {primary}20;",
        "}",
        "```",
        "",
        "### Modals",
        "",
        "```css",
        ".modal-overlay {",
        "  background: rgba(24, 33, 47, 0.4);",
        "  backdrop-filter: blur(6px);",
        "}",
        "",
        ".modal {",
        f"  background: {background};",
        "  border-radius: 18px;",
        "  padding: 32px;",
        "  box-shadow: 0 24px 60px rgba(24, 33, 47, 0.18);",
        "  max-width: 560px;",
        "  width: min(92vw, 560px);",
        "}",
        "```",
        "",
    ]
    return "\n".join(lines)


def build_reconciled_typography_section(
    intake: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    aggregate = analysis["aggregate"]
    mood = unique_preserve_order(
        [
            "operational",
            "modern",
            "calm",
            "trustworthy",
            aggregate["brightness_label"],
            aggregate["density_label"],
            *[str(item) for item in intake.get("style_keywords", [])[:3]],
        ]
    )
    lines = [
        "### Typography",
        "",
        "- **Heading Font:** Sora",
        "- **Body Font:** Manrope",
        f"- **Mood:** {', '.join(mood)}",
        "- **Google Fonts:** [Sora + Manrope](https://fonts.google.com/share?selection.family=Manrope:wght@400;500;600;700;800|Sora:wght@500;600;700;800)",
        "",
        "**CSS Import:**",
        "```css",
        "@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap');",
        "```",
        "",
    ]
    return "\n".join(lines)


def build_reconciled_anti_patterns_section(
    intake: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    must_avoid = unique_preserve_order(
        [str(item) for item in intake.get("must_avoid", []) if str(item).strip()]
    )
    existing: set[str] = set()

    def add_line(lines: list[str], text: str) -> None:
        key = text.strip().lower()
        if key in existing:
            return
        existing.add(key)
        lines.append(text)

    lines = [
        "## Anti-Patterns (Do NOT Use)",
        "",
    ]
    if analysis["aggregate"]["brightness_label"] == "light":
        add_line(lines, "- Forcing dark mode against a predominantly light reference pack")
    add_line(lines, "- Decorative visual noise that competes with data, forms, or status information")
    add_line(lines, "- Crowded cards or cramped panels that reduce scanability")
    for item in must_avoid:
        normalized = item.lower()
        if analysis["aggregate"]["brightness_label"] == "light" and "dark" in normalized and "light" in normalized:
            continue
        add_line(lines, f"- {item}")
    lines.extend(
        [
            "",
            "### Additional Forbidden Patterns",
            "",
            "- Emojis as icons. Use SVG icons from a real icon set.",
            "- Missing `cursor-pointer` on clickable elements.",
            "- Layout-shifting hover transforms.",
            "- Low-contrast text that drops below accessibility thresholds.",
            "- Instant state changes without transitions.",
            "- Invisible focus states.",
            "",
        ]
    )
    return "\n".join(lines)


def reconcile_master_with_analysis(
    master_content: str,
    intake: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    legacy_page_reference = "`design-system/" + "pages/[page-name].md`"
    legacy_reference_warning = (
        "Using fallback references outside the local design-system folder. "
        "Prefer moving them into `projects-docs/"
        + "design-system/<project>/references/`."
    )
    master_content = master_content.replace(
        legacy_page_reference,
        "`page.<page-name>.md` in `projects-docs/40-design-system/`",
    )
    master_content = replace_section(
        master_content,
        "### Color Palette",
        "\n### Typography",
        build_reconciled_color_palette_section(analysis),
    )
    master_content = replace_section(
        master_content,
        "## Component Specs",
        "\n---\n\n## Style Guidelines",
        build_reconciled_component_specs_section(analysis),
    )
    master_content = replace_section(
        master_content,
        "### Typography",
        "\n### Spacing Variables",
        build_reconciled_typography_section(intake, analysis),
    )
    master_content = replace_section(
        master_content,
        "## Style Guidelines",
        "\n---\n\n## Anti-Patterns",
        build_reconciled_style_section(intake, analysis),
    )
    master_content = replace_section(
        master_content,
        "## Anti-Patterns (Do NOT Use)",
        "\n---\n\n## Pre-Delivery Checklist",
        build_reconciled_anti_patterns_section(intake, analysis),
    )
    master_content = master_content.replace(
        legacy_reference_warning,
        "Using legacy references outside `projects-docs/references/images/`. Prefer consolidating them in the official images directory.",
    )
    master_content = master_content.replace("âŒ", "-")

    return master_content


def intake_warnings(intake: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    required_scalars = ["product_type", "industry", "target_feel"]
    for key in required_scalars:
        if not str(intake.get(key, "")).strip():
            warnings.append(f"Missing `{key}` in intake.json.")
    if not intake.get("style_keywords"):
        warnings.append("`style_keywords` is empty.")
    if not intake.get("liked_examples"):
        warnings.append("`liked_examples` is empty; the agent may need a follow-up question.")
    if not intake.get("must_avoid"):
        warnings.append("`must_avoid` is empty; the agent may miss anti-patterns you dislike.")
    return warnings


def init_project(paths: PipelinePaths, force: bool = False) -> None:
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.references_dir.mkdir(parents=True, exist_ok=True)

    write_json(paths.intake_file, default_intake(paths.project_name), force=force)
    write_text(paths.notes_file, default_notes(paths.project_slug), force=force)
    write_text(paths.readme_file, default_readme(paths), force=force)
    write_text(
        paths.prompt_foundation_file,
        foundation_prompt(paths),
        force=force,
    )
    write_text(
        paths.prompt_component_file,
        component_prompt(paths),
        force=force,
    )
    write_text(
        paths.prompt_page_file,
        page_prompt(paths),
        force=force,
    )


def collect_status(paths: PipelinePaths) -> dict[str, Any]:
    intake = load_json(paths.intake_file, default_intake(paths.project_name))
    discovery = discover_reference_images(paths)
    notes_present = paths.notes_file.exists() and bool(paths.notes_file.read_text(encoding="utf-8").strip())

    warnings = intake_warnings(intake)
    if not discovery.images:
        warnings.append(
            f"No reference images found in `{paths.references_dir}`."
        )

    return {
        "project_name": paths.project_name,
        "project_slug": paths.project_slug,
        "root": str(paths.root),
        "references_dir": str(paths.references_dir),
        "source_directories": [path_for_display(path) for path in discovery.source_dirs],
        "used_fallback_sources": discovery.used_fallback,
        "image_count": len(discovery.images),
        "images": [path_for_display(path) for path in discovery.images],
        "master_exists": paths.master_file.exists(),
        "page_override_files": [
            path_for_display(path)
            for path in sorted(paths.root.glob("page.*.md"))
        ],
        "image_analysis_exists": paths.image_analysis_md_file.exists(),
        "notes_present": notes_present,
        "warnings": warnings,
    }


def prompt_for_missing_fields(intake: dict[str, Any]) -> dict[str, Any]:
    updated = json.loads(json.dumps(intake))

    prompts = [
        (
            "style_keywords",
            "Style keywords (comma-separated, blank to keep current): ",
            True,
        ),
        (
            "liked_examples",
            "What did you like in the references? (comma-separated, blank to keep current): ",
            True,
        ),
        (
            "must_avoid",
            "What should the UI avoid? (comma-separated, blank to keep current): ",
            True,
        ),
        (
            "target_feel",
            "Target feel in one sentence (blank to keep current): ",
            False,
        ),
    ]

    for key, message, expects_list in prompts:
        current_value = updated.get(key)
        is_missing = not current_value
        if not is_missing:
            continue

        answer = input(message).strip()
        if not answer:
            continue

        if expects_list:
            updated[key] = [item.strip() for item in answer.split(",") if item.strip()]
        else:
            updated[key] = answer

    return updated


def derive_query(intake: dict[str, Any], analysis: dict[str, Any] | None = None) -> str:
    component_examples = intake.get("component_examples", {})
    if not isinstance(component_examples, dict):
        component_examples = {}

    analysis_terms: list[str] = []
    if analysis:
        aggregate = analysis.get("aggregate", {})
        analysis_terms.extend(str(item) for item in aggregate.get("style_keywords", []))
        filtered_terms = [
            str(item)
            for item in aggregate.get("suggested_query_terms", [])
            if str(item) not in {"web", "app", "website", "pos", "orders", "payment"}
        ]
        analysis_terms.extend(filtered_terms[:6])

    raw_parts: list[str] = [
        str(intake.get("product_type", "")),
        str(intake.get("industry", "")),
        *[str(item) for item in intake.get("style_keywords", [])],
        str(intake.get("target_feel", "")),
        *[str(item) for item in intake.get("liked_examples", [])[:3]],
        *[str(item) for item in intake.get("must_keep", [])[:2]],
        *[str(value) for value in component_examples.values()],
        *analysis_terms,
    ]
    query_parts = unique_preserve_order(raw_parts)
    return " ".join(query_parts)


def build_context_document(
    paths: PipelinePaths,
    intake: dict[str, Any],
    query: str,
    analysis: dict[str, Any],
    page: str | None,
) -> str:
    aggregate = analysis["aggregate"]
    lines = [
        "# Design System Implementation Context",
        "",
        f"Project: {paths.project_name}",
        "Root: `projects-docs/40-design-system/`",
        f"Generated query: `{query}`",
        "",
        "## Inputs",
        "",
        "- Intake: `projects-docs/40-design-system/intake.json`",
        "- Notes: `projects-docs/40-design-system/notes.md`",
        f"- References: {', '.join(f'`{path}`' for path in analysis['source_directories']) or '`(none)`'}",
        "- Image analysis: `projects-docs/40-design-system/IMAGE_ANALYSIS.md`",
        "",
        "## Reference Images",
        "",
    ]

    for image in analysis["images"]:
        lines.append(f"- `{image['path']}`")
    if not analysis["images"]:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Intake Summary",
            "",
            f"- Product type: {intake.get('product_type', '')}",
            f"- Industry: {intake.get('industry', '')}",
            f"- Style keywords: {', '.join(intake.get('style_keywords', [])) or '(empty)'}",
            f"- Target feel: {intake.get('target_feel', '') or '(empty)'}",
            f"- Liked examples: {', '.join(intake.get('liked_examples', [])) or '(empty)'}",
            f"- Must keep: {', '.join(intake.get('must_keep', [])) or '(empty)'}",
            f"- Must avoid: {', '.join(intake.get('must_avoid', [])) or '(empty)'}",
            "",
            "## Automatic Visual Signals",
            "",
            f"- Inferred tone: {aggregate['brightness_label']}, {aggregate['saturation_label']}, {aggregate['density_label']}",
            f"- Suggested query terms: {', '.join(aggregate['suggested_query_terms']) or '(none)'}",
            f"- Primary token hint: `{aggregate['token_hints']['primary'] or '(unknown)'}`",
            f"- Accent token hint: `{aggregate['token_hints']['accent'] or '(unknown)'}`",
            f"- Background token hint: `{aggregate['token_hints']['background'] or '(unknown)'}`",
            f"- Text token hint: `{aggregate['token_hints']['text'] or '(unknown)'}`",
            "",
            "## Generated Artifacts",
            "",
            "- Master rules: `projects-docs/40-design-system/MASTER.md`",
            "- Page overrides: `projects-docs/40-design-system/page.<name>.md`",
            "- Prompt pack: `projects-docs/40-design-system/prompt-*.md`",
            "- Image analysis JSON: `projects-docs/40-design-system/image-analysis.json`",
        ]
    )

    if page:
        lines.append(f"- Current page override requested: `{page}`")

    lines.extend(
        [
            "",
            "## Implementation Notes",
            "",
            "- Use the local reference pack as the visual source of truth.",
            "- React + Vite + Tailwind is the default target stack.",
            "- Read `MASTER.md` before coding, then apply page overrides when they exist.",
            "- Use `IMAGE_ANALYSIS.md` to keep color, density, and contrast decisions anchored to the references.",
            "- Keep recurring patterns in the shared design system instead of burying them inside pages.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def run_generation(
    paths: PipelinePaths,
    page: str | None,
    output_format: str,
    prompt_missing: bool,
) -> int:
    init_project(paths)

    intake = load_json(paths.intake_file, default_intake(paths.project_name))
    discovery = discover_reference_images(paths)

    if not discovery.images:
        print(
            "No reference images found. Add files to "
            f"`{paths.references_dir}`."
        )
        return 1

    if prompt_missing and sys.stdin.isatty():
        updated = prompt_for_missing_fields(intake)
        if updated != intake:
            write_json(paths.intake_file, updated, force=True)
            intake = updated

    analysis = build_image_analysis(discovery)
    write_json(paths.image_analysis_json_file, analysis, force=True)
    write_text(
        paths.image_analysis_md_file,
        format_image_analysis_markdown(analysis),
        force=True,
    )

    query = derive_query(intake, analysis)
    if not query:
        print("Could not derive a design-system query from intake.json and image analysis.")
        return 1

    temp_output_root = paths.root / ".tmp-generation"
    shutil.rmtree(temp_output_root, ignore_errors=True)

    command = [
        sys.executable,
        str(UI_UX_SEARCH_SCRIPT),
        query,
        "--design-system",
        "--persist",
        "--project-name",
        paths.project_name,
        "--format",
        output_format,
        "--output-dir",
        str(temp_output_root),
    ]
    if page:
        command.extend(["--page", page])

    result = subprocess.run(
        command,
        cwd=WORKSPACE_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )

    if result.returncode != 0:
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        return result.returncode
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)

    generated_root = temp_output_root / "design-system" / paths.project_slug
    generated_master = generated_root / "MASTER.md"
    if generated_master.exists():
        master_content = generated_master.read_text(encoding="utf-8")
        master_content = inject_reference_analysis(master_content, analysis)
        master_content = reconcile_master_with_analysis(master_content, intake, analysis)
        write_text(paths.master_file, master_content, force=True)
    if page:
        generated_page = generated_root / "pages" / f"{slugify(page)}.md"
        if generated_page.exists():
            write_text(
                paths.root / page_override_filename(page),
                generated_page.read_text(encoding="utf-8"),
                force=True,
            )
    shutil.rmtree(temp_output_root, ignore_errors=True)

    context = build_context_document(paths, intake, query, analysis, page)
    write_text(paths.context_file, context, force=True)

    print("")
    print("Design system generated from the local reference pack.")
    print(f"Root: {paths.root}")
    print(f"MASTER.md: {paths.master_file}")
    if page:
        print(f"Page override: {paths.root / page_override_filename(page)}")
    print(f"Image analysis: {paths.image_analysis_md_file}")
    print(f"Implementation context: {paths.context_file}")
    return 0


def print_status(status: dict[str, Any]) -> None:
    print(f"Project: {status['project_name']}")
    print(f"Root: {status['root']}")
    print(f"References: {status['image_count']} image(s)")
    print(f"MASTER.md: {'yes' if status['master_exists'] else 'no'}")
    print(f"Image analysis: {'yes' if status['image_analysis_exists'] else 'no'}")
    print(f"Notes present: {'yes' if status['notes_present'] else 'no'}")
    print(f"Page overrides: {len(status['page_override_files'])}")
    if status["source_directories"]:
        print("Source directories:")
        for source in status["source_directories"]:
            print(f"  - {source}")
    if status["images"]:
        print("Images:")
        for image in status["images"]:
            print(f"  - {image}")
    if status["page_override_files"]:
        print("Page override files:")
        for path in status["page_override_files"]:
            print(f"  - {path}")
    if status["warnings"]:
        print("Warnings:")
        for warning in status["warnings"]:
            print(f"  - {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Design system pipeline for project-docs references")
    parser.add_argument("command", choices=["init", "status", "generate"], help="Pipeline command")
    parser.add_argument("--project", help="Project name stored in the generated design-system metadata")
    parser.add_argument("--page", help="Optional page override to generate")
    parser.add_argument(
        "--format",
        choices=["ascii", "markdown"],
        default="markdown",
        help="Design system output format for the generated search result",
    )
    parser.add_argument("--json", action="store_true", help="Print status as JSON")
    parser.add_argument(
        "--prompt-missing",
        action="store_true",
        help="Prompt for missing intake fields during generate",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite scaffolded files during init")

    args = parser.parse_args()
    paths = resolve_paths(args.project)

    if args.command == "init":
        init_project(paths, force=args.force)
        print(f"Initialized design-system intake at {paths.root}")
        return 0

    if args.command == "status":
        status = collect_status(paths)
        if args.json:
            print(json.dumps(status, indent=2, ensure_ascii=True))
        else:
            print_status(status)
        return 0

    return run_generation(
        paths=paths,
        page=args.page,
        output_format=args.format,
        prompt_missing=args.prompt_missing,
    )


if __name__ == "__main__":
    raise SystemExit(main())
