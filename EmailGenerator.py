import string
import random
import requests
import re
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# ---------------- CONFIG ----------------
HEADERS = {"User-Agent": "Mozilla/5.0"}
SEARCH_ENGINE = "https://html.duckduckgo.com/html/?q={query}&s={start}"
FAKE_EMAIL_FILE = "fake_emails.txt"
REAL_EMAIL_FILE = "real_emails.txt"
COMBO_FILE = "combo_list.txt"

# ---------------- UTILITIES ----------------

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_line(title):
    print("=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)

# Extensive and diverse name pools
first_names = [
    'john', 'sara', 'mark', 'emma', 'jake', 'linda', 'chris', 'anna', 'mike', 'nina',
    'ahmed', 'mohamed', 'fatima', 'ali', 'omar', 'hassan', 'noor', 'reem', 'khaled', 'salma',
    'abdullah', 'faisal', 'layla', 'mona', 'tariq', 'yasmin', 'huda', 'amal', 'nasser', 'waleed',
    'zainab', 'hussein', 'ibrahim', 'samir', 'jamal', 'dina', 'nawal', 'sami', 'ghada', 'yousef'
]

last_names = [
    'doe', 'smith', 'brown', 'white', 'king', 'johnson', 'lee', 'clark', 'hall', 'wright',
    'ali', 'hassan', 'ahmed', 'khan', 'mohammed', 'faris', 'mansour', 'hamdan', 'abbas', 'fahad',
    'sultan', 'rashid', 'matar', 'sabah', 'soud', 'nasr', 'hilal', 'kamel', 'bakr', 'fahmy',
    'zaki', 'nasser', 'taha', 'mahmoud', 'morsi', 'samir', 'younes', 'sharif', 'darwish', 'adel'
]

adjectives = ['fast', 'cool', 'hot', 'red', 'blue', 'dark', 'happy', 'sad', 'wild', 'quiet', 'crazy', 'brave', 'smart', 'lazy']
nouns = ['tiger', 'lion', 'eagle', 'wolf', 'shark', 'dragon', 'hawk', 'fox', 'bear', 'snake', 'panther', 'falcon', 'rhino', 'cobra']
separators = ['', '.', '_', '-']

def generate_username(style):
    num = str(random.randint(0, 9999))
    if style == 1:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    elif style == 2:
        return random.choice(first_names) + random.choice(last_names)
    elif style == 3:
        return random.choice(first_names) + num
    elif style == 4:
        return random.choice(first_names) + '.' + random.choice(last_names)
    elif style == 5:
        return random.choice(adjectives) + random.choice(nouns) + num
    elif style == 6:
        return random.choice(nouns) + random.choice(separators) + num
    elif style == 7:
        return random.choice(first_names) + random.choice(separators) + random.choice(last_names) + num
    elif style == 8:
        return random.choice(adjectives) + random.choice(first_names) + num
    elif style == 9:
        return random.choice(first_names) + str(random.randint(10, 99))
    elif style == 10:
        return random.choice(adjectives) + random.choice(nouns) + str(random.randint(0, 999))
    else:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def generate_fake_emails(domain, count, style=1):
    seen = set()
    with open(FAKE_EMAIL_FILE, "w", encoding="utf-8") as f:
        for i in range(count):
            while True:
                email = generate_username(style) + f"@{domain}"
                if email not in seen:
                    seen.add(email)
                    f.write(email + "\n")
                    print(f"[{i+1}/{count}] Generated: {email}")
                    break
    print(f"\n[✔] {count} fake emails saved to {FAKE_EMAIL_FILE}")

def extract_emails_from_text(text, domain=None):
    pattern = rf"[a-zA-Z0-9.%+-]+@{re.escape(domain)}" if domain else r"[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)

def extract_combos_from_text(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}:[^\\s]+"
    return re.findall(pattern, text)

def scrape_real_emails(domain, max_pages):
    session = requests.Session()
    found_emails = set()
    print(f"\n[✓] Starting real email search for: {domain}")
    for page in range(max_pages):
        print(f"[*] Searching page {page+1}/{max_pages}...")
        query = f"@{domain}"
        url = SEARCH_ENGINE.format(query=quote_plus(query), start=page * 30)
        try:
            res = session.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")
            links = [a['href'] for a in soup.find_all("a", href=True)]
            for link in links:
                try:
                    sub_res = session.get(link, headers=HEADERS, timeout=10)
                    emails = extract_emails_from_text(sub_res.text, domain)
                    for email in emails:
                        if email not in found_emails:
                            print(f"[✓] Found: {email}")
                            found_emails.add(email)
                except:
                    continue
        except Exception as e:
            print(f"[!] Error on page {page+1}: {e}")
        time.sleep(1.5)
    with open(REAL_EMAIL_FILE, "w", encoding="utf-8") as f:
        for email in sorted(found_emails):
            f.write(email + "\n")
    print(f"\n[✔] {len(found_emails)} real emails saved to {REAL_EMAIL_FILE}")

def scrape_combos(max_pages):
    session = requests.Session()
    found_combos = set()
    print(f"\n[✓] Starting combo list extraction (email:pass format)")
    for page in range(max_pages):
        print(f"[*] Searching page {page+1}/{max_pages}...")
        query = "intext:@gmail.com filetype:txt"
        url = SEARCH_ENGINE.format(query=quote_plus(query), start=page * 30)
        try:
            res = session.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")
            links = [a['href'] for a in soup.find_all("a", href=True)]
            for link in links:
                try:
                    sub_res = session.get(link, headers=HEADERS, timeout=10)
                    combos = extract_combos_from_text(sub_res.text)
                    for combo in combos:
                        if combo not in found_combos:
                            print(f"[✓] Found combo: {combo}")
                            found_combos.add(combo)
                except:
                    continue
        except Exception as e:
            print(f"[!] Error on page {page+1}: {e}")
        time.sleep(1.5)
    with open(COMBO_FILE, "w", encoding="utf-8") as f:
        for combo in sorted(found_combos):
            f.write(combo + "\n")
    print(f"\n[✔] {len(found_combos)} combos saved to {COMBO_FILE}")

def main():
    clear_console()
    print_line("🔥 Ultimate Email & Combo Toolkit - Enhanced 🔥")
    print("\nSelect Mode:")
    print("1. Generate Fake Emails")
    print("2. Extract Real Emails from Web")
    print("3. Extract Email:Password Combos from Web")
    print("4. Do All (Fake + Real + Combo)")
    choice = input("\nEnter your choice [1/2/3/4]: ").strip()
    if choice in ["1", "4"]:
        domain = input("Enter domain (e.g. gmail.com): ").strip().lower()
        count = int(input("Number of fake emails to generate: ").strip())
        print("\nChoose email format (username style):")
        print("1. Random 8 chars (a1b2c3d4)")
        print("2. firstname + lastname")
        print("3. firstname + number")
        print("4. firstname.lastname")
        print("5. adjective + noun + number")
        print("6. noun + separator + number")
        print("7. firstname + separator + lastname + number")
        print("8. adjective + firstname + number")
        print("9. firstname + two digit number")
        print("10. adjective + noun + number (alt)")
        style = int(input("Your choice [1-10]: ").strip())
        generate_fake_emails(domain, count, style)
    if choice in ["2", "4"]:
        domain = input("\nDomain to extract real emails from (e.g. gmail.com): ").strip().lower()
        pages = int(input("How many search pages to scan (e.g. 3): ").strip())
        scrape_real_emails(domain, pages)
    if choice in ["3", "4"]:
        pages = int(input("\nHow many pages to extract combos from (e.g. 3): ").strip())
        scrape_combos(pages)
    print("\n[✔] All tasks completed. Output files saved.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
#########################################################

#import string
#import random
#letters = string.ascii_lowercase
#print("yahoo"'\n'
#      "gmail"'\n'
#      "aol"'\n'
#      "write any domail")
#email = input("domain : ")
#m = int(input("How many emails: "))
#done = 0
#li = 0
#lst = open("email.txt", "w")
#ranges = int(input("email characters range : "))
#while li == 0:
#    lst.write( ''.join(random.choice(letters) for i in range(ranges))+f'@{email}.com'+'\n')
#    done += 1
#    print(done)
#    if done == m:
#        li = 1
#        while True:
#            print("Done (:")
#            print("Click Ctrl C to Exit")
#            input("")
