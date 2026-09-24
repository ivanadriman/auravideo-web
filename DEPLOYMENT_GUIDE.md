# 🚀 Complete Deployment Guide: AuraVideo Studio Online

This guide walks you through deploying your video filter web application online for **100% free** using **GitHub + Hugging Face Spaces** (2 vCPU, 16 GB RAM, 50 GB storage).

All deployment-ready files are isolated inside the `web_deployment/` folder so your desktop app remains untouched.

---

## 📂 Web Deployment Folder Contents (`web_deployment/`)

```
web_deployment/
├── app.py              # Gradio web app with live frame preview & full video export
├── video_service.py    # Zero-disk headless video pipeline & audio muxing
├── requirements.txt    # Cloud Python dependencies (gradio, opencv-python-headless, numpy)
├── packages.txt        # Linux system dependencies (ffmpeg)
├── README.md           # Hugging Face Spaces configuration header
└── core/               # FilterEngine & all 36 aesthetic preset definitions
    ├── config.py
    ├── filter_engine.py
    └── ffmpeg_utils.py
```

---

## Method 1: Deploy Directly via Hugging Face Web (Easiest — 3 Minutes)

If you don't want to use command line tools, you can upload the `web_deployment` files directly via your web browser:

### Step 1: Create a Free Hugging Face Account
1. Go to [https://huggingface.co/join](https://huggingface.co/join) and create an account.
2. Verify your email.

### Step 2: Create a New Space
1. Click your profile icon (top right) ➔ **New Space** (or visit [https://huggingface.co/new-space](https://huggingface.co/new-space)).
2. Fill in:
   - **Space name:** `auravideo-studio` (or your preferred name)
   - **License:** `mit` (or choose another)
   - **Select the Space SDK:** Choose **Gradio**
   - **Gradio template:** Choose **Blank**
   - **Space Hardware:** Choose **CPU basic • 2 vCPU • 16 GB RAM • Free**
   - **Visibility:** **Public**
3. Click **Create Space**.

### Step 3: Upload the Files
1. In your newly created Space, click the **Files** tab.
2. Click **Add file** ➔ **Upload files**.
3. Drag and drop the contents of your local `web_deployment/` folder:
   - `app.py`
   - `video_service.py`
   - `requirements.txt`
   - `packages.txt`
   - `README.md`
   - The entire `core/` folder (including `config.py`, `filter_engine.py`, `ffmpeg_utils.py`)
4. At the bottom, click **Commit changes to main**.

### Step 4: Launch!
1. Click the **App** tab.
2. Hugging Face will automatically read `packages.txt` (installs FFmpeg) and `requirements.txt` (installs Python libraries).
3. In about 1–2 minutes, your web app will be live with a permanent URL:
   `https://huggingface.co/spaces/<your-username>/auravideo-studio`

---

## Method 2: Deploy from GitHub (Automated CI/CD)

If you want your web app to update automatically every time you `git push` to GitHub:

### Step 1: Push `web_deployment` to a GitHub Repository
1. On GitHub, create a new public repository (e.g. `auravideo-web`).
2. On your computer, open a terminal inside the `web_deployment` folder:
   ```bash
   cd "c:\Users\kiris\OneDrive\Documents\AI Projects\Video Filter App\web_deployment"
   git init
   git add .
   git commit -m "Initial commit for AuraVideo Studio web app"
   git branch -M main
   git remote add origin https://github.com/<your-github-username>/auravideo-web.git
   git push -u origin main
   ```

### Step 2: Connect GitHub to Hugging Face
1. Create a Space on Hugging Face as described in Method 1.
2. In your Space, go to **Settings** ➔ scroll down to **Github Sync**.
3. Link your GitHub repository (`<your-github-username>/auravideo-web`).
4. Whenever you push new presets or code to GitHub, Hugging Face will automatically rebuild and deploy your changes.

---

## 💻 How to Test Locally Before Deploying

You can test the web app on your own computer right now:

1. Open PowerShell or Command Prompt.
2. Activate your app's virtual environment:
   ```powershell
   cd "c:\Users\kiris\OneDrive\Documents\AI Projects\Video Filter App"
   .\venv\Scripts\activate.bat
   ```
3. Install Gradio:
   ```powershell
   pip install gradio
   ```
4. Run the web app:
   ```powershell
   python web_deployment\app.py
   ```
5. Open your browser and navigate to:
   ```
   http://localhost:7860
   ```
6. You will see the complete AuraVideo Studio web interface:
   - Upload any video (e.g., `Sample.mp4`).
   - Select any of the **36 curated presets**.
   - Adjust Light, Color, FX sliders.
   - See instant before/after frame previews.
   - Click **Process Full Video with Audio** to download the finished file!
