# MotionLab

Procedural animation studio, developed entirely from an iPhone using GitHub and cloud builds.

## Mobile animation app

After the pull request is merged and GitHub Pages is enabled, open:
https://hasky00.github.io/motionlab/

The site plays a gold Bitcoin coin with moving particles automatically in Safari.
Pause, restart, change playback speed, or scrub to a frame. Reduced Motion starts
the preview paused. Download GIF saves the real rendered GIF directly without
a GitHub login or an Actions ZIP. Open original GIF is an alternative for Safari's
Share menu and Save to Files. No desktop is required.

The site is a browser preview and export app for the current Bitcoin animation.
It does not run Python in Safari or offer arbitrary new animation generation.

## Activate deployment (repository owner, one time)

1. Merge the mobile app pull request into main.
2. Open https://github.com/hasky00/motionlab/settings/pages
3. Under **Build and deployment → Source**, select **GitHub Actions**.
4. Open **Actions → Mobile web app → Run workflow**, choose **main**, and run.
5. Wait for both build and deploy to succeed. Open the URL in the deploy job.

The address above is the intended deployment URL, not a claim of a live deployment.
If deployment reports Pages is not enabled, complete step 3 and rerun the workflow.
Pull requests build and validate assets but do not deploy.

## Build locally (optional)

```bash
python -m pip install -r requirements.txt
python scripts/build_web.py
python -m http.server 8000 --directory dist
```

Open http://localhost:8000. The portable dist folder contains the interface, a
48-frame preview sheet, and the downloadable looping GIF, all with relative paths
for GitHub Pages project hosting. The build verifies multiple visibly changing
frames and infinite looping. No third-party scripts, fonts, or accounts are needed.

## Existing cloud renderer

The original Python renderer and **Render Bitcoin Preview** workflow remain
available unchanged. On an iPhone, run it from Actions and download the
motionlab-bitcoin-gif artifact if you need the original ZIP workflow.

```bash
python motionlab.py --output out/bitcoin.gif
```
