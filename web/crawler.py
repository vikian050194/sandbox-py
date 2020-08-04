#!/usr/bin/env python3

"""Crawler"""

import os
import requests
from html.parser import HTMLParser

from download import download as download_file
from load import load as load_page_content

site = "https://lingua.com"
page = "/french/reading/"

class HrefParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            (name, value) = attr
            if name == "href" and value.endswith(".pdf"):
                file = value[5:] 
                print(file)
                download_file( + file)


def crawl(url):
    try:
        page = load_page_content(url)

        # fo = open("page.html", "r+")
        # page = fo.read()
        # fo.close()
        
        parser = HrefParser()
        parser.feed(page)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    crawl(site + page)
