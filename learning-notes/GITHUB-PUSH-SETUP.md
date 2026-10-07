# GitHub Push — 403 Fix (awaisahmadfg)

## Problem kya thi?

1. **HTTPS `git push`** → `403 Permission denied to awaisahmadfg`  
   - GitHub password field mein **account password** kaam nahi karta.  
   - **Personal Access Token (PAT)** chahiye.  
   - **Fine-grained token** bina **repository select** + **Contents: Read and write** ke → push fail.

2. **Is laptop par SSH key** GitHub user **`devmustansar`** se linked hai (`ssh -T git@github.com`).  
   - SSH se push **`devmustansar`** ke rights se hota hai, **`awaisahmadfg`** ke repo par tabhi chalega jab wo collaborator ho.  
   - Is liye **`awaisahmadfg`** repo ke liye HTTPS + PAT (awaisahmadfg account ka) ya **awaisahmadfg** par nayi SSH key add karni hogi.

3. **Public repo par `curl` → 200** token test **nahi** hai — bina auth bhi 200 aa sakta hai.

## Solution (recommended): Classic PAT + HTTPS push

1. Login GitHub as **awaisahmadfg** (browser).  
2. **Settings → Developer settings → Personal access tokens → Tokens (classic)**  
3. **Generate new token (classic)** → scope **`repo`** ✅  
4. Token copy (`ghp_...`).

Verify token:

```bash
curl -s -H "Authorization: Bearer ghp_YOUR_TOKEN" https://api.github.com/user | grep login
# "login": "awaisahmadfg" hona chahiye
```

Push (password prompt par **token** paste):

```bash
cd ~/Documents/ML-Training-2026
git config user.name "awaisahmadfg"
git config user.email "awaisahmadfg@gmail.com"
git push origin main
# Username: awaisahmadfg
# Password: <paste ghp_ token, not GitHub password>
```

Optional — credentials save (local):

```bash
git config --global credential.helper store
# phir ek dafa push + token → ~/.git-credentials mein save
```

## Fine-grained token (agar classic na use karo)

- Repository: **ML-Training-2026** (select)  
- **Contents: Read and write** (Read only = 403 on push)

## Alternative: SSH as awaisahmadfg

1. Nayi key: `ssh-keygen -t ed25519 -C "awaisahmadfg@gmail.com" -f ~/.ssh/id_ed25519_awais`  
2. Public key **awaisahmadfg** GitHub → Settings → SSH keys  
3. `~/.ssh/config` host alias `github-awais`  
4. `git remote set-url origin git@github-awais:awaisahmadfg/ML-Training-2026.git`

## Local commits ready to push (Oct 2026)

```text
c4f2e2c — learning-notes guide + README
5da5814 — projects/phase-a structure
```

```bash
git log origin/main..HEAD --oneline
git push origin main
```

**Security:** Token chat/terminal history mein paste mat karo; leak ho to token **revoke** karo.
