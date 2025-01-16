import requests
import time
from user_agent import generate_user_agent

# Banner
print("""
    ███████╗███╗   ███╗ █████╗ ██╗██╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
    ██╔════╝████╗ ████║██╔══██╗██║██║     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
    █████╗  ██╔████╔██║███████║██║██║     ██║     ███████║█████╗  ██║     █████╔╝ 
    ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
    ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
    ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
by @7snhacker
""")

# User input
email_file = input("Enter the email file path: ")
sleep_interval = float(input("Sleep interval (seconds): "))

# Read emails from file
try:
    with open(email_file, "r") as f:
        email_list = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print("Email file not found!")
    exit()

# Platforms to check
platforms = [
    {
        "name": "Instagram",
        "url": "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'X-CSRFToken': "missing"
        },
        "data": lambda email: {"email_or_username": email},
        "success_message": "We sent an",
        "rate_limit_message": "Please wait a few minutes before you try again."
    },
    {
        "name": "TikTok",
        "url": "https://www.tiktok.com/api/passport/web/send_code/",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/json"
        },
        "data": lambda email: {"account": email, "type": "email"},
        "success_message": "verification code has been sent",
        "rate_limit_message": "Too many attempts"
    },
    {
        "name": "Snapchat",
        "url": "https://accounts.snapchat.com/accounts/validate_email",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/x-www-form-urlencoded"
        },
        "data": lambda email: {"email": email},
        "success_message": "Email is valid",
        "rate_limit_message": "Too many requests"
    },
    {
        "name": "Twitter",
        "url": "https://api.twitter.com/i/account/login_verification",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/json"
        },
        "data": lambda email: {"email": email},
        "success_message": "An email has been sent",
        "rate_limit_message": "Too many requests"
    },
    {
        "name": "Netflix",
        "url": "https://www.netflix.com/api/v2/account/validateemail",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/json"
        },
        "data": lambda email: {"email": email},
        "success_message": "valid email",
        "rate_limit_message": "Too many requests"
    },
    {
        "name": "Twitch",
        "url": "https://passport.twitch.tv/password_resets",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/json"
        },
        "data": lambda email: {"email": email},
        "success_message": "password reset email sent",
        "rate_limit_message": "Too many requests"
    },
    {
        "name": "Amazon",
        "url": "https://www.amazon.com/ap/forgotpassword",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/json"
        },
        "data": lambda email: {"email": email},
        "success_message": "password reset email sent",
        "rate_limit_message": "Please wait"
    },
    {
        "name": "Discord",
        "url": "https://discord.com/api/v9/auth/forgot",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/json"
        },
        "data": lambda email: {"email": email},
        "success_message": "reset email sent",
        "rate_limit_message": "You are being rate limited"
    },
    {
        "name": "Facebook",
        "url": "https://www.facebook.com/recover/initiate",
        "headers": lambda: {
            'user-agent': generate_user_agent(),
            'Content-Type': "application/x-www-form-urlencoded"
        },
        "data": lambda email: {"email": email},
        "success_message": "check your email",
        "rate_limit_message": "Please slow down"
    }
]

# Results
results = {
    "linked_available": [],
    "linked_taken": [],
    "unlinked": [],
    "unknown": []
}

# Main loop
for email in email_list:
    for platform in platforms:
        platform_name = platform["name"]
        print(f"Checking {email} on {platform_name}...")
        time.sleep(sleep_interval)

        try:
            response = requests.post(
                platform["url"],
                headers=platform["headers"](),
                data=platform["data"](email)
            )
            if platform["success_message"] in response.text:
                print(f"{email} is linked on {platform_name}.")
                results["linked_available"].append(email)
            elif platform["rate_limit_message"] in response.text:
                print(f"Rate limit reached for {platform_name}. Retrying...")
                time.sleep(10)
            else:
                print(f"{email} is unlinked on {platform_name}.")
                results["unlinked"].append(email)
        except Exception as e:
            print(f"Error checking {email} on {platform_name}: {e}")
            results["unknown"].append(email)

# Save results to files
with open("LinkedAvailable.txt", "w") as f:
    f.writelines([email + "\n" for email in results["linked_available"]])
with open("LinkedTaken.txt", "w") as f:
    f.writelines([email + "\n" for email in results["linked_taken"]])
with open("Unlinked.txt", "w") as f:
    f.writelines([email + "\n" for email in results["unlinked"]])
with open("Unknown.txt", "w") as f:
    f.writelines([email + "\n" for email in results["unknown"]])

print("Check completed. Results saved!")
