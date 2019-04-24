#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os

import requests
import re
from html.parser import HTMLParser


class getReviewsURL(HTMLParser):

    def __init__(self, hotel_en_cour):
        super().__init__()
        self.hotel_en_cour = hotel_en_cour
        self.counter = 0

    def handle_starttag(self, tag, attrs):

        if tag.startswith('a') and self.counter < 110:
            self.counter = self.counter + 1
            for attr in attrs:
                if attr[0] == 'href' and attr[1][0:16] == '/ShowUserReviews':
                    try:
                        os.makedirs("hotels/" + self.hotel_en_cour + "/reviews/")
                    except FileExistsError:
                        pass

                    with open("./hotels/" + self.hotel_en_cour + "/reviews/reviews_link.csv", 'a', newline='') as out:
                        print(attr[1])
                        out.write(attr[1])
                        out.write("\n")


def retrievelocations():

    with open('./csv/input_2.csv', newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in content:
            url_origin = row[1]
            hotel_en_cour = row[0].replace(' ', '')

            create_directory(hotel_en_cour)

            print("hotel en cour:" + url_origin)
            page = requests.get(url_origin)
            html = page.text
            m = re.search('<a class="pageNum " href="(.+?)</a>', html)
            if m:
                found = m.group(1)
                number = int(re.search(r'\d+', found[60:len(found)]).group())
                step = number
                print("Nombre total  de page: " + str(step))
            parser = getReviewsURL(hotel_en_cour)
            parser.feed(html)

            pagination = 5
            print("Pagination: " + str(pagination) + "step: " + str(step))

            loop = range(step, 0, -1)
            for pageId in loop:
                print("Pagination: " + str(pagination) + "step: " + str(step))
                print("loop: " + str(pageId))
                pos_reviews = re.search("-Reviews-", url_origin).end()
                url_page = url_origin[:pos_reviews] + 'or' + str(pagination) + url_origin[pos_reviews - 1:]
                print("page url " + url_page)
                print("Pagination: " + str(pagination) + "step: " + str(step))
                page = requests.get(url_page)
                html = page.text

                parser = getReviewsURL(hotel_en_cour)
                parser.feed(html)
                pagination = pagination + 5


def create_directory(path):
    try:
        os.makedirs("hotels/" + path)
    except FileExistsError:
        pass

def get_every_str_between(s, before, after):
    return (i.split(after)[0] for i in s.split(before)[1:] if after in i)

def main():
    retrievelocations()


if __name__ == '__main__':
    main()
