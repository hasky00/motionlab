# MotionLab

Procedural animation studio, developed entirely from an iPhone using GitHub and cloud builds.

## First milestone: animated Bitcoin

The renderer creates a looping GIF with a gold coin, a prominent Bitcoin-style B with double vertical strokes, and moving orbital particles.

## Run locally (optional)

```bash
python -m pip install -r requirements.txt
python motionlab.py --output out/bitcoin.gif
```

## Run without a computer

1. Open **Actions** in this GitHub repository using Safari on your iPhone.
2. Select **Render Bitcoin Preview**, then **Run workflow** (or wait for the push-triggered run).
3. When the workflow finishes, open its run and download **motionlab-bitcoin-gif** from **Artifacts**.
4. Unzip the artifact in iPhone Files to view `bitcoin.gif`.

This is the rendering MVP. A native macOS GUI and macOS packaging workflow are planned for the next milestone.
