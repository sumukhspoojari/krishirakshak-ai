# KrishiRakshak AI — Production Deployment Guide

This guide walks you through deploying **KrishiRakshak AI** to **GitHub**, **Render** (FastAPI backend), and **Vercel** (React/Vite frontend), with **Supabase** PostgreSQL and secure **Groq API key** configuration.

---

## 🏗️ Architecture Overview
* **Frontend**: React 19 + Vite (Deployed on **Vercel** CDN)
* **Backend**: FastAPI + LangGraph Agent + SQLAlchemy (Deployed on **Render**)
* **Database**: **Supabase** (Managed PostgreSQL) or SQLite
* **AI Engine**: **Groq Cloud API** (Llama-3.3-70b / Llama-3.2-11b-vision)
* **Storage**: Encrypted PBKDF2 authentication, file uploads with MIME/extension protection.

---

## Step 1: Push Repository to GitHub

1. Initialize git and check status (sensitive files like `.env` and `*.db` are automatically ignored):
```bash
git init
git add .
git status
```
> **Security Check**: Ensure `.env` is **NOT** listed in `Changes to be committed`. Only `.env.example` should be tracked.

2. Commit and push to your private or public GitHub repository:
```bash
git commit -m "feat: production deployment configuration for KrishiRakshak AI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/krishirakshak-ai.git
git push -u origin main
```

---

## Step 2: Set Up Supabase (Managed PostgreSQL)

1. Go to [https://supabase.com](https://supabase.com) and create a free project (e.g., `krishirakshak-db`).
2. Navigate to **Project Settings** -> **Database**.
3. Under **Connection string**, select **URI** (or Connection Pooling / Transaction mode).
4. Copy the URI. It will look like:
   `postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`
5. Save this URI; you will enter it in Render as `DATABASE_URL`.

---

## Step 3: Deploy Backend on Render

1. Log into [https://render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository `krishirakshak-ai`.
4. Configure the settings:
   * **Name**: `krishirakshak-ai-backend`
   * **Root Directory**: Leave blank (or specify `backend` if deploying only the backend folder)
   * **Environment**: `Python 3`
   * **Build Command**: `pip install -r backend/requirements.txt`
   * **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   * **Plan**: Free
5. Expand **Advanced** -> **Environment Variables** and add:

| Key | Value | Notes |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | `gsk_...` | **Required**: Your secret Groq API key from https://console.groq.com/keys |
| `DATABASE_URL` | `postgresql://...` | **Optional/Recommended**: Your Supabase connection string (defaults to SQLite if blank) |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app` | We will update this with your actual Vercel URL in Step 4 |
| `DEMO_MODE` | `false` | Set to `false` for full live AI responses with your Groq key |
| `OPENWEATHER_API_KEY` | `...` | Optional: For live weather advisories |

6. Click **Create Web Service**.
7. Once deployed, copy your backend URL (e.g., `https://krishirakshak-ai-backend.onrender.com`).
8. Test health endpoint in browser: `https://krishirakshak-ai-backend.onrender.com/health` -> should return `{"status":"ok"}`.

---

## Step 4: Deploy Frontend on Vercel

1. Log into [https://vercel.com](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your GitHub repository `krishirakshak-ai`.
4. In the configuration screen:
   * **Framework Preset**: `Vite`
   * **Root Directory**: Click **Edit** and select `frontend`
   * **Build Command**: `npm run build`
   * **Output Directory**: `dist`
5. Expand **Environment Variables** and add:

| Key | Value |
| :--- | :--- |
| `VITE_API_BASE_URL` | `https://krishirakshak-ai-backend.onrender.com` (Your Render backend URL from Step 3 without trailing slash) |

6. Click **Deploy**.
7. In ~60 seconds, your frontend will be live at `https://your-project.vercel.app`!
8. Head back to **Render** -> **Environment Variables** and update `CORS_ORIGINS` to include your actual Vercel URL (e.g. `https://your-project.vercel.app`).

---

## Step 5: Verification & Production Health Checklist

- [ ] **Landing Page**: Visiting `https://your-project.vercel.app/` loads the hero page with live metrics and language selector.
- [ ] **Sign In / Registration**: Visiting `/signup` allows registering a new farmer account and persists the data in Supabase/SQLite.
- [ ] **Direct URL Navigation**: Navigating to `/login` or `/signup` directly or refreshing does not throw a 404 (handled by `vercel.json`).
- [ ] **AI Agronomy Chat**: Asking `"steps to grow raagi"` in Kannada/English returns structured action plans powered by Groq.
- [ ] **Leaf Photo Diagnosis**: Uploading a diseased leaf image uploads cleanly, validates MIME type/size, and renders in chat via the deployed backend.
- [ ] **Security**: Inspect browser network calls to verify that no passwords, Groq API keys, or database credentials are ever exposed in responses or frontend bundles.
