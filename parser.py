#!/usr/bin/env python
# -*- coding: utf-8 -*-


from splinter import Browser
import os
import re


def parseHtml(url):
	browser = Browser('chrome', headless=True)

	print(url)
	with browser:
		browser.visit("https://www.tripadvisor.fr" + url)
		remove = browser.find_by_css('.header.heading.masthead.masthead_h1').click()
		plus = browser.find_by_css('span.moreBtn')

		rating_date = browser.find_by_css('span.ratingDate')[0]
		rating_date_text = rating_date.text[14:len(rating_date.text)]

		print(rating_date_text)

		location_date = browser.find_by_css('div.prw_reviews_stay_date_hsx')[0]
		location_date_text = location_date.text[17:len(location_date.text)]

		user = browser.find_by_css('.info_text div')[0]
		user_text = user.text

		html = browser.html

		rating_number = int(re.search('ui_bubble_rating bubble_(.*?)\"></span>', html).group(1)) / 10

		print("c'est le user")
		print(rating_number)


		if plus:
			plus.click()

		textElem = browser.find_by_css('span.fullText').first

		text = textElem.text
		result = [text, rating_date_text, location_date_text, user_text, rating_number]
		return result


def main():
	for file in os.listdir("hotels/"):
		print(file)
		with open("./hotels/" + file + "/reviews/reviews_link.csv") as f:
			with open("./resultat.csv", 'a', newline='') as out:
				content = f.readlines()
				for line in content:
					text = parseHtml(line)

					text_clean = text[0].replace(',', '/')
					text_clean_without_br = text_clean.replace('"', '')
					text_clean_without_br = text_clean.replace('<br>', '')
					text_clean_without_br = text_clean.replace('</br>', '')
					text_clean_without_br = text_clean.replace('\n', '')

					print(repr(text_clean_without_br))
					print(text)
					out.write(file + "," + text_clean_without_br + "," + str(text[1]) + "," + str(text[2]) + "," + str(text[3]) + "," + str(text[4]))
					out.write("\n")


if __name__ == '__main__':
	main()
