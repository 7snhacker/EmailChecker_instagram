import requests
import time
from user_agent import generate_user_agent
lst = open("email.txt","r")
print("""
    ███████╗███╗   ███╗ █████╗ ██╗██╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
    ██╔════╝████╗ ████║██╔══██╗██║██║     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
    █████╗  ██╔████╔██║███████║██║██║     ██║     ███████║█████╗  ██║     █████╔╝ 
    ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
    ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
    ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
by @7snhacker""")
print("instagram version ")
sleep = float(input("sleep : "))
while True:
    reads = lst.readline().split('\n')[0]
    time.sleep(sleep)
    headers = {'user-agent': generate_user_agent(),
               'X-CSRFToken': "missing"

               }
    data = {"email_or_username":reads}
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
    r = requests.post(url,headers=headers,data=data)
    if ("We sent an") in r.text:
        rc = requests.get(f"https://api.skrapp.io/v3/open/verify?email={reads}").text
        if "Email is invalid" in rc:
            print(f"{reads} : Linked : Taken[!]")
            with open("LinkedTaken.txt", "a") as LinkedTaken:
                LinkedTaken.write(reads + "\n")
        elif "Email is valid" in rc:
            print(f"{reads} : Linked : Available[*]")
            print(r.text)
            with open("LinkedAvailable.txt", "a") as Linked:
                Linked.write(reads + "\n")
        else:
            print(f"{reads} : Linked : Unknown[*]")
            print(rc)
            with open("LinkedUnknown.txt", "a") as LinkedUnknown:
                LinkedUnknown.write(reads + "\n")
    elif ("Please wait a few minutes before you try again.") in r.text:
        print("Please wait a few minutes")
        print("You Send Many Requests")
        print("Turn On Vpn")
        time.sleep(2)

    else:
        print(f"UnLinked : {reads}")






































