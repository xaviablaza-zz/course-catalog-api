# -*- coding: utf-8 -*-
# import the necessary packages
from cu_coursecatalog_spider.items import Course, Major, Minor
import scrapy
import json

# Spider used to crawl through the webpage and get info
class SchmidCatalogSpider(scrapy.Spider):

	# Name of the spider
	name = "schmid-catalog-spider"

	# URLs of each school's catalog
	start_urls = [
		'https://www.chapman.edu/catalog/oc/current/ug/content/8174.htm', # Schmid College
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/3610.htm', # Argyros School
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/3695.htm', # College of Education
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/3807.htm', # Dodge College
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/9075.htm', # Crean College
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/3910.htm', # Wilkinson College
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/7580.htm', # College of Performing Arts
		# 'https://www.chapman.edu/catalog/oc/current/ug/content/12155.htm', # School of Pharmacy
	]

	# Used to click a link on a page
	# From tutorial: http://www.pyimagesearch.com/2015/10/12/scraping-images-with-python-and-scrapy/
	# def parse(self, response):
	# 	# Gets node with link that has title "TIME U.S."
	# 	url = response.css("div.refineCol ul li").xpath("a[contains(., 'TIME U.S.')]")

	# 	# HTTP Request with URL of request and callback function parse_page
	# 	yield scrapy.Request(url.xpath("@href").extract_first(), self.parse_page)

	# In charge of processing the response and returning the scraped data as objects
	def parse(self, response):
		empty = []
		ignore = u'\r\n'

		# Used to get major names
		descs = []
		reqs = []
		for selector in response.xpath('//p/span/a'):
			majorTitle = selector.xpath('@title').extract()[0]
			print majorTitle
			subHeadingStr = ''
			for sel in response.xpath('//*[(name()=\'p\' or name()=\'table\') and (preceding-sibling::h2[1][.=\''+majorTitle+'\'])]'):
				links = sel.xpath('a/text()').extract()
				subHeading = sel.xpath('span/text()').extract()
				description = sel.xpath('text()').extract()
				tableTxt = sel.xpath('tr/td/p/a/text()').extract()
				# If there are links then they must be put into the description
				if links != empty:
					for i in range(len(links)):
						description.insert((2*i)+1, links[i])
					description = ''.join(description)
					descs.insert(len(descs), description.encode('utf-8'))
				elif subHeading != empty and description != empty:
					subHeadingStr += subHeading[0] + description[0]
				elif subHeading != empty:
					descs.insert(len(descs), subHeading[0].encode('utf-8'))
				elif description != empty:
					if ignore not in description:
						descs.insert(len(descs), description[0].encode('utf-8'))
				if tableTxt != empty:
					reqs.insert(len(reqs), subHeadingStr.encode('utf-8'))
					subHeadingStr = ''
					for subj in tableTxt:
						subj = subj.encode('utf-8')
					reqs.insert(len(reqs), tableTxt)
				# print links
				# print subHeading
				# print description
				# print tableTxt
				# print
			print descs
			print reqs
			descs = []
			reqs = []
			# yield Major(title=major1, department='Schmid College of Science and Technology')

		# Used to get minor names
		# for sel in response.xpath('//h3[re:test(., \'Minor in\', \'i\')]'):
		# 	minorTitle = sel.xpath('text()').extract()[0][9:]
		# 	yield Minor(title=minorTitle, department='Schmid College of Science and Technology')

		# Used to get courses
		# subject = ''
		# number = -1
		# name = ' '
		# heading = True
		# for sel in response.xpath('//*[(name()=\'h3\' and re:test(., \'^((?!Minor in).)*$\', \'i\')) or (name()=\'p\' and @class=\'coursedescription\')]'):
		# 	if (heading == True):
		# 		courseStr = sel.xpath('text()').extract()[0]
		# 		courseStr = courseStr.split()
		# 		name = ' '.join(courseStr[2:])
		# 		subject = courseStr[0]
		# 		number = courseStr[1]
		# 		heading = False
		# 	else:
		# 		prerequisites = sel.xpath('a/text()').extract()
		# 		description = sel.xpath('text()').extract()
		# 		if (prerequisites != empty):
		# 			for i in range(len(prerequisites)):
		# 				description.insert((2*i)+1, prerequisites[i])
		# 		description = ''.join(description)
		# 		heading = True
		# 		yield Course(subject=subject, number=number, name=name, description=description)

		# print json.dumps({"c":0, "b":0, "a":0}, sort_keys=True)

	# def parse_page(self, response):
	# 	# loop over all links in the page that contain
	# 	# "Bachelor of Science In "
	# 	response.xpath('//p//span//a/@title').extract()
	# 	#for data in response.xpath("//h1)

