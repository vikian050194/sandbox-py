import os
import requests

def download(url, folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = url.split("/")[-1]
        filename = folder + "/" + filename
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs-CZ;q=0.6,cs;q=0.5",
            "cache-control": "no-cache",
            "cookie": "_ga=GA1.2.28811514.1621103113; _gid=GA1.2.1407532990.1621103113",
            "pragma": "no-cache",
            "referer": "https://notificationsounds.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        # headers={}
        r = requests.get(url, allow_redirects=False, headers=headers)
        if r.status_code == 200:
            open(filename, "wb").write(r.content)
            print(folder, url.split("/")[-1])
        else:
            print(r)
    except Exception as e:
        print(e)
