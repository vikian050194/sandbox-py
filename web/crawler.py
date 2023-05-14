#!/usr/bin/env python3

"""Crawler"""

import os
import requests
from html.parser import HTMLParser

from download import download as download_file
from load import load as load_page_content

site = "https://hpaudiobooks.club"
page = "/harry-potter-and-prisoner-azkaban/"

index = 1

class HrefParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "source":
            for attr in attrs:
                (name, value) = attr
                try:
                    if name == "src" and value.endswith(f".mp3?_={index}"):
                        file = value[5:] 
                        print(file)
                        download_file( + file)
                        index += 1
                except:
                    pass


def crawl(url):
    try:
        page = load_page_content(url)
        page = page.decode()
        # fo = open("page.html", "r+")
        # page = fo.read()
        # fo.close()
        
        parser = HrefParser()
        parser.feed(page)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    crawl(site + page)
