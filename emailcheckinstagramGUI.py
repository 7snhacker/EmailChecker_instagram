import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import queue
import requests
import time
import random
import os
from user_agent import generate_user_agent

DEFAULT_THREAD_COUNT = 10
PROXIES_FILE = "proxies.txt"

TEXTS = {
    "ar": {
        "title": "أداة فحص إيميلات إنستغرام",
        "select_file": "اختيار ملف الإيميلات",
        "load_proxies": "تحميل البروكسيات",
        "start": "ابدأ الفحص",
        "mode_label": "اختر الوضع:",
        "mode_sleep": "نوم (Sleep)",
        "mode_thread": "خيوط (Threads)",
        "thread_count": "عدد الخيوط:",
        "sleep_time": "مدة الانتظار (ثواني):",
        "language": "اللغة:",
        "log": "سجل الأحداث:",
        "file_not_found": "لم يتم العثور على الملف.",
        "select_email_file": "يرجى اختيار ملف الإيميلات أولاً.",
        "loading_emails": "جار تحميل الإيميلات...",
        "loading_proxies": "جار تحميل البروكسيات...",
        "loaded_emails": "تم تحميل {} إيميل.",
        "loaded_proxies": "تم تحميل {} بروكسي.",
        "no_proxies": "لم يتم تحميل أي بروكسي، سيتم الفحص بدون بروكسي.",
        "error": "حدث خطأ أثناء الفحص.",
        "finished": "انتهى الفحص!",
        "rate_limited": "تم الحظر مؤقتاً، يرجى الانتظار...",
        "linked": "[مرتبط] {} | المستخدم: {} | المتابعون: {} | يتابع: {}",
        "unlinked": "[غير مرتبط] {}",
    },
    "en": {
        "title": "Instagram Email Checker Tool",
        "select_file": "Select Email File",
        "load_proxies": "Load Proxies",
        "start": "Start Checking",
        "mode_label": "Choose Mode:",
        "mode_sleep": "Sleep",
        "mode_thread": "Threads",
        "thread_count": "Thread Count:",
        "sleep_time": "Sleep Time (seconds):",
        "language": "Language:",
        "log": "Log:",
        "file_not_found": "File not found.",
        "select_email_file": "Please select the email file first.",
        "loading_emails": "Loading emails...",
        "loading_proxies": "Loading proxies...",
        "loaded_emails": "Loaded {} emails.",
        "loaded_proxies": "Loaded {} proxies.",
        "no_proxies": "No proxies loaded, will check without proxies.",
        "error": "An error occurred during checking.",
        "finished": "Checking finished!",
        "rate_limited": "Rate limited, please wait...",
        "linked": "[Linked] {} | User: {} | Followers: {} | Following: {}",
        "unlinked": "[Unlinked] {}",
    }
}

class InstagramCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Email Checker")
        self.lang = "en"
        self.texts = TEXTS[self.lang]
        self.emails = []
        self.proxies = []
        self.queue = queue.Queue()
        self.stop_flag = False

        self.build_gui()
        self.load_proxies()

    def build_gui(self):
        # Language selection
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(padx=10, pady=5, anchor="w")

        tk.Label(lang_frame, text=TEXTS["en"]["language"]).pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="en")
        lang_menu = tk.OptionMenu(lang_frame, self.lang_var, "en", "ar", command=self.change_language)
        lang_menu.pack(side=tk.LEFT)

        # File selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(padx=10, pady=5, fill="x")

        self.file_label = tk.Label(file_frame, text=self.texts["select_file"])
        self.file_label.pack(side=tk.LEFT)

        btn_browse = tk.Button(file_frame, text=self.texts["select_file"], command=self.select_email_file)
        btn_browse.pack(side=tk.RIGHT)

        # Mode selection
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(mode_frame, text=self.texts["mode_label"]).pack(side=tk.LEFT)

        self.mode_var = tk.StringVar(value="sleep")
        rb_sleep = tk.Radiobutton(mode_frame, text=self.texts["mode_sleep"], variable=self.mode_var, value="sleep", command=self.toggle_mode)
        rb_sleep.pack(side=tk.LEFT, padx=5)
        rb_thread = tk.Radiobutton(mode_frame, text=self.texts["mode_thread"], variable=self.mode_var, value="thread", command=self.toggle_mode)
        rb_thread.pack(side=tk.LEFT, padx=5)

        # Thread count and sleep time
        options_frame = tk.Frame(self.root)
        options_frame.pack(padx=10, pady=5, fill="x")

        self.thread_label = tk.Label(options_frame, text=self.texts["thread_count"])
        self.thread_label.pack(side=tk.LEFT)
        self.thread_entry = tk.Entry(options_frame, width=5)
        self.thread_entry.pack(side=tk.LEFT)
        self.thread_entry.insert(0, str(DEFAULT_THREAD_COUNT))

        self.sleep_label = tk.Label(options_frame, text=self.texts["sleep_time"])
        self.sleep_label.pack(side=tk.LEFT, padx=(20,5))
        self.sleep_entry = tk.Entry(options_frame, width=5)
        self.sleep_entry.pack(side=tk.LEFT)
        self.sleep_entry.insert(0, "1")

        # Start button
        start_frame = tk.Frame(self.root)
        start_frame.pack(padx=10, pady=10, fill="x")

        self.start_btn = tk.Button(start_frame, text=self.texts["start"], command=self.start_checking)
        self.start_btn.pack()

        # Log output
        log_frame = tk.Frame(self.root)
        log_frame.pack(padx=10, pady=5, fill="both", expand=True)

        tk.Label(log_frame, text=self.texts["log"]).pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill="both", expand=True)

        self.toggle_mode()

    def change_language(self, choice):
        self.lang = choice
        self.texts = TEXTS[self.lang]
        self.update_texts()

    def update_texts(self):
        self.root.title(self.texts["title"])
        self.file_label.config(text=self.texts["select_file"])
        self.thread_label.config(text=self.texts["thread_count"])
        self.sleep_label.config(text=self.texts["sleep_time"])
        self.start_btn.config(text=self.texts["start"])
        # Update mode radio buttons text
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Radiobutton):
                        val = widget.cget("value")
                        if val == "sleep":
                            widget.config(text=self.texts["mode_sleep"])
                        elif val == "thread":
                            widget.config(text=self.texts["mode_thread"])

    def toggle_mode(self):
        if self.mode_var.get() == "thread":
            self.thread_entry.config(state="normal")
            self.sleep_entry.config(state="disabled")
        else:
            self.thread_entry.config(state="disabled")
            self.sleep_entry.config(state="normal")

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def select_email_file(self):
        file_path = filedialog.askopenfilename(title=self.texts["select_file"], filetypes=[("Text files","*.txt")])
        if file_path:
            self.email_file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.log(self.texts["loading_emails"])
            self.emails = []
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        email = line.strip()
                        if email:
                            self.emails.append(email)
                self.log(self.texts["loaded_emails"].format(len(self.emails)))
            except Exception as e:
                messagebox.showerror(self.texts["file_not_found"], str(e))

    def load_proxies(self):
        self.proxies = []
        if os.path.exists(PROXIES_FILE):
            self.log(self.texts["loading_proxies"])
            try:
                with open(PROXIES_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        p = line.strip()
                        if p:
                            self.proxies.append(p)
                self.log(self.texts["loaded_proxies"].format(len(self.proxies)))
            except:
                self.log(self.texts["no_proxies"])
        else:
            self.log(self.texts["no_proxies"])

    def get_random_proxy(self):
        if self.proxies:
            proxy = random.choice(self.proxies)
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        return None

    def get_instagram_account_data(self, email_or_username):
        try:
            headers = {
                "User-Agent": generate_user_agent(),
                "X-CSRFToken": "missing"
            }
            proxy = self.get_random_proxy()
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

    def save_result(self, filename, line):
        with threading.Lock():
            with open(filename, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def worker(self):
        while not self.queue.empty() and not self.stop_flag:
            email = self.queue.get()
            status, username, followers, following = self.get_instagram_account_data(email)

            if status == "Linked":
                msg = self.texts["linked"].format(email, username, followers, following)
                self.log(msg)
                self.save_result("LinkedAvailable.txt", f"{email} | User: {username} | Followers: {followers} | Following: {following}")

            elif status == "Unlinked":
                msg = self.texts["unlinked"].format(email)
                self.log(msg)
                self.save_result("Unlinked.txt", email)

            elif status == "RateLimited":
                self.log(self.texts["rate_limited"])
                self.save_result("RateLimited.txt", email)
                time.sleep(10)

            else:
                self.log(self.texts["error"])
                self.save_result("Errors.txt", email)

            self.queue.task_done()

    def start_checking(self):
        if not hasattr(self, "emails") or not self.emails:
            messagebox.showwarning(self.texts["title"], self.texts["select_email_file"])
            return

        self.stop_flag = False
        self.start_btn.config(state="disabled")
        self.log_text.delete("1.0", tk.END)

        mode = self.mode_var.get()
        self.queue = queue.Queue()
        for email in self.emails:
            self.queue.put(email)

        if mode == "sleep":
            try:
                sleep_time = float(self.sleep_entry.get())
            except:
                sleep_time = 1
            threading.Thread(target=self.sleep_mode_worker, args=(sleep_time,), daemon=True).start()
        else:
            try:
                thread_count = int(self.thread_entry.get())
                if thread_count <= 0:
                    thread_count = DEFAULT_THREAD_COUNT
            except:
                thread_count = DEFAULT_THREAD_COUNT
            threading.Thread(target=self.thread_mode_worker, args=(thread_count,), daemon=True).start()

    def sleep_mode_worker(self, sleep_time):
        while not self.queue.empty() and not self.stop_flag:
            email = self.queue.get()
            status, username, followers, following = self.get_instagram_account_data(email)

            if status == "Linked":
                msg = self.texts["linked"].format(email, username, followers, following)
                self.log(msg)
                self.save_result("LinkedAvailable.txt", f"{email} | User: {username} | Followers: {followers} | Following: {following}")

            elif status == "Unlinked":
                msg = self.texts["unlinked"].format(email)
                self.log(msg)
                self.save_result("Unlinked.txt", email)

            elif status == "RateLimited":
                self.log(self.texts["rate_limited"])
                self.save_result("RateLimited.txt", email)
                time.sleep(10)

            else:
                self.log(self.texts["error"])
                self.save_result("Errors.txt", email)

            self.queue.task_done()
            time.sleep(sleep_time)
        self.start_btn.config(state="normal")
        self.log(self.texts["finished"])

    def thread_mode_worker(self, thread_count):
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        self.queue.join()
        self.start_btn.config(state="normal")
        self.log(self.texts["finished"])


if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramCheckerGUI(root)
    root.mainloop()
