import requests
import threading
import time
import queue
import sys

# بيانات الـ cookies و headers كما زودتني بها:
COOKIES = {
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

UAID = '1bfcf3d86a676cf18caac2c61f4dcecf'
HPGID = 200225

HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'https://signup.live.com',
    'Referer': 'https://signup.live.com/signup?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'canary': '8FOXN/BoKJoAse9L/cxWgCzIU3wyLo0EnBVrSTmhEQuF3KXW7iSlS0uWIzhy1rsVml1o895MgruB839QaMX1R4SUT8pgeEq92aMk/ej1u4JuFZU+PMM01pI0ZURsQgTvZzDLSvhlGhdGxQtcNm3isYbVaaPERr3Kqhz22ws6CVEh2sKtDcKskRZxqKD5yoqkB+d8pAYm2vMvhhN1ST1YLXODgqQUq0/pcoVSX3kLxhHV7LLga927SGS6OOjkGrji:2:3c',
    'client-request-id': UAID,
    'correlationId': UAID,
    'hpgact': '0',
    'hpgid': str(HPGID),
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

API_URL = 'https://signup.live.com/API/CheckAvailableSigninNames?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1'

def check_email(email):
    json_data = {
        'includeSuggestions': True,
        'signInName': email,
        'uiflvr': 1001,
        'scid': 100118,
        'uaid': UAID,
        'hpgid': HPGID,
    }
    try:
        response = requests.post(API_URL, cookies=COOKIES, headers=HEADERS, json=json_data, timeout=10)
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

def worker(email, idx, total, available_emails, stop_flag, pause_event):
    if stop_flag[0]:
        return
    pause_event.wait()
    status = check_email(email)
    if status == "available":
        print(f"[{idx}/{total}] ✅ Available: {email}")
        available_emails.append(email)
    elif status == "unavailable":
        print(f"[{idx}/{total}] ❌ Unavailable: {email}")
    else:
        print(f"[{idx}/{total}] ⚠️ Error for {email}: {status}")

def main():
    print("Email Availability Checker CLI")
    filename = input("Enter path to email list file (txt): ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            emails = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    if not emails:
        print("No emails found in file.")
        return

    print(f"Loaded {len(emails)} emails.")

    mode = ""
    while mode not in ["sleep", "threads"]:
        mode = input("Select mode (sleep/threads): ").strip().lower()

    sleep_time = 0.5
    thread_count = 10

    if mode == "sleep":
        val = input("Enter sleep time in seconds (e.g. 0.5): ").strip()
        try:
            sleep_time = float(val)
        except:
            print("Invalid input, using default 0.5s")

    else:
        val = input("Enter number of threads (1-50): ").strip()
        try:
            thread_count = int(val)
            if thread_count < 1 or thread_count > 50:
                thread_count = 10
        except:
            print("Invalid input, using default 10")

    available_emails = []
    stop_flag = [False]
    pause_event = threading.Event()
    pause_event.set()

    def input_listener():
        print("Commands: p = pause, r = resume, s = stop")
        while True:
            cmd = input().strip().lower()
            if cmd == "p":
                pause_event.clear()
                print("Paused.")
            elif cmd == "r":
                pause_event.set()
                print("Resumed.")
            elif cmd == "s":
                stop_flag[0] = True
                pause_event.set()
                print("Stopping...")
                break

    listener_thread = threading.Thread(target=input_listener, daemon=True)
    listener_thread.start()

    total = len(emails)

    if mode == "sleep":
        for idx, email in enumerate(emails, 1):
            if stop_flag[0]:
                break
            pause_event.wait()
            status = check_email(email)
            if status == "available":
                print(f"[{idx}/{total}] ✅ Available: {email}")
                available_emails.append(email)
            elif status == "unavailable":
                print(f"[{idx}/{total}] ❌ Unavailable: {email}")
            else:
                print(f"[{idx}/{total}] ⚠️ Error for {email}: {status}")
            time.sleep(sleep_time)
    else:
        threads = []
        for idx, email in enumerate(emails, 1):
            if stop_flag[0]:
                break
            pause_event.wait()
            while threading.active_count() > thread_count:
                time.sleep(0.1)
            t = threading.Thread(target=worker, args=(email, idx, total, available_emails, stop_flag, pause_event))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    print("\nChecking finished.")
    print(f"Available emails ({len(available_emails)}):")
    for e in available_emails:
        print(e)

    # حفظ النتائج
    save = input("Save available emails to file? (y/n): ").strip().lower()
    if save == "y":
        out_file = input("Enter output filename: ").strip()
        try:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write("\n".join(available_emails))
            print(f"Saved to {out_file}")
        except Exception as e:
            print(f"Failed to save file: {e}")

if __name__ == "__main__":
    main()
