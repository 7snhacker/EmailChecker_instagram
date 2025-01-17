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
    # Add more platforms here if needed
]

# Skrapp API
def check_skrapp(email):
    skrapp_url = f"https://api.skrapp.io/v3/open/verify?email={email}"
    try:
        response = requests.get(skrapp_url)
        if response.status_code == 200:
            result = response.json()
            return result.get("status", "unknown")
        else:
            print(f"Error with Skrapp API for {email}: {response.status_code}")
            return "unknown"
    except Exception as e:
        print(f"Error with Skrapp API for {email}: {e}")
        return "unknown"

# Results
results = {
    "linked_available": [],
    "linked_taken": [],
    "unlinked": [],
    "unknown": [],
    "skrapp_status": []
}

# Main loop
for email in email_list:
    skrapp_status = check_skrapp(email)
    print(f"Skrapp status for {email}: {skrapp_status}")
    results["skrapp_status"].append(f"{email}: {skrapp_status}")
    time.sleep(sleep_interval)

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
with open("Unlinked.txt", "w") as f:
    f.writelines([email + "\n" for email in results["unlinked"]])
with open("Unknown.txt", "w") as f:
    f.writelines([email + "\n" for email in results["unknown"]])
with open("SkrappStatus.txt", "w") as f:
    f.writelines([status + "\n" for status in results["skrapp_status"]])

print("Check completed. Results saved!"
