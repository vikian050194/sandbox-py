def download(url):
    try:
        filename = url.split("/")[-1]
        r = requests.get(url, allow_redirects=True)
        open(filename, "wb").write(r.content)
    except Exception as e:
        print(e)
