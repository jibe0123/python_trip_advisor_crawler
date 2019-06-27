#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import time

import re
from splinter import Browser


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parseHtml(url, hotel_en_cour):
	executable_path = {'executable_path': './chromedriver'}


	browser = Browser('chrome', headless=True)

	print(url)
	with browser:
		browser.visit(url)


		reviews = browser.find_by_css('.hotels-review-list-parts-SingleReview__reviewContainer--d54T4')
		i = 0
		for review in reviews:

			if	i == len(reviews):
				break

			user = review.find_by_css('.social-member-event-MemberEventOnObjectBlock__member--35-jC').text
			user_contribution = review.find_by_css('.social-member-MemberHeaderStats__bold--3z3qh')[0].text
			vote_utile = 0

			date_contribution_raw = str(review.find_by_css('.social-member-event-MemberEventOnObjectBlock__event_type--3njyv span').text)

			date_sejour = review.find_by_css('.hotels-review-list-parts-EventDate__event_date--CRXs4')

			print(date_sejour.text)

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

			reponse_proprio_clean = ""

			if review.find_by_css('.hotels-review-list-parts-OwnerResponse__reviewText--28Wat'):
				reponse_proprio = ""
				reponse_proprio = review.find_by_css('.hotels-review-list-parts-OwnerResponse__reviewText--28Wat').text
				reponse_proprio_clean = reponse_proprio.replace(',', '/')
				reponse_proprio_clean = reponse_proprio_clean.replace('\n', " ")

			text_clean = text.replace(',', '/')
			text_clean = text_clean.replace('\n' , " ")




			with open("./resultat.csv", 'a', newline='') as out:
				out.write(hotel_en_cour + ","+ str(user) + "," + str(user_contribution) + "," + str(vote_utile) +  "," + str(date_contribution) + ","  + str(date_sejour_formatted) + "," + repr(text_clean) + "," + str(reponse_proprio_clean))
				out.write("\n")

			i = i + 1

		return 1

def getPageNumber(url):
	executable_path = {'executable_path': './chromedriver'}

	browser = Browser('chrome', headless=True)
	with browser:
		browser.visit(url)
		page_number = browser.find_by_css('.pageNumbers a.pageNum')
		result = page_number[len(page_number) - 1]["href"]
		number = int(re.search(r'\d+', result[60:len(result)]).group())
		step = number
		return step






def retrievelocations():
	with open("./resultat.csv", 'a', newline='') as out:
		out.write("Nom de l'hotel" + "," + "Contributeur" + "," + "Nombre_de_contributions" + "," + "Vote_utile" + "," + "date_contribution" + "," + "date_sejour" + "," + "review" + "," + "reponse_proprietaire")
		out.write("\n")


	with open('./csv/input.csv', newline='') as csvfile:
		content = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in content:
			start_time = time.time()
			url_origin = row[1]
			hotel_en_cour = row[0].replace(' ', '')

			print("hotel en cour:" + url_origin)

			step = getPageNumber(url_origin)

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
				if pagination == step:
					print("Hotel scrappé en : %s secondes ---" % (time.time() - start_time))
					print(bcolors.OKGREEN+ "Hotel scrappé ;)")
					break

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
