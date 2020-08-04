def load(url):
    try:
        return requests.get(url, allow_redirects=True).content
    except Exception as e:
        print(e)
        return ""
