import requests
import time
import threading
import queue
import json
import os
import random
from user_agent import generate_user_agent

# --- إعدادات ---
DEFAULT_THREAD_COUNT = 10  # عدد الـ Threads الافتراضي
PROXIES_FILE = "proxies.txt"
EMAILS_FILE = "email.txt"

# --- ترجمة النصوص ---
TEXTS = {
    "ar": {
        "welcome": """
███████╗███╗   ███╗ █████╗ ██╗██╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██║██║     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
█████╗  ██╔████╔██║███████║██║██║     ██║     ███████║█████╗  ██║     █████╔╝ 
██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
███████╗██║ ╚═╝ ██║██║  ██║██║███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
by @7snhacker
""",
        "choose_language": "اختر اللغة / Choose language (ar/en): ",
        "loaded_emails": "تم تحميل {} إيميل",
        "loaded_proxies": "تم تحميل {} بروكسي",
        "no_proxies": "لم يتم تحميل أي بروكسي",
        "choose_mode": "اختر الوضع (sleep/thread): ",
        "invalid_mode": "وضع غير صحيح. سيتم اختيار الوضع الافتراضي sleep.",
        "thread_count": "عدد الخيوط (threads) (افتراضي {}): ",
        "sleep_time": "حدد مدة الانتظار بين كل فحص (بالثواني): ",
        "linked": "[مرتبط] {} | المستخدم: {} | المتابعون: {} | يتابع: {}",
        "unlinked": "[غير مرتبط] {}",
        "rate_limited": "[محدود] {} - الرجاء الانتظار...",
        "error": "[خطأ] {} - حدث خطأ أثناء الفحص",
        "finished": "انتهى الفحص!",
        "file_not_found": "لم يتم العثور على ملف {}",
    },
    "en": {
        "welcome": """
███████╗███╗   ███╗ █████╗ ██╗██╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██║██║     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
█████╗  ██╔████╔██║███████║██║██║     ██║     ███████║█████╗  ██║     █████╔╝ 
██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
███████╗██║ ╚═╝ ██║██║  ██║██║███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
by @7snhacker
""",
        "choose_language": "اختر اللغة / Choose language (ar/en): ",
        "loaded_emails": "Loaded {} emails",
        "loaded_proxies": "Loaded {} proxies",
        "no_proxies": "No proxies loaded",
        "choose_mode": "Choose mode (sleep/thread): ",
        "invalid_mode": "Invalid mode, defaulting to sleep.",
        "thread_count": "Number of threads (default {}): ",
        "sleep_time": "Set sleep time between checks (seconds): ",
        "linked": "[Linked] {} | User: {} | Followers: {} | Following: {}",
        "unlinked": "[Unlinked] {}",
        "rate_limited": "[Rate Limited] {} - Please wait...",
        "error": "[Error] {} - Error occurred during check",
        "finished": "Checking finished!",
        "file_not_found": "File not found: {}",
    }
}

# --- تحميل البروكسيات ---
def load_proxies():
    proxies = []
    if os.path.exists(PROXIES_FILE):
        with open(PROXIES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                p = line.strip()
                if p:
                    proxies.append(p)
    return proxies

# --- تحميل الإيميلات ---
def load_emails(lang_texts):
    emails = []
    if os.path.exists(EMAILS_FILE):
        with open(EMAILS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                e = line.strip()
                if e:
                    emails.append(e)
    else:
        print(lang_texts["file_not_found"].format(EMAILS_FILE))
        exit(1)
    return emails

# --- اختيار بروكسي عشوائي ---
def get_random_proxy(proxies):
    if proxies:
        proxy = random.choice(proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    else:
        return None

# --- جلب بيانات حساب إنستغرام ---
def get_instagram_account_data(email_or_username, proxies):
    try:
        headers = {
            "User-Agent": generate_user_agent(),
            "X-CSRFToken": "missing"
        }
        proxy = get_random_proxy(proxies)

        url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
        data = {"email_or_username": email_or_username}
        r = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=15)

        if "We sent an" in r.text:
            profile_url = f"https://www.instagram.com/{email_or_username}/?__a=1&__d=dis"
            headers2 = {"User-Agent": generate_user_agent()}
            resp = requests.get(profile_url, headers=headers2, proxies=proxy, timeout=15)
            if resp.status_code == 200:
                try:
                    data_json = resp.json()
                    user = data_json.get("graphql", {}).get("user", {})
                    username = user.get("username", "N/A")
                    followers = user.get("edge_followed_by", {}).get("count", "N/A")
                    following = user.get("edge_follow", {}).get("count", "N/A")
                    return ("Linked", username, followers, following)
                except Exception:
                    return ("Linked", "N/A", "N/A", "N/A")
            else:
                return ("Linked", "N/A", "N/A", "N/A")

        elif "Please wait a few minutes before you try again." in r.text:
            return ("RateLimited", None, None, None)
        else:
            return ("Unlinked", None, None, None)
    except Exception:
        return ("Error", None, None, None)

# --- حفظ النتائج ---
def save_result(filename, line):
    with threading.Lock():
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")

# --- دالة العمل لكل إيميل ---
def worker(email_queue, proxies, lang_texts):
    while not email_queue.empty():
        email = email_queue.get()
        status, username, followers, following = get_instagram_account_data(email, proxies)

        if status == "Linked":
            print(lang_texts["linked"].format(email, username, followers, following))
            save_result("LinkedAvailable.txt", f"{email} | User: {username} | Followers: {followers} | Following: {following}")

        elif status == "Unlinked":
            print(lang_texts["unlinked"].format(email))
            save_result("Unlinked.txt", email)

        elif status == "RateLimited":
            print(lang_texts["rate_limited"].format(email))
            save_result("RateLimited.txt", email)
            time.sleep(10)

        else:
            print(lang_texts["error"].format(email))
            save_result("Errors.txt", email)

        email_queue.task_done()

# --- نسخة CLI رئيسية ---
def main():
    # اختيار اللغة
    lang = input(TEXTS["en"]["choose_language"]).strip().lower()
    if lang not in ["ar", "en"]:
        lang = "en"
    texts = TEXTS[lang]

    print(texts["welcome"])

    emails = load_emails(texts)
    proxies = load_proxies()

    print(texts["loaded_emails"].format(len(emails)))
    if proxies:
        print(texts["loaded_proxies"].format(len(proxies)))
    else:
        print(texts["no_proxies"])

    mode = input(texts["choose_mode"]).strip().lower()
    if mode not in ["sleep", "thread"]:
        print(texts["invalid_mode"])
        mode = "sleep"

    thread_count = 10
    if mode == "thread":
        try:
            user_input = input(texts["thread_count"].format(DEFAULT_THREAD_COUNT)).strip()
            if user_input:
                val = int(user_input)
                if val > 0:
                    thread_count = val
        except:
            pass

    if mode == "sleep":
        sleep_time =  float(input(texts["sleep_time"]))
        for email in emails:
            status, username, followers, following = get_instagram_account_data(email, proxies)
            if status == "Linked":
                print(texts["linked"].format(email, username, followers, following))
                save_result("LinkedAvailable.txt", f"{email} | User: {username} | Followers: {followers} | Following: {following}")
            elif status == "Unlinked":
                print(texts["unlinked"].format(email))
                save_result("Unlinked.txt", email)
            elif status == "RateLimited":
                print(texts["rate_limited"].format(email))
                save_result("RateLimited.txt", email)
                time.sleep(10)
            else:
                print(texts["error"].format(email))
                save_result("Errors.txt", email)
            time.sleep(sleep_time)

    else:  # thread mode
        email_queue = queue.Queue()
        for email in emails:
            email_queue.put(email)

        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=worker, args=(email_queue, proxies, texts))
            t.daemon = True
            t.start()
            threads.append(t)

        email_queue.join()
        print(texts["finished"])

if __name__ == "__main__":
    main()
