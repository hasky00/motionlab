"""Build a portable static site from the unchanged Python renderer."""
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image, ImageChops
from motionlab import frame, render

root = Path(__file__).resolve().parents[1]
out = root / "dist"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(root / "web", out)
assets = out / "assets"
assets.mkdir()
render(assets / "bitcoin.gif")
sheet = Image.new("RGB", (480 * 8, 480 * 6))
for i in range(48):
    sheet.paste(frame(i), ((i % 8) * 480, (i // 8) * 480))
sheet.save(assets / "frames.png", optimize=True)
with Image.open(assets / "bitcoin.gif") as gif:
    assert gif.n_frames == 48 and gif.info.get("loop") == 0
    gif.seek(0)
    first = gif.convert("RGB")
    gif.seek(12)
    assert ImageChops.difference(first, gif.convert("RGB")).getbbox()
print("Built dist: 48 changing frames, looping GIF, matching preview sheet.")
