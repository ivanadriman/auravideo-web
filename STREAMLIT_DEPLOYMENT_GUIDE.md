# 🌐 100% Free Web Deployment Guide (Streamlit Community Cloud + GitHub)

This guide takes **3 minutes** and deploys your AuraVideo Studio web app online with a permanent public link (`https://auravideo-studio.streamlit.app`) at **$0 cost forever**.

---

## 📁 What You Are Deploying
All web files are neatly isolated inside `web_deployment/`:
- `streamlit_app.py` — The interactive web UI (upload, live frame scrubber, preset picker, sliders, video render & download).
- `video_service.py` — Zero-disk in-memory video processor with lossless audio pass-through.
- `requirements.txt` — Python libraries (`streamlit`, `opencv-python-headless`, `numpy`).
- `packages.txt` — Linux system package (`ffmpeg`).
- `core/` — All 36 aesthetic presets and the `FilterEngine`.

---

## Step 1: Push `web_deployment` to GitHub (2 Minutes)

1. Open your browser and log into [GitHub](https://github.com).
2. Click **New Repository** (top right `+` button):
   - **Repository name:** `auravideo-web`
   - **Visibility:** **Public** (required for free Streamlit Community Cloud)
   - Do **not** check "Add a README file".
   - Click **Create repository**.

3. On your computer, open PowerShell and push the `web_deployment` folder to your new GitHub repository:
   ```powershell
   cd "c:\Users\kiris\OneDrive\Documents\AI Projects\Video Filter App\web_deployment"
   git init
   git add .
   git commit -m "Deploy AuraVideo Studio Web"
   git branch -M main
   git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/auravideo-web.git
   git push -u origin main
   ```
   *(Replace `<YOUR-GITHUB-USERNAME>` with your actual GitHub username).*

---

## Step 2: Deploy on Streamlit Community Cloud (1 Minute)

1. Go to **[https://share.streamlit.io](https://share.streamlit.io)**.
2. Click **Continue with GitHub** and authorize it.
3. Once logged in, click the **"New app"** (or **"Create app"**) button.
4. Fill in the simple form:
   - **Repository:** `<YOUR-GITHUB-USERNAME>/auravideo-web`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL (optional):** Choose a custom subdomain like `auravideo-studio`
5. Click **Deploy!**

---

## Step 3: That's It! 🎉

- Streamlit will read `packages.txt` (automatically installs FFmpeg on Linux) and `requirements.txt` (installs Streamlit, OpenCV, and NumPy).
- In ~60 to 90 seconds, your app will open live at:
  ```
  https://auravideo-web.streamlit.app
  ```
- Anyone on the internet can now upload video clips, browse your 36 aesthetic presets, inspect live before/after frames, and export graded videos!
- **Auto-Sync:** Whenever you commit new presets or adjustments to GitHub, Streamlit automatically updates the live app.
