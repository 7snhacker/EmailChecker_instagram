import requests
import time
from user_agent import generate_user_agent

def check_instagram(email):
    """Check the status of the email using Instagram API and third-party verification services."""
    headers = {
        'user-agent': generate_user_agent(),
        'X-CSRFToken': "missing"
    }
    data = {"email_or_username": email}
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"

    try:
        response = requests.post(url, headers=headers, data=data)
        if "We sent an" in response.text:
            return 'Instagram Sent', response.text
        elif "Please wait a few minutes" in response.text:
            return 'Instagram RateLimited', response.text
        else:
            return 'Instagram UnLinked', response.text
    except requests.exceptions.RequestException as e:
        return 'Instagram Error', str(e)

def check_twitter(email):
    """Check the status of the email using Twitter API and third-party verification services."""
    # Simulate Twitter email check or recovery request
    try:
        url = f"https://twitter.com/account/begin_password_reset"
        data = {'email': email}
        headers = {'User-Agent': generate_user_agent()}
        response = requests.post(url, headers=headers, data=data)
        if "Please enter your email address" in response.text:
            return 'Twitter Linked', response.text
        else:
            return 'Twitter UnLinked', response.text
    except requests.exceptions.RequestException as e:
        return 'Twitter Error', str(e)

def check_facebook(email):
    """Simulate Facebook account verification or email check."""
    try:
        url = f"https://www.facebook.com/recover/initiate/"
        data = {'email': email}
        headers = {'User-Agent': generate_user_agent()}
        response = requests.post(url, headers=headers, data=data)
        if "We sent you an email" in response.text:
            return 'Facebook Sent', response.text
        else:
            return 'Facebook UnLinked', response.text
    except requests.exceptions.RequestException as e:
        return 'Facebook Error', str(e)

def check_snapchat(email):
    """Simulate Snapchat email recovery process."""
    try:
        url = f"https://accounts.snapchat.com/accounts/password_reset_request"
        data = {'email': email}
        headers = {'User-Agent': generate_user_agent()}
        response = requests.post(url, headers=headers, data=data)
        if "Snapchat sent you an email" in response.text:
            return 'Snapchat Sent', response.text
        else:
            return 'Snapchat UnLinked', response.text
    except requests.exceptions.RequestException as e:
        return 'Snapchat Error', str(e)

def verify_email_third_party(email):
    """Verify the email using third-party service (e.g., Skrapp)."""
    try:
        api_url = f"https://api.skrapp.io/v3/open/verify?email={email}"
        response = requests.get(api_url).json()
        if response.get("status") == "Email is invalid":
            return 'Invalid', response
        elif response.get("status") == "Email is valid":
            return 'Valid', response
        else:
            return 'Unknown', response
    except requests.exceptions.RequestException as e:
        return 'Error', str(e)

def save_status(email, status):
    """Save email status to appropriate files."""
    if status == 'Linked - Taken':
        with open("LinkedTaken.txt", "a") as file:
            file.write(email + "\n")
    elif status == 'Linked - Available':
        with open("LinkedAvailable.txt", "a") as file:
            file.write(email + "\n")
    elif status == 'Linked - Unknown':
        with open("LinkedUnknown.txt", "a") as file:
            file.write(email + "\n")
    elif status == 'UnLinked':
        with open("UnLinkedEmails.txt", "a") as file:
            file.write(email + "\n")
    
def main():
    print("""
    ███████╗███╗   ███╗ █████╗ ██╗██╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
    ██╔════╝████╗ ████║██╔══██╗██║██║     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
    █████╗  ██╔████╔██║███████║██║██║     ██║     ███████║█████╗  ██║     █████╔╝
    ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗
    ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
    ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
    by @7snhacker
    """)

    # Input sleep interval between requests
    sleep_interval = float(input("Enter sleep interval (in seconds): "))
    
    with open("email.txt", "r") as lst:
        for email in lst:
            email = email.strip()
            time.sleep(sleep_interval)
            
            # Check status on multiple platforms
            platforms = [check_instagram, check_twitter, check_facebook, check_snapchat]
            for platform in platforms:
                status, response = platform(email)
                print(f"{email} - {status}")
                
                if "Sent" in status:
                    # If the platform sends a reset email or verification
                    link_status, verification_response = verify_email_third_party(email)
                    if link_status == 'Valid':
                        print(f"{email} : Linked : Taken[!]")
                        save_status(email, 'Linked - Taken')
                    elif link_status == 'Invalid':
                        print(f"{email} : Linked : Available[*]")
                        save_status(email, 'Linked - Available')
                    else:
                        print(f"{email} : Linked : Unknown[*]")
                        save_status(email, 'Linked - Unknown')
                elif "RateLimited" in status:
                    print("Rate limit reached. Please try again later.")
                    time.sleep(5)
                else:
                    print(f"{email} : UnLinked")
                    save_status(email, 'UnLinked')
                
if __name__ == "__main__":
    main()
