# Create GitHub repository and push this project

Follow these steps to put your code on GitHub.

---

## 1. Create the repository on GitHub

1. Open **https://github.com/new** in your browser (log in if needed).
2. Fill in:
   - **Repository name:** e.g. `cab-service-app` or `figma-export` (use a name you like).
   - **Description:** optional, e.g. `Cab Service – User, Driver & Admin app + backend API`.
   - **Visibility:** **Public**.
   - Do **not** check “Add a README”, “Add .gitignore”, or “Choose a license” (you already have files).
3. Click **Create repository**.

---

## 2. Initialize Git and push from your computer

Open Terminal and run these commands **one by one**. Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and the repo name you chose.

```bash
# Go to your project folder
cd "/Users/android/Desktop/my_projects/My App/figma_export"

# Initialize git (if not already done)
git init

# Add all files (respects .gitignore – .env and Firebase JSON won’t be added)
git add .
git status
# Check that .env and *firebase*.json do NOT appear. If they do, don’t commit – fix .gitignore first.

# First commit
git commit -m "Initial commit: Cab Service backend API + app + screens"

# Rename branch to main (if needed)
git branch -M main

# Add GitHub as remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

**Example:** If your username is `johndoe` and repo name is `cab-service-app`:

```bash
git remote add origin https://github.com/johndoe/cab-service-app.git
git push -u origin main
```

---

## 3. If GitHub asks for login

- **HTTPS:** GitHub will ask for username and **password**. Use a **Personal Access Token** as the password (Settings → Developer settings → Personal access tokens).
- **SSH:** If you use SSH keys:
  ```bash
  git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

---

## 4. After pushing

- Your code will be at `https://github.com/YOUR_USERNAME/YOUR_REPO`.
- `.env` and Firebase service account JSON are **not** in the repo (they are in `.gitignore`).
- On cPanel or any server, add `.env` and the Firebase JSON **manually** (see `backend/DEPLOY.md`).

---

## Quick checklist

- [ ] Repo created on GitHub (Public, no README/.gitignore added).
- [ ] `git init` and `git add .` in project folder.
- [ ] `git status` shows no `.env` or `*firebase*.json`.
- [ ] `git commit` and `git push -u origin main` done.
- [ ] Code visible on GitHub.
