#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os

import requests
import re
from splinter import Browser


def parseHtml(url, hotel_en_cour):

	browser = Browser('chrome', headless=True)

	print(url)
	with browser:
		browser.visit(url)
		remove = browser.find_by_css('body').click()

		plus_present = browser.is_element_not_present_by_css('span.moreBtn', wait_time=5)

		plus = browser.find_by_css('span.moreBtn')

		reviews = browser.find_by_css('.hotels-community-tab-common-Card__section--4r93H')

		i = 0
		for review in reviews:

			if	i == 5:
				break

			user = review.find_by_css('.social-member-event-MemberEventOnObjectBlock__member--35-jC').text
			user_contribution = review.find_by_css('.social-member-MemberHeaderStats__bold--3z3qh')[0].text
			vote_utile = 0

			date_contribution_raw = str(review.find_by_css('.social-member-event-MemberEventOnObjectBlock__event_type--3njyv span').text)

			date_sejour = review.find_by_css('.hotels-review-list-parts-EventDate__event_date--CRXs4')

			date_sejour_formatted = date_sejour.text[16:len(date_sejour.text)]



			if re.search("avis le", date_contribution_raw):
				pos_date = re.search("avis le", date_contribution_raw).end()
				date_contribution = date_contribution_raw[pos_date:len(date_contribution_raw)]

			if len(review.find_by_css('.social-member-MemberHeaderStats__bold--3z3qh')) > 1:
				text = review.find_by_css('q.hotels-review-list-parts-ExpandableReview__reviewText--3oMkH').text
				vote_utile = review.find_by_css('.social-member-MemberHeaderStats__bold--3z3qh')[1].text

			if len(date_sejour) > 0:
				date_sejour = date_sejour.text


			if len(review.find_by_css('q.hotels-review-list-parts-ExpandableReview__reviewText--3oMkH')) > 0:
				text = review.find_by_css('q.hotels-review-list-parts-ExpandableReview__reviewText--3oMkH').text


			reponse_proprio = review.find_by_css('.hotels-review-list-parts-OwnerResponse__reviewText--28Wat').text


			text_clean = text.replace(',', '/')
			text_clean = text_clean.replace('\n' , " ")

			reponse_proprio_clean = reponse_proprio.replace(',', '/')
			reponse_proprio_clean = reponse_proprio_clean.replace('\n', " ")


			with open("./resultat.csv", 'a', newline='') as out:
				out.write(hotel_en_cour + ","+ str(user) + "," + str(user_contribution) + "," + str(vote_utile) +  "," + str(date_contribution) + ","  + str(date_sejour_formatted) + "," + repr(text_clean) + "," + str(reponse_proprio_clean))
				out.write("\n")

			i = i + 1

		return 1


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

			parseHtml(url_origin, hotel_en_cour)



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

				parseHtml(url_page, hotel_en_cour)
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
