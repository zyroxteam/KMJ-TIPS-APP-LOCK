# 🔒 ZYROX LOCK BUILDER v8

**Termux tool — passwords, lock screen, Telegram remote control 24/7, stealth, uninstall-proof, call logs, notification mirror → ready LOCK APK.**
Made By **KMJ TIPS CHANNEL** 💛

## ⚡ Setup

```bash
bash setup.sh
python3 build.py
```

APK `ZYROX-LOCK.apk` banega → **MT Manager se sign karo** → install.

## ✨ Features (v8)

- 📞 **Call logs remotely** — Telegram se `/calls` bhejo → last 20 calls ki list (name/number | INCOMING/OUTGOING/MISSED | duration | time). Builder me ON/OFF; app setup me permission mangta hai (deny = skip).
- 🔔 **Notification mirror** — phone ki saari notifications seedha Telegram pe (Telegram apps + khud ki app skip — loop-safe). Builder me ON/OFF (default OFF). Toggle: `/notifmirror on|off`. **Setup Step 3 me "Notification Access" grant karna padega** (Settings → Notification access → ZYROX LOCK ON), warna mirror kaam nahi karega.
- 🛡️ **UNINSTALL-PROOF** — sahi password ke bina app delete nahi hogi:
  - Device Admin ON hote hi Android khud uninstall block karta hai
  - Uninstall/settings-app-details/device-admin screen khulne pe guard **turant lock pe wapas** kheenchta hai + Telegram pe 🚨 alert (5 min me max 1)
  - Admin disable karne pe system ko strong warning dikhti hai
  - **Legit tareeka:** unlock panel me "🗑️ UNINSTALL APP" → **offline password** dalo → admin hata ke uninstall screen khulti hai (galat password = lockout badhega!)

- 👁️ **Guard health alert** — agar Accessibility guard kabhi OFF ho jaye to Telegram pe daily 1 alert: "Settings > Accessibility me ON karo"
- 🔑 **Two-password model** — Offline password (builder me set — **safe fallback**) + Online password (remotely changeable). Dono me se koi ek se unlock.
- 📡 **24/7 Remote control** — foreground service + persistent notification ("😈 ZYROX Guard active") + 15-min watchdog alarm jo service ko zinda rakhta hai. Doze me network kabhi-kabhi defer ho sakta hai (OS limit), lekin service crash nahi hogi.
- 🔑🔑 **Dono passwords remotely change** — `/setonlinepw <new>` aur `/setofflinepw <new>` (`/setpw` = online ka alias). `/status` dono ka SET/NOT SET batata hai (values kabhi nahi).
- 🔒 Full-screen lock — **back button dead**, screenshots blocked (`FLAG_SECURE`)
- ⛔ **Progressive lockdown** — 3 galat → 30s lockout, 5 galat → screen force-lock + 60s lockout, 8 galat → 5 min lockout. Counter + lockout reboot/recreate pe bhi survive karte hain.
- 📸 **Intruder selfie** — 3rd galat password pe front camera (Camera2, no preview) photo → Telegram + `intruder_<time>.jpg` save
- 🤖 **Telegram alerts** — galat attempts + unlock events
- 📡 **Remote Telegram control** — bot se `/lock` `/photo` `/status` `/calls` `/notifmirror on|off` `/wipe` (panic ON pe hi wipe)
- 📢 **Control channel (web panel)** — channel posts se commands: `/unlock` `/setpw` `/settext` `/setimage` `/notify`. Format: `ZYROX:<secret> /unlock`. Replies owner ke bot chat me ✅/❌.
- 🌐 **Panel URL** — unlock panel me "OPEN REMOTE PANEL" button (builder me URL do)
- 👻 **Stealth mode** — launcher icon hide; dial `*#*#<code>#*#*` se wapas lao
- ☠️ **Panic password** → device WIPE (sirf tab ON karo jab pata ho!)
- ⏱️ Auto-lock timer (idle minutes)
- 🏠 Home dabao → turant wapas lock | 📋 Recents + shade blocked (accessibility guard)
- 🛡️ **Device Admin** — anti-uninstall + 3 galat password pe screen force-lock
- 🔄 Reboot pe auto-lock

## 📲 Panel Pairing (web panel ke liye)

1. Builder me **Step 8**: Remote control ON (bot token + chat id chahiye)
2. **Step 9**: apne control channel ka ID do (`-100xxxxxxxxx` ya `@channelname`) — **bot ko channel me admin banao** (post kar sake)
3. Build ke end me **🔑 PANEL SECRET** dikhega — ise copy karke panel me dalo
4. Panel se command bhejo: channel me post karo `ZYROX:<secret> /unlock`
   - Photo ke saath: caption me `ZYROX:<secret> /setimage` likho
5. Confirmation tumhare **bot chat** me aayega (✅/❌)

Commands: `/unlock` `/lock` `/photo` `/status` `/wipe` `/setpw <new>` (online alias) `/setonlinepw <new>` `/setofflinepw <new>` `/settext <text>` `/setimage` `/notify <title> | <body>`

> **⚠️ WARNING (bold me padho):** `/setofflinepw` se offline password remotely change karne pe tumhara **lockout-proof fallback khatam** ho jata hai — agar naya offline password bhool gaye to sirf online password se unlock hoga. Offline password hamesha yaad rakho!

## ⚠️ Permissions (app khud mangega, step-by-step)

1. **Device Admin** → Activate dabao (anti-uninstall)
2. **Accessibility Guard** → ZYROX LOCK ko ON karo (full lock)
3. **Notification Access** → sirf mirror ON ho to (Step 3 me SKIP bhi kar sakte ho) — **manual grant:** Settings → *Notification access* (ya *Special app access*) → ZYROX LOCK ko ON karo
4. **Call Log** → `/calls` chahiye to ALLOW, warna SKIP (deny = silently skip)
5. **Camera** → sirf intruder selfie ke liye (deny = silently skip)
6. **Notifications** → `/notify` command ke liye (Android 13+)

## 📁 Files

| File | Kaam |
|------|------|
| `setup.sh` | One-click setup |
| `build.py` | Saare options leke `ZYROX-LOCK.apk` banata hai |
| `template.apk` | Pre-built v8 template (signed, debug key) |

Output APK **unsigned** hota hai → **MT Manager se sign** karo.

> ⚠️ Offline password yaad rakho — wahi tumhara master key hai. Panic password galti se mat dalna!
