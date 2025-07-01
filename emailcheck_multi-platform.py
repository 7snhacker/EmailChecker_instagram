#!/usr/bin/env python3
"""
Email & Platform Checker
------------------------
Generate and check emails for existence and platform account association
across Gmail, Yahoo, Outlook, TikTok, Instagram, Twitter, Snapchat, PayPal, Netflix, and more.

- Multilingual support (Arabic, English)
- Multi-threaded and proxy support for speed and reliability
- Professional output and CSV export

Requirements:
    pip install dnspython requests

Author: 7snhacker
License: MIT
"""

import random
import threading
import time
import smtplib
import dns.resolver
import requests
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import re
import os

# =========================
# CONFIGURATION & PLATFORM API ENDPOINTS
# =========================
PLATFORMS = [
    {"name_en": "tiktok", "name_ar": "تيك توك", "checker": "check_tiktok"},
    {"name_en": "instagram", "name_ar": "انستجرام", "checker": "check_instagram"},
    {"name_en": "twitter", "name_ar": "تويتر", "checker": "check_twitter"},
    {"name_en": "snapchat", "name_ar": "سناب شات", "checker": "check_snapchat"},
    {"name_en": "paypal", "name_ar": "باي بال", "checker": "check_paypal"},
    {"name_en": "netflix", "name_ar": "نتفلكس", "checker": "check_netflix"},
    {"name_en": "microsoft", "name_ar": "مايكروسوفت", "checker": "check_microsoft"},
    {"name_en": "yahoo", "name_ar": "ياهو", "checker": "check_yahoo"},
    {"name_en": "gmail", "name_ar": "جيميل", "checker": "check_gmail"},
]
DEFAULT_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
]
PROXY_LIST = [
    "http://51.79.50.31:9300",
    "http://154.236.189.32:1981",
    "http://38.154.227.167:80",
]
LANGUAGES = {
    "ar": {
        "banner": "🔎 أداة فحص الإيميلات والمنصات 🔎",
        "developed_by": "المطور: 7snhacker | نسخة احترافية",
        "input_domains": "أدخل الدومينات مفصولة بفاصلة (أو اضغط Enter للإفتراضي): ",
        "input_count": "كم عدد الإيميلات؟ (افتراضي 10): ",
        "mode_choice": "اختر الوضع: 1-تسلسلي (آمن) 2-متعدد (سريع) (افتراضي 2): ",
        "sleep_time": "مدة الانتظار بين الطلبات (ثواني، الافتراضي 0.3): ",
        "jitter": "المدة العشوائية الإضافية (افتراضي 0.5): ",
        "max_threads": "عدد الثريدات الأقصى (افتراضي 16): ",
        "use_proxies": "استخدام بروكسيات للفحص؟ (y/N): ",
        "emails_to_check": "الإيميلات التي سيتم فحصها:",
        "checking": "جاري الفحص...",
        "finished": "تم الانتهاء. النتائج:",
        "save_csv": "حفظ النتائج كملف CSV؟ (y/N): ",
        "csv_saved": "تم حفظ النتائج في platform_scan_results.csv",
        "done": "انتهى الفحص. شكراً لاستخدام الأداة 👋",
        "email": "البريد الإلكتروني",
        "availability": "الحالة",
    },
    "en": {
        "banner": "🔎 Email & Platform Checker 🔎",
        "developed_by": "Developed by: 7snhacker | Pro Edition",
        "input_domains": "Enter domains separated by comma (default: gmail.com,yahoo.com,hotmail.com,outlook.com): ",
        "input_count": "How many emails to generate? (default 10): ",
        "mode_choice": "Select mode: 1-Serial (safe) 2-Threaded (fast) (default 2): ",
        "sleep_time": "Base sleep between checks in seconds (default 0.3): ",
        "jitter": "Max random jitter (default 0.5): ",
        "max_threads": "Max threads (default 16): ",
        "use_proxies": "Use proxies for scans? (y/N): ",
        "emails_to_check": "Emails to check:",
        "checking": "Checking...",
        "finished": "Finished. Results:",
        "save_csv": "Save results to CSV file? (y/N): ",
        "csv_saved": "Results saved to platform_scan_results.csv",
        "done": "Done. Thank you for using the tool 👋",
        "email": "Email",
        "availability": "Status",
    }
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_language():
    print("1- العربية (Arabic)\n2- English")
    lang_input = input("اختر اللغة | Select language: ").strip()
    return "ar" if lang_input == "1" else "en"

def banner(lang):
    print("\033[1;35m" + "="*70)
    print(f"{lang['banner']:^70}")
    print("="*70 + "\033[0m")
    print(f"\033[1;36m{lang['developed_by']}\033[0m\n")

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def is_syntax_valid(email):
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(regex, email) is not None

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return bool(answers)
    except Exception:
        return False

def generate_emails(domain_list, count):
    names = [
        "ahmed", "mohamed", "sara", "noor", "omar", "jana", "ali", "lina",
        "khaled", "reem", "samir", "yasmin", "fadi", "malak", "hassan", "eman",
        "ammar", "salma", "nour", "abdullah", "fatima", "dina", "tariq", "hamza",
        "ibrahim", "zain", "layla", "maryam", "osama", "huda", "adel", "sofia"
    ]
    emails = set()
    while len(emails) < count:
        name = random.choice(names)
        number = random.randint(100, 9999)
        domain = random.choice(domain_list)
        safe_name = "".join([c for c in name if c.isalnum()])
        email = f"{safe_name}{number}@{domain}"
        emails.add(email)
    return list(emails)

def get_proxy():
    return random.choice(PROXY_LIST)

def robust_request(method, url, use_proxy=False, max_retries=3, sleep_range=(0.8, 1.7), **kwargs):
    for attempt in range(max_retries):
        try:
            s = requests.Session()
            if use_proxy:
                proxy = get_proxy()
                s.proxies.update({"http": proxy, "https": proxy})
            resp = getattr(s, method)(url, timeout=10, **kwargs)
            return resp
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(random.uniform(*sleep_range))
            continue
    return None

# ================================
# PLATFORM CHECKERS (using real public endpoints as much as possible)
# ================================
def check_gmail(email, use_proxy=False):
    local_part = email.split('@')[0]
    url = "https://accounts.google.com/_/signup/webusernameavailability"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    data = f"flowEntry=SignUp&Email={local_part}"
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and resp.status_code == 200 and '"gf.sua"' in resp.text:
        pattern_true = f'"{local_part}@gmail.com",1'
        pattern_false = f'"{local_part}@gmail.com",0'
        if pattern_true in resp.text:
            return "✅ Exists"
        elif pattern_false in resp.text:
            return "❌ Not Exists"
    return "❌ Not Exists"

def check_yahoo(email, use_proxy=False):
    url = "https://login.yahoo.com/account/module/create?validateField=yid"
    headers = {
        'User-Agent': get_random_user_agent(),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://login.yahoo.com',
        'Referer': 'https://login.yahoo.com/account/create',
    }
    data = f"specId=yidregsimplified&yid={email.split('@')[0]}&yidType=login&done=https://mail.yahoo.com/"
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and resp.status_code == 200:
        if '"IDENTIFIER_EXISTS"' in resp.text:
            return "✅ Exists"
        if '"OK"' in resp.text:
            return "❌ Not Exists"
    return "❌ Not Exists"

def check_microsoft(email, use_proxy=False):
    url = "https://login.live.com/GetUserExistence.srf"
    headers = {
        'User-Agent': get_random_user_agent(),
        'Content-Type': 'application/json; charset=utf-8',
    }
    payload = {"username": email, "uaid": "random"}
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, json=payload)
    if resp and resp.ok and 'IfExistsResult' in resp.text:
        if '"IfExistsResult":0' in resp.text:
            return "✅ Exists"
        elif '"IfExistsResult":1' in resp.text:
            return "❌ Not Exists"
    return "❌ Not Exists"

def check_tiktok(email, use_proxy=False):
    url = "https://www.tiktok.com/passport/web/user/check_email_available/"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Referer": "https://www.tiktok.com/signup",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = f"email={email}"
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and resp.status_code == 200:
        if '"email_status":5' in resp.text or '"email_status":1' in resp.text:
            return "✅ Exists"
        elif '"email_status":2' in resp.text or '"email_status":3' in resp.text:
            return "❌ Not Exists"
    return "❌ Not Exists"

def check_instagram(email, use_proxy=False):
    url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
    headers = {
        "User-Agent": get_random_user_agent(),
        "X-CSRFToken": "missing",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/password/reset/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }
    data = f"email_or_username={email}&recaptcha_challenge_field="
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and resp.status_code in (200, 400):
        if '"status":"ok"' in resp.text or "We sent an email" in resp.text:
            return "✅ Exists"
        elif "No users found" in resp.text or "not associated with an account" in resp.text or "No account found" in resp.text:
            return "❌ Not Exists"
    return "❌ Not Exists"

def check_twitter(email, use_proxy=False):
    url = "https://api.twitter.com/i/account/pw_reset/send"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded",
        "x-twitter-active-user": "yes"
    }
    data = f"account_identifier={email}"
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and "instructions" in resp.text:
        return "✅ Exists"
    elif resp and ("not found" in resp.text or "not associated" in resp.text or "does not exist" in resp.text):
        return "❌ Not Exists"
    return "❌ Not Exists"

def check_snapchat(email, use_proxy=False):
    url = "https://accounts.snapchat.com/accounts/password_reset_request"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = f"email={email}"
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and "We have sent a password reset link" in resp.text:
        return "✅ Exists"
    elif resp and ("is not registered" in resp.text or "does not exist" in resp.text):
        return "❌ Not Exists"
    return "❌ Not Exists"

def check_paypal(email, use_proxy=False):
    url = "https://www.paypal.com/authflow/password-recovery/?country.x=US&locale.x=en_US"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "en-US,en;q=0.9",
    }
    data = {"email": email}
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and ("We couldn't find your email" in resp.text or "can't find your email" in resp.text):
        return "❌ Not Exists"
    elif resp and ("We've sent a verification" in resp.text or "send a verification" in resp.text):
        return "✅ Exists"
    elif resp and resp.status_code == 200 and "reset your password" in resp.text:
        return "✅ Exists"
    else:
        return "❌ Not Exists"

def check_netflix(email, use_proxy=False):
    url = "https://www.netflix.com/LoginHelp"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"email": email, "action": "emailReset"}
    resp = robust_request("post", url, use_proxy=use_proxy, headers=headers, data=data)
    if resp and "Sorry, we can't find an account" in resp.text:
        return "❌ Not Exists"
    elif resp and ("We’ve sent you an email" in resp.text or "We've sent you an email" in resp.text):
        return "✅ Exists"
    return "❌ Not Exists"

PLATFORM_FUNCTION_MAP = {
    "check_gmail": check_gmail,
    "check_yahoo": check_yahoo,
    "check_microsoft": check_microsoft,
    "check_tiktok": check_tiktok,
    "check_instagram": check_instagram,
    "check_twitter": check_twitter,
    "check_snapchat": check_snapchat,
    "check_paypal": check_paypal,
    "check_netflix": check_netflix
}

# ================================
# GENERIC EMAIL CHECK (syntax, MX, fallback SMTP)
# ================================
def smtp_check(email):
    domain = email.split('@')[1]
    from_address = f"test{random.randint(10000,99999)}@{domain}"
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)
    except Exception:
        return "❌ Not Exists"
    try:
        socket.setdefaulttimeout(7)
        server = smtplib.SMTP(timeout=7)
        server.connect(mx_host)
        server.helo("testdomain.com")
        server.mail(from_address)
        try:
            result = server.rcpt(email)
            code = result[0] if isinstance(result, tuple) and len(result) > 0 else None
        except Exception:
            code = None
        server.quit()
        if code in (250, 251):
            return "✅ Exists"
        elif code in (550, 551, 553):
            return "❌ Not Exists"
        else:
            return "❌ Not Exists"
    except Exception:
        return "❌ Not Exists"

def check_email_availability(email, use_proxy=False):
    if not is_syntax_valid(email):
        return "❌ Invalid Syntax"
    domain = email.split('@')[1].lower()
    if not has_mx_record(domain):
        return "❌ No MX Record"
    for plat in ["gmail", "yahoo", "microsoft"]:
        if plat in domain:
            return PLATFORM_FUNCTION_MAP[f"check_{plat}"](email, use_proxy)
    return smtp_check(email)

def color_status(status):
    if "✅" in status:
        return f"\033[92m{status}\033[0m"
    elif "❌" in status:
        return f"\033[91m{status}\033[0m"
    else:
        return status

class Throttle:
    def __init__(self, base_sleep=0.3, jitter=0.5):
        self.base_sleep = base_sleep
        self.jitter = jitter
    def sleep(self):
        t = self.base_sleep + random.uniform(0, self.jitter)
        time.sleep(t)

def print_professional_table(results, platforms, lang, lang_key):
    headers = [
        lang[lang_key]['email'],
        lang[lang_key]['availability']
    ] + [p['name_ar'] if lang_key == "ar" else p['name_en'] for p in platforms]
    col_widths = [max(len(headers[i]), max((len(str(row.get(h, ""))) for row in results), default=0)) for i, h in enumerate(headers)]
    for i, p in enumerate(platforms, 2):
        for r in results:
            val = r.get(f"{p['name_en']}_platform", "")
            col_widths[i] = max(col_widths[i], len(val))
    sep = " | "
    head = sep.join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print("\033[1;34m" + "=" * len(head))
    print(head)
    print("=" * len(head) + "\033[0m")
    for r in results:
        row = [
            r["email"].ljust(col_widths[0]),
            color_status(r["availability"]).ljust(col_widths[1])
        ] + [color_status(r.get(f"{p['name_en']}_platform", "")).ljust(col_widths[i+2]) for i, p in enumerate(platforms)]
        print(sep.join(row))
    print("\033[1;34m" + "=" * len(head) + "\033[0m")

def scan_worker(email, platforms, throttle, results, lock, idx, total, max_len, lang, lang_key, use_proxy):
    avail = check_email_availability(email, use_proxy=use_proxy)
    plats = {}
    for p in platforms:
        plats[p["name_en"]] = PLATFORM_FUNCTION_MAP[p["checker"]](email, use_proxy=use_proxy)
    with lock:
        results.append({
            "email": email,
            "availability": avail,
            **{f"{p['name_en']}_platform": plats[p['name_en']] for p in platforms}
        })
    throttle.sleep()

def check_emails_threaded(emails, platforms, base_sleep=0.3, jitter=0.5, max_workers=16, lang=None, lang_key="en", use_proxy=False):
    results = []
    lock = threading.Lock()
    throttle = Throttle(base_sleep=base_sleep, jitter=jitter)
    max_len = max([len(e) for e in emails]) + 2
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for idx, email in enumerate(emails, 1):
            futures.append(
                executor.submit(scan_worker, email, platforms, throttle, results, lock, idx, len(emails), max_len, lang, lang_key, use_proxy)
            )
        for _ in as_completed(futures):
            pass
    return results

def check_emails_serial(emails, platforms, base_sleep=0.5, jitter=0.5, lang=None, lang_key="en", use_proxy=False):
    results = []
    lock = threading.Lock()
    throttle = Throttle(base_sleep=base_sleep, jitter=jitter)
    max_len = max([len(e) for e in emails]) + 2
    for idx, email in enumerate(emails, 1):
        scan_worker(email, platforms, throttle, results, lock, idx, len(emails), max_len, lang, lang_key, use_proxy)
    return results

def save_results_csv(results, platforms, filename="platform_scan_results.csv"):
    fieldnames = ["email", "availability"] + [f"{p['name_en']}_platform" for p in platforms]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def main():
    clear()
    lang_key = choose_language()
    lang = LANGUAGES[lang_key]
    banner(lang)
    domains = input(f"\033[1;36m{lang['input_domains']}\033[0m").strip()
    if not domains:
        domain_list = DEFAULT_DOMAINS
    else:
        domain_list = [d.strip() for d in domains.split(",") if d.strip()]
    try:
        count = int(input(f"\033[1;36m{lang['input_count']}\033[0m").strip() or "10")
    except Exception:
        count = 10
    print(f"\033[1;33m{lang['mode_choice']}\033[0m")
    mode = input().strip()
    use_threads = (mode != "1")
    try:
        base_sleep = float(input(f"\033[1;36m{lang['sleep_time']}\033[0m").strip() or "0.3")
    except:
        base_sleep = 0.3
    try:
        jitter = float(input(f"\033[1;36m{lang['jitter']}\033[0m").strip() or "0.5")
    except:
        jitter = 0.5
    try:
        max_workers = int(input(f"\033[1;36m{lang['max_threads']}\033[0m").strip() or "16")
    except:
        max_workers = 16
    use_proxy = False
    use_proxy_input = input(f"\033[1;36m{lang['use_proxies']}\033[0m").strip().lower()
    if use_proxy_input in ["y", "yes", "نعم"]:
        use_proxy = True
    platforms = PLATFORMS
    emails = generate_emails(domain_list, count)
    print(f"\n\033[1;37m{lang['emails_to_check']}\033[0m")
    for e in emails:
        print(f" - \033[96m{e}\033[0m")
    print(f"\n\033[1;33m{lang['checking']}\n\033[0m")
    if use_threads:
        results = check_emails_threaded(emails, platforms, base_sleep=base_sleep, jitter=jitter, max_workers=max_workers, lang=lang, lang_key=lang_key, use_proxy=use_proxy)
    else:
        results = check_emails_serial(emails, platforms, base_sleep=base_sleep, jitter=jitter, lang=lang, lang_key=lang_key, use_proxy=use_proxy)
    print(f"\n\033[1;35m{lang['finished']}\033[0m")
    print_professional_table(results, platforms, LANGUAGES, lang_key)
    save = input(f"\033[1;36m{lang['save_csv']}\033[0m").strip().lower()
    if save == "y":
        save_results_csv(results, platforms)
        print(f"\033[92m{lang['csv_saved']}\033[0m")
    print(f"\033[1;32m{lang['done']}\033[0m\n")

if __name__ == "__main__":
    main()
