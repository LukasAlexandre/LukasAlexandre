"""Turn the source photograph into real ASCII characters (run locally, once per photo).

Pipeline: crop -> GrabCut matte (seeded by the polygon in config/profile.json) ->
CLAHE local contrast -> unsharp mask -> area resample to the character grid ->
tone-to-glyph mapping. The output is a plain text file; the SVG renderer reads it,
so CI never needs OpenCV or the photograph.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def foreground_mask(rgb: np.ndarray, cfg: dict) -> np.ndarray:
    h, w = rgb.shape[:2]
    left, top, right, bottom = cfg["crop"]
    sx, sy = w / (right - left), h / (bottom - top)

    def to_crop(x: float, y: float) -> tuple[int, int]:
        return int((x - left) * sx), int((y - top) * sy)

    poly = np.array([to_crop(x, y) for x, y in cfg["silhouette"]], np.int32)
    inside = np.zeros((h, w), np.uint8)
    cv2.fillPoly(inside, [poly], 1)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (w // 14 | 1, w // 14 | 1))
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)
    mask[cv2.dilate(inside, k) == 1] = cv2.GC_PR_BGD
    mask[inside == 1] = cv2.GC_PR_FGD
    for x0, y0, x1, y1 in cfg["sureForeground"]:
        (ax, ay), (bx, by) = to_crop(x0, y0), to_crop(x1, y1)
        mask[max(ay, 0):max(by, 0), max(ax, 0):max(bx, 0)] = cv2.GC_FGD
    cv2.setRNGSeed(7)
    bgd, fgd = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), mask, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
    fg = np.isin(mask, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(fg)
    if n > 1:
        fg = (labels == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    return fg


def build_ascii(image: Image.Image, cfg: dict, columns: int | None = None) -> list[str]:
    cols = columns or cfg["columns"]
    if isinstance(cols, bool) or not isinstance(cols, int) or not 24 <= cols <= 400:
        raise ValueError("ASCII columns must be an integer between 24 and 400")
    crop = ImageOps.exif_transpose(image).convert("RGB").crop(tuple(cfg["crop"]))
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
    rgb = np.array(crop)
    mask = foreground_mask(rgb, cfg)
    if not np.any(mask):
        raise ValueError("Portrait segmentation produced an empty foreground")

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 50, 9)
    local = cv2.createCLAHE(clipLimit=cfg["claheClip"], tileGridSize=(6, 6)).apply(gray)
    blur = cv2.GaussianBlur(local, (0, 0), 4)
    local = cv2.addWeighted(local, 1 + cfg["sharpen"], blur, -cfg["sharpen"], 0)

    lo, hi = np.percentile(local[mask == 1], (4, 97))
    tone = np.clip((local.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1) ** cfg["gamma"]

    # Thin dark structures (glasses frame, eyes, lips, brows) vanish when averaged into
    # cells, so they are carved out of the tone explicitly.
    g = gray.astype(np.float32)
    dark = np.clip((cv2.GaussianBlur(g, (0, 0), 11) - g - 14) / 45, 0, 1)
    dark = cv2.dilate(dark, np.ones((3, 3), np.uint8))
    tone *= 1 - cfg["lineStrength"] * dark

    # Dim the clothing so the face stays the focal point.
    y = np.linspace(0, 1, tone.shape[0], dtype=np.float32)[:, None]
    tone *= 1 - cfg["bodyDim"] * np.clip((y - cfg["bodyStart"]) / 0.08, 0, 1)
    tone *= 1 - cfg.get("bodyFade", 0.55) * np.clip((y - 0.88) / 0.12, 0, 1)
    floor = cfg.get("foregroundFloor", 0)
    tone = floor + (1 - floor) * tone

    rows = round(cols * (crop.height / crop.width) * cfg["cellAspect"] / cfg["lineHeight"])
    small = cv2.resize(tone.astype(np.float32), (cols, rows), interpolation=cv2.INTER_AREA)
    alpha = cv2.resize(mask.astype(np.float32), (cols, rows), interpolation=cv2.INTER_AREA)

    ramp, bg = cfg["ramp"], cfg["backgroundChar"]
    lines = []
    for y in range(rows):
        line = []
        for x in range(cols):
            if alpha[y, x] < 0.5:
                line.append(bg)
            else:
                line.append(ramp[min(int(small[y, x] * len(ramp)), len(ramp) - 1)])
        lines.append("".join(line))
    return lines


def main() -> None:
    cfg = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))["portrait"]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=str(ROOT / cfg["source"]))
    ap.add_argument("--columns", type=int, default=cfg["columns"], help="character density")
    ap.add_argument("--output", default=str(ROOT / cfg["output"]))
    args = ap.parse_args()
    with Image.open(args.source) as im:
        lines = build_ascii(im, cfg, args.columns)
    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{args.columns}x{len(lines)} characters -> {args.output}")


if __name__ == "__main__":
    main()
