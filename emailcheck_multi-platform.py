import requests
import time
import random
from user_agent import generate_user_agent

# Banner
print("""
    ███████╗███╗   ███╗ █████╗ ██╗██╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
    ██╔════╝████╗ ████║██╔══██╗██║██║     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
    █████╗  ██╔████╔██║███████║██║██║     ██║     ███████║█████╗  ██║     █████╔╝ 
    ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
    ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
    ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
by @7snhacker""")
print("Starting multi-platform email checker...")

# User input for sleep time between requests
sleep_time = float(input("Sleep time between requests (seconds): "))
timeout_period = 10  # Timeout period for HTTP requests

# Helper function to save results to files with checks
def save_result(file_name, email, status):
    with open(file_name, "a") as file:
        file.write(f"{email} : {status}\n")
    print(f"{email} : {status} saved to {file_name}")

# Function to handle requests and check email validity
def check_email_on_platform(url, data, headers, platform_name):
    try:
        response = requests.post(url, headers=headers, data=data, timeout=timeout_period)
        if response.status_code == 200:
            return response
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error contacting {platform_name}: {e}")
        return None

# List of platforms with respective URLs and request details
platforms = [
    {"name": "Instagram", "url": "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/", "data": {"email_or_username": ""}, "header": {'user-agent': generate_user_agent(), 'X-CSRFToken': "missing"}},
    {"name": "Twitter", "url": "https://api.twitter.com/1.1/account/verify_credentials.json", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Epic Games", "url": "https://www.epicgames.com/account/api/v1/validate-email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "TikTok", "url": "https://www.tiktok.com/api/verify/email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Yahoo", "url": "https://login.yahoo.com/account/validate_email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Steam", "url": "https://store.steampowered.com/account/validate_email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Facebook", "url": "https://www.facebook.com/api/v1/account_recovery", "data": {"email_or_username": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "LinkedIn", "url": "https://www.linkedin.com/checkpoint/lg/sign-in-another-account", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Google", "url": "https://accounts.google.com/AccountChooser", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Reddit", "url": "https://www.reddit.com/api/v1/validate_email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Microsoft", "url": "https://account.microsoft.com/account/validate_email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Apple", "url": "https://appleid.apple.com/account/validate_email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Pinterest", "url": "https://www.pinterest.com/login", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Snapchat", "url": "https://accounts.snapchat.com/accounts/email_login", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Amazon", "url": "https://www.amazon.com/ap/validate-email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Spotify", "url": "https://www.spotify.com/us/account/validate-email", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Netflix", "url": "https://www.netflix.com/login", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Dropbox", "url": "https://www.dropbox.com/login", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Slack", "url": "https://slack.com/signin", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
    {"name": "Discord", "url": "https://discord.com/login", "data": {"email": ""}, "header": {'user-agent': generate_user_agent()}},
]

# Main loop to process email list
lst = open("email.txt", "r")
while True:
    email = lst.readline().strip()
    if not email:
        break  # End of file, exit loop
    time.sleep(sleep_time + random.uniform(0.5, 1.5))  # Random delay between requests
    
    # Process each platform
    for platform in platforms:
        platform["data"]["email_or_username"] = email
        response = check_email_on_platform(platform["url"], platform["data"], platform["header"], platform["name"])
        
        if response:
            # Determine if email is valid or invalid for each platform
            if "success" in response.text or "sent" in response.text:
                save_result("LinkedAvailable.txt", email, f"{platform['name']} : Available[*]")
            elif "invalid" in response.text or "error" in response.text:
                save_result("LinkedTaken.txt", email, f"{platform['name']} : Taken[!]")
            else:
                save_result("LinkedUnknown.txt", email, f"{platform['name']} : Unknown[*]")
        else:
            save_result("LinkedUnknown.txt", email, f"{platform['name']} : Error contacting platform")

    print(f"Processed: {email}")

lst.close()
