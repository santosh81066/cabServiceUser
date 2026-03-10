# Deploy Backend on cPanel (Public Hosting)

Steps to push your code and run the Cab Service API on cPanel.

---

## 1. Push code safely (no secrets)

Your repo can be **public**. Do **not** commit:

- `.env` (already in `.gitignore`)
- Any `*-firebase-adminsdk-*.json` or `firebase-service-account.json` (already in `.gitignore`)

Before pushing:

```bash
cd backend
# Make sure secrets are not staged
git status
# .env and *firebase*.json should NOT appear. If they do, run:
# git reset HEAD .env  and  git reset HEAD *firebase*.json
```

On cPanel you will set **environment variables** and upload the **service account JSON** separately (see below).

---

## 2. Upload code to cPanel

- **Option A – Git:** If cPanel has **Git Version Control**, clone your repo into e.g. `~/cabservice-backend` (or your chosen path).
- **Option B – FTP/File Manager:** Upload the `backend` folder (without `venv/`, without `.env`, without `*firebase*.json`) into a folder under your home, e.g. `~/cabservice-backend`.

Example structure on server:

```
~/cabservice-backend/
  main.py
  requirements.txt
  app/
  .env.example   (optional, for reference)
```

Do **not** upload `venv/`, `.env`, or the Firebase JSON.

---

## 3. Create `.env` and Firebase key on cPanel

In the same folder as `main.py` (e.g. `~/cabservice-backend/`):

1. **Create `.env`** (File Manager or SSH):
   ```env
   FIREBASE_PROJECT_ID=cabservice-6c9ff
   GOOGLE_APPLICATION_CREDENTIALS=./cabservice-6c9ff-firebase-adminsdk-XXXXX.json
   ```
   Replace `XXXXX` with your actual filename if different.

2. **Upload the Firebase service account JSON** into that folder (same name as in `GOOGLE_APPLICATION_CREDENTIALS`).  
   Use File Manager or SCP. Restrict permissions if possible (e.g. `chmod 600 filename.json` via SSH).

---

## 4. Python app on cPanel

### If cPanel has “Setup Python App” (or “Application Manager”)

1. In cPanel go to **Setup Python App** / **Application Manager**.
2. **Create application:**
   - Python version: **3.10** or **3.11** (whatever is available).
   - Application root: `cabservice-backend` (or the folder where `main.py` is).
   - Application URL: e.g. `api.yourdomain.com` or `yourdomain.com/api`.
3. In “Configuration” or “Start command” set the startup command to:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   (Use the port cPanel assigns if it gives you one, e.g. `$PORT`.)
4. Install dependencies from the app’s virtualenv (Terminal or “Run pip” in the panel):
   ```bash
   cd ~/cabservice-backend
   source /path/to/venv/bin/activate   # path shown in Setup Python App
   pip install -r requirements.txt
   ```
5. Start / restart the application from the panel.

### If you only have SSH / Terminal

```bash
cd ~/cabservice-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Run in background (use your domain port or 8000)
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
```

Then use **Reverse Proxy** (next step) to send traffic from your domain to `http://127.0.0.1:8000`.

---

## 5. Reverse proxy (domain → FastAPI)

You want `https://api.yourdomain.com` (or similar) to hit the FastAPI app.

- **cPanel “Reverse Proxy” or “Application Manager”:** Add a reverse proxy for your subdomain/domain to `http://127.0.0.1:8000` (or the port your app uses).
- **Or `.htaccess`** in the **document root** of the domain/subdomain (e.g. `public_html` or `api.yourdomain.com`’s root). A sample is in `htaccess.example` – copy it to `.htaccess` and set the port if needed:

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://127.0.0.1:8000/$1 [P,L]
```

(See `htaccess.example` in the repo.)

---

## 6. Keep the app running (optional)

- If cPanel starts the app for you, use its “Restart” when you update code.
- If you started it with `nohup`, it stops when the server restarts. Use a simple loop or cron (e.g. “every 5 min check if process exists, start if not”) or ask your host for a way to run a long-lived process (e.g. systemd, supervisor).

---

## 7. After deploy

- Open `https://api.yourdomain.com/docs` to see Swagger.
- Call `POST /api/v1/auth/user/firebase-login` with a valid `id_token` to test login.
- Ensure Firebase Console has your production domain (e.g. `api.yourdomain.com`) allowed if you use Auth domain restrictions.

---

## Checklist

- [ ] Code pushed without `.env` and without Firebase JSON
- [ ] `.env` created on server with `FIREBASE_PROJECT_ID` and `GOOGLE_APPLICATION_CREDENTIALS`
- [ ] Firebase service account JSON uploaded to the app folder (and named as in `.env`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Uvicorn started (by cPanel or via `nohup`)
- [ ] Reverse proxy or .htaccess points domain to the app port
- [ ] HTTPS enabled for the API domain (cPanel SSL / Let’s Encrypt)
