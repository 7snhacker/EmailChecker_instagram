import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import requests
import time

class EmailCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Availability Checker")
        self.root.geometry("700x600")

        self.available_emails = []
        self.stop_flag = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.available_file = "Available.txt"

        self.emails = []

        self.mode_var = tk.StringVar(value="threads")
        self.sleep_time_var = tk.DoubleVar(value=0.5)
        self.thread_count_var = tk.IntVar(value=10)

        # وضع التشغيل
        mode_frame = tk.LabelFrame(root, text="Select Mode", padx=10, pady=10)
        mode_frame.pack(padx=10, pady=10, fill="x")

        tk.Radiobutton(mode_frame, text="Threads", variable=self.mode_var, value="threads",
                       command=self.toggle_mode).pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(mode_frame, text="Sleep", variable=self.mode_var, value="sleep",
                       command=self.toggle_mode).pack(side=tk.LEFT, padx=20)

        # إعدادات Threads
        self.threads_frame = tk.LabelFrame(root, text="Threads Settings", padx=10, pady=10)
        self.threads_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(self.threads_frame, text="Number of Threads (1-50):").pack(side=tk.LEFT)
        self.thread_spin = tk.Spinbox(self.threads_frame, from_=1, to=50, textvariable=self.thread_count_var, width=5)
        self.thread_spin.pack(side=tk.LEFT, padx=10)

        # إعدادات Sleep
        self.sleep_frame = tk.LabelFrame(root, text="Sleep Settings", padx=10, pady=10)
        self.sleep_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(self.sleep_frame, text="Sleep Time (seconds):").pack(side=tk.LEFT)
        self.sleep_spin = tk.Spinbox(self.sleep_frame, from_=0, to=10, increment=0.1, textvariable=self.sleep_time_var, width=5)
        self.sleep_spin.pack(side=tk.LEFT, padx=10)

        # زر استيراد الإيميلات
        import_frame = tk.Frame(root)
        import_frame.pack(pady=5)

        self.import_btn = tk.Button(import_frame, text="Import Emails", width=20, command=self.import_emails)
        self.import_btn.pack()

        # أزرار التحكم Start, Pause, Resume, Stop
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start", width=10, command=self.start_checking)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(btn_frame, text="Pause", width=10, state=tk.DISABLED, command=self.pause_checking)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.resume_btn = tk.Button(btn_frame, text="Resume", width=10, state=tk.DISABLED, command=self.resume_checking)
        self.resume_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="Stop", width=10, state=tk.DISABLED, command=self.stop_checking)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # أزرار نسخ، حفظ، مسح النتائج
        action_frame = tk.Frame(root)
        action_frame.pack(pady=5)

        self.copy_btn = tk.Button(action_frame, text="Copy Results", width=15, command=self.copy_results)
        self.copy_btn.pack(side=tk.LEFT, padx=10)

        self.save_btn = tk.Button(action_frame, text="Save Results", width=15, command=self.save_results)
        self.save_btn.pack(side=tk.LEFT, padx=10)

        self.clear_btn = tk.Button(action_frame, text="Clear Results", width=15, command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        # مربع النتائج / السجلات
        self.status_box = scrolledtext.ScrolledText(root, height=15)
        self.status_box.pack(padx=10, pady=10, fill="both", expand=True)

        self.toggle_mode()

    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "threads":
            self.threads_frame.pack(padx=10, pady=5, fill="x")
            self.sleep_frame.pack_forget()
        else:
            self.sleep_frame.pack(padx=10, pady=5, fill="x")
            self.threads_frame.pack_forget()

    def log(self, message):
        self.status_box.insert(tk.END, message + "\n")
        self.status_box.see(tk.END)

    def import_emails(self):
        file_path = filedialog.askopenfilename(
            title="Select Email List File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    emails = [line.strip() for line in f if line.strip()]
                if emails:
                    self.emails = emails
                    messagebox.showinfo("Success", f"Imported {len(emails)} emails successfully.")
                    self.log(f"Imported {len(emails)} emails from {file_path}")
                else:
                    messagebox.showwarning("Warning", "No emails found in the selected file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import emails:\n{str(e)}")

    def check_email_availability(self, email):
        cookies = {
            'MUID': 'f768f0a9d71a47058deef47149cf691d',
            'mkt': 'en-US',
            '_pxvid': '387b5fe0-4ef8-11f0-baa7-ad0d60f7fa91',
            'MSFPC': 'GUID=17d02f066f0449a2b73597042bbff98c&HASH=17d0&LV=202504&V=4&LU=1744202961624',
            'mkt1': 'en-US',
            'amsc': 'rgLkzt7J7ly9nkHGg6O7WefQDQFfFZmbZJgDiy0uuGJV8AOhVjA7g9H8/6ANTG7kkGhl+r2z9qazvFEJUNDZvqsMHytlDDFP7VMu/C+6teNn9Me5O0RlgL5OqqBe35oU4UyNLVmrC6WdcLm+FQgC36Ck3VQ/hnQg0LM3WHGYHyQmYLnA6NS1K0HmHI1FuSFVXg/HcaQPm45kbfexwIWt9c/rAUu0AjAQpGloJFeiKQgZAs65mGfCvN/qcUnmCqGedX+GgLnCkJRMeXEwvcx1xWH1TlQmulL67+2gxY9eDFpPgJc8VnBtUP3pL3uGMwcH:2:3c',
            'fptctx2': 'taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO3k3ecRPU%252fEniICvNC0stL5RfgqQc2MJzffXpGPyMoteq0x4AJ3nU%252fnHVK03udcgd%252bpof%252b1H9sMQVyGXIfrvWh9ktrtAQhkmCuBDPN9WOVUjfGoOgXK8KjzgUk98q4sEiNEphJr3Ng%252bGDruXRbzgrEANOg3%252b3rpFZze0p%252f%252fnt2tkgWukqLSyf3BmL3luobm%252b8ueZcZqIVXCfN4JBlgPRhEue9Iu8KicgtBW0bzilvir4Ni9L7s%252fuFBfg8QMvGKoyPOUyfm5qPM3DLLi%252fTibwAeYkAGO0joqyFhgpJPkmyBZ2Q%253d%253d',
            'ai_session': 'sw+Qt2N/o0AeH+bq866xxl|1750730005893|1750730032360',
            '_px3': ('314fb0128cb9c781b9aba89b3c8b393ca92e86076b4f5fabc86300ff43c32ccc:'
                     'xnAtkWL2DobtBM/3Gj0v9lIiHKH2YiQADOQBSEaLhEHlg2RtJbHeYidtO50QYmQCMOg0zxmUagWsD1kSXnyHVw==:'
                     '1000:BXi2yOn86s5JuG1JLzr3SONQBErCpzv/P8XELjKrWZP7Ulxi1y5KOMB7Q/JbKKTN5v932sleJPK2iJGo0g910J97wJYNEQPUi++xsootwsUmctdMNNWlnwfmnE++ZcbGM59o01X16aBorouoj5GmEJjUEwGqbx79C4mLFS517VuFE4N/GpkCd3ZE1JBJLEQFvaF3Zo5ZwgIhLpLZhH14AViDta4ERet5TxcO7jeVfoU='),
            '_pxde': '76630ecb267458b41d4e7dac9181be7877c0569cae88f1f703b02dd3bb17b4d7:eyJ0aW1lc3RhbXAiOjE3NTA3MzAwMzM3ODAsImZfa2IiOjAsImluY19pZCI6WyJiZjYzZDAxZDg2YzNjNmQ0YTI0YjBmZjgxZWU2MDZlNCJdfQ==',
        }

        uaid = '1bfcf3d86a676cf18caac2c61f4dcecf'
        hpgid = 200225

        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=utf-8',
            'Origin': 'https://signup.live.com',
            'Referer': ('https://signup.live.com/signup?sru=https%3a%2f%2flogin.live.com%2f'
                        'oauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%'
                        '3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%'
                        '3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%'
                        '26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1'),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'canary': ('8FOXN/BoKJoAse9L/cxWgCzIU3wyLo0EnBVrSTmhEQuF3KXW7iSlS0uWIzhy1rsVml1o895MgruB839QaMX1R4SUT8pgeEq92aMk/ej1u4JuFZU+PMM01pI0ZURsQgTvZzDLSvhlGhdGxQtcNm3isYbVaaPERr3Kqhz22ws6CVEh2sKtDcKskRZxqKD5yoqkB+d8pAYm2vMvhhN1ST1YLXODgqQUq0/pcoVSX3kLxhHV7LLga927SGS6OOjkGrji:2:3c'),
            'client-request-id': uaid,
            'correlationId': uaid,
            'hpgact': '0',
            'hpgid': str(hpgid),
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        json_data = {
            'includeSuggestions': True,
            'signInName': email,
            'uiflvr': 1001,
            'scid': 100118,
            'uaid': uaid,
            'hpgid': hpgid,
        }

        try:
            response = requests.post(
                'https://signup.live.com/API/CheckAvailableSigninNames?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1',
                cookies=cookies,
                headers=headers,
                json=json_data,
                timeout=10
            )
            if response.status_code == 200:
                text = response.text
                if '"isAvailable":true' in text:
                    return "available"
                elif '"isAvailable":false' in text:
                    return "unavailable"
                else:
                    return "unknown"
            else:
                return f"error: status code {response.status_code}"
        except Exception as e:
            return f"error: {str(e)}"

    def run_sleep_mode(self):
        self.log("Running in Sleep mode...")
        total = len(self.emails)
        for idx, email in enumerate(self.emails, 1):
            if self.stop_flag:
                break
            self.pause_event.wait()
            status = self.check_email_availability(email)
            if status == "available":
                self.log(f"[{idx}/{total}] ✅ Available: {email}")
                self.available_emails.append(email)
                with open(self.available_file, "a", encoding="utf-8") as f:
                    f.write(email + "\n")
            elif status == "unavailable":
                self.log(f"[{idx}/{total}] ❌ Unavailable: {email}")
            else:
                self.log(f"[{idx}/{total}] ⚠️ Error for {email}: {status}")

            time.sleep(self.sleep_time_var.get())

        self.log("Sleep mode finished.")
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)

    def worker_thread(self, email, idx, total):
        if self.stop_flag:
            return
        self.pause_event.wait()
        status = self.check_email_availability(email)
        if status == "available":
            self.log(f"[{idx}/{total}] ✅ Available: {email}")
            self.available_emails.append(email)
            with open(self.available_file, "a", encoding="utf-8") as f:
                f.write(email + "\n")
        elif status == "unavailable":
            self.log(f"[{idx}/{total}] ❌ Unavailable: {email}")
        else:
            self.log(f"[{idx}/{total}] ⚠️ Error for {email}: {status}")

    def run_threads_mode(self):
        self.log("Running in Threads mode...")
        total = len(self.emails)
        thread_count = self.thread_count_var.get()
        threads = []
        for idx, email in enumerate(self.emails, 1):
            if self.stop_flag:
                break
            self.pause_event.wait()
            while threading.active_count() > thread_count:
                time.sleep(0.1)
            t = threading.Thread(target=self.worker_thread, args=(email, idx, total))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.log("Threads mode finished.")
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)

    def start_checking(self):
        if self.stop_flag:
            self.stop_flag = False
        self.available_emails.clear()
        self.status_box.delete("1.0", tk.END)

        if not self.emails:
            try:
                with open("email.txt", "r", encoding="utf-8") as f:
                    self.emails = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                messagebox.showerror("Error", "email.txt file not found and no emails imported!")
                return

        if not self.emails:
            messagebox.showwarning("Warning", "No emails to check!")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        mode = self.mode_var.get()
        threading.Thread(target=self.run_sleep_mode if mode == "sleep" else self.run_threads_mode).start()

    def pause_checking(self):
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.NORMAL)
        self.log("Paused.")
        self.pause_event.clear()

    def resume_checking(self):
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.log("Resumed.")
        self.pause_event.set()

    def stop_checking(self):
        self.stop_flag = True
        self.pause_event.set()  # استئناف إذا كان متوقف حتى يتمكن من الإيقاف
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("Stopped.")

    def copy_results(self):
        if self.available_emails:
            self.root.clipboard_clear()
            self.root.clipboard_append("\n".join(self.available_emails))
            messagebox.showinfo("Copied", "Available emails copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "No available emails to copy.")

    def save_results(self):
        if self.available_emails:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Available Emails"
            )
            if save_path:
                try:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(self.available_emails))
                    messagebox.showinfo("Saved", f"Available emails saved to:\n{save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
        else:
            messagebox.showwarning("Warning", "No available emails to save.")

    def clear_results(self):
        self.status_box.delete("1.0", tk.END)
        self.available_emails.clear()
        self.log("Results cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailCheckerApp(root)
    root.mainloop()
