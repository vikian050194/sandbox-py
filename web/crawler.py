#!/usr/bin/env python3

import os
import requests
from html.parser import HTMLParser

from download import download as download_file
from load import load as load_page_content


site = "https://notificationsounds.com"
page = "/notification-sounds/pages/"
pages = dict()


class FooParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            (name, value) = attr
            if name == "class" and value == "block text-2xl text-link mb-6 leading-6":
                initial_page = attrs[0][1]
                _, sound_type, sound_name = initial_page.split("/")
                if sound_type in pages:
                    pages_list = pages.get(sound_type)
                    pages_list.append(sound_name)
                else:
                    pages_list = [sound_name]
                    pages[sound_type] = pages_list
                continue


files = set()


class BarParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            (name, value) = attr
            if name == "href" and value.endswith(".mp3"):
                file = value
                values = value.split("/")
                folder = values[3]
                name = values[-1]
                if not name in files:
                    files.add(name)
                    print(file)
                    download_file(file, folder)
                break


def foo_crawl(url):
    try:
        page = load_page_content(url)
        page = page.decode("utf-8")

        # fo = open("page.html", "r+")
        # page = fo.read()
        # fo.close()

        parser = FooParser()
        parser.feed(page)
    except Exception as e:
        print(e)


def bar_crawl(url):
    try:
        page = load_page_content(url)
        page = page.decode("utf-8")

        # fo = open("page.html", "r+")
        # page = fo.read()
        # fo.close()

        parser = BarParser()
        parser.feed(page)
    except Exception as e:
        print(e)


for i in range(1, 49):
    url = site + page + str(i)
    foo_crawl(url)

for sound_type, pages_list in pages.items():
    pages_list = sorted(pages_list)
    for page_item in pages_list:
        url = site + "/" + sound_type + "/" + page_item
        bar_crawl(url)
