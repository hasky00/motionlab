"""MotionLab: deterministic procedural Bitcoin animation renderer."""
from __future__ import annotations
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def font(size: int):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/System/Library/Fonts/Supplemental/Arial Bold.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def frame(index: int, count: int = 48, size: int = 480) -> Image.Image:
    # Draw at a fixed reference resolution and resize for reproducibility.
    S = 480
    phase = 2 * math.pi * index / count
    im = Image.new("RGB", (S, S), "#070d1b")
    d = ImageDraw.Draw(im)
    cx, cy = 240, 231
    # Orbiting points and circular tracks.
    for radius in (156, 186):
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius),
                  outline="#493417", width=2)
    for n in range(65):
        a = n * 2.399963 + phase * (0.4 + (n % 5) * 0.08)
        radius = 145 + (n * 37) % 74
        x = cx + math.cos(a) * radius
        y = cy + math.sin(a) * radius * 0.8
        r = 1 + n % 3
        d.ellipse((x-r, y-r, x+r, y+r),
                  fill=("#f8c66b" if n % 3 else "#8d5a21"))
    # A slight rocking motion keeps the Bitcoin mark legible at all times.
    x = cx + round(5 * math.sin(phase))
    y = cy + round(4 * math.cos(phase))
    d.ellipse((x-118, y-118, x+118, y+118), fill="#87500b", outline="#ffe28b", width=6)
    d.ellipse((x-106, y-106, x+106, y+106), fill="#e8a722", outline="#fff0a7", width=5)
    d.ellipse((x-91, y-91, x+91, y+91), fill="#c17a0c", outline="#ffd66d", width=3)
    # Draw a bold B with Bitcoin's characteristic two vertical strokes.
    f = font(182)
    bb = d.textbbox((0, 0), "B", font=f, stroke_width=1)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    tx = x - tw/2 - bb[0]
    ty = y - th/2 - bb[1] - 6
    d.text((tx, ty), "B", font=f, fill="#fff1b0", stroke_width=2, stroke_fill="#75420a")
    for dx in (-14, 10):
        d.line((x+dx, y-89, x+dx, y-67), fill="#fff1b0", width=8)
        d.line((x+dx, y+70, x+dx, y+91), fill="#fff1b0", width=8)
    # Moving satellite highlight.
    a = phase
    sx, sy = cx + 185*math.cos(a), cy + 185*math.sin(a)
    d.ellipse((sx-7, sy-7, sx+7, sy+7), fill="#fff4bd")
    title = "MOTIONLAB  /  BITCOIN"
    d.text((S/2, 448), title, anchor="mm", font=font(16), fill="#c99a53")
    return im if size == S else im.resize((size, size), Image.Resampling.LANCZOS)

def render(output: Path, frames: int = 48, size: int = 480, duration: int = 60):
    if frames < 2 or not 128 <= size <= 2048 or duration < 20:
        raise ValueError("Require frames >= 2, 128 <= size <= 2048, duration >= 20")
    images = [frame(i, frames, size) for i in range(frames)]
    output.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(output, save_all=True, append_images=images[1:],
                   duration=duration, loop=0, optimize=False, disposal=2)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a looping Bitcoin GIF")
    parser.add_argument("--output", type=Path, default=Path("out/bitcoin.gif"))
    parser.add_argument("--frames", type=int, default=48)
    parser.add_argument("--size", type=int, default=480)
    args = parser.parse_args()
    print(render(args.output, args.frames, args.size))
