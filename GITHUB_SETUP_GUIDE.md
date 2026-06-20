# CommitClock — Run Karne Aur GitHub Par Daalne Ka Poora Guide

Sab kuch is guide mein **bilkul free** hai. Kuch bhi paid nahi.

---

## Part 1 — App ko abhi apne computer par chalana

1. **Python install karo** (agar pehle se nahi hai): python.org/downloads se free download. Install karte waqt "Add Python to PATH" wala box zaroor tick karna.
2. Project folder (`CommitClock`) ko kahin save karo, phir terminal/command prompt waha kholo:
   ```
   cd CommitClock
   pip install -r requirements.txt
   python main.py
   ```
3. Ek window khulegi — wahi app hai. Bas itna.

---

## Part 2 — Phone par chalana (bina APK banaye, free)

Agar abhi sirf dekhna/test karna hai, **Pydroid 3** app use karo (Play Store par free):
1. Pydroid 3 install karo.
2. Usme "Pip" section se `kivy` install karo (free, andar hi ho jata hai).
3. CommitClock folder ko phone mein copy karo (USB ya Google Drive se).
4. Pydroid 3 mein `main.py` file kholo aur "Run" dabao.

Ye real APK nahi hai, lekin app ka pura experience dikha dega bina kuch banaye.

---

## Part 3 — Real .apk file banana (free, GitHub Actions se)

Tumhare paas Linux machine nahi hai — koi baat nahi. **GitHub khud free mein APK bana ke de sakta hai.** Bas project GitHub par hona chahiye (Part 4 dekho), aur is zip mein jo file di hai (`.github/workflows/build_apk.yml`) wo apne project mein daal do.

Phir jab bhi tum GitHub par code push karoge:
1. GitHub khud-ba-khud APK build karega (3-5 cents... nahi, **bilkul free** — public repo ke liye GitHub Actions free hai).
2. Tumhare repo ke "Actions" tab mein jaake build dekh sakte ho.
3. Build complete hone ke baad, usi page par neeche "Artifacts" mein `.apk` file download kar sakte ho.

Ye sab free hai, koi credit card nahi chahiye.

---

## Part 4 — GitHub par project daalna (step by step)

### Step 1: GitHub account banao
github.com par jaake free account banao (sign up).

### Step 2: Git install karo
git-scm.com se free download, install kar lo.

### Step 3: Naya repository banao
GitHub par "New repository" button dabao, naam do `CommitClock`, **Public** select karo (free Actions ke liye public hona zaroori hai), "Create" dabao. Koi README check mat karo abhi.

### Step 4: Apne project folder ko Git se jodo
Terminal mein CommitClock folder ke andar jaake:
```
git init
git add -A
git commit -m "Initial commit: CommitClock app"
git branch -M main
git remote add origin https://github.com/TUMHARA-USERNAME/CommitClock.git
git push -u origin main
```
(`TUMHARA-USERNAME` apne GitHub username se replace karna. Pehli baar push karte waqt GitHub login mangega — browser mein sign in kar dena, ya GitHub Desktop use karo agar terminal mushkil lage.)

Bas — ab tumhara poora project GitHub par hai, aur APK build wala workflow bhi khud-ba-khud chal jayega (Part 3).

---

## Part 5 — Automatic commit (har change khud commit ho)

Tumne pucha tha ke jo bhi project mein change karo wo khud commit ho jaye — iske 2 tareeke hain, dono free:

### Tareeka A: Asaan (one-click) — GitHub Desktop
1. desktop.github.com se **GitHub Desktop** free install karo.
2. Usme apna CommitClock folder add karo ("Add Existing Repository").
3. Jab bhi koi change karo, GitHub Desktop khud dikha dega "X files changed" — bas neeche "Commit" aur "Push" button dabana hota hai. Fully automatic nahi, lekin ek click jitna aasan.

### Tareeka B: Pura automatic — `auto_commit.py` script
Maine ek chota script bana diya hai (is zip mein) jo har 60 second mein check karta hai ke kuch change hua ya nahi, aur agar hua to khud commit + push kar deta hai. Bas isay terminal mein chala kar chhod do:
```
python auto_commit.py
```
Jab tak ye chal raha hai, har change apne aap GitHub par chala jayega. Band karne ke liye Ctrl+C dabao.

**Note:** Pehli baar `git push` karte waqt agar GitHub login/permission maange to wo ek baar manually karna padega (browser ya token ke zariye) — uske baad script khud sambhal lega.

---

## Free Checklist — kuch bhi paid nahi
- Python — free
- Kivy — free
- Git — free
- GitHub account + public repo — free
- GitHub Actions (APK build) — free for public repos
- Pydroid 3 — free
- GitHub Desktop — free

Sab kuch bina ek rupaya kharch kiye ho sakta hai.
