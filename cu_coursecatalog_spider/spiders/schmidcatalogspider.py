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

	# In charge of processing the response and returning the scraped data as objects
	def parse(self, response):
		empty = []
		emptyStr = ''
		ignore = u'\r\n'
		nbsp = u'\xa0'

		# Get department name
		department = response.xpath('//h1[1]/text()').extract()[0]

		# Used to get major names
		descs = []
		reqs = []
		# For each major name
		for selector in response.xpath('//h2[contains(text(), \'Bachelor of\')]'):
			# Get major name
			majorTitle = selector.xpath('text()').extract()[0]
			print majorTitle
			# Reset subHeadingStr
			subHeadingStr = ''

			# For each p and table tag that is after the h2 tag containing the majorTitle but before the next h2 tag
			for sel in response.xpath('//*[(name()=\'p\' or name()=\'table\') and (preceding-sibling::h2[1][.=\''+majorTitle+'\'])]'):

				# use this for descriptions, subHeadings, subHeading addenums, but not anything that has an ignore (\r\n)
				info = sel.xpath('descendant-or-self::*/text()').extract()
				# Join parts together to make a unicode string
				info = ''.join(info)
				# Encode string as utf-8 for serialization
				info = info.encode('utf-8')

				# Any links inside the text
				links = sel.xpath('a/text()').extract()

				# The subheading (e.g. requirements, electives, etc.)
				subHeading = sel.xpath('span/text()').extract()

				# Any paragraph description of the major, or subHeading text to be added
				description = sel.xpath('text()').extract()

				# Array containing subjects, or description with or without links that come after the subHeading
				tableTxt = sel.xpath('tr/td')

				# If there are links then they must be put into the description
				if links != empty:
					descs.append(info)

				# Subheading usually is accompanied by a description (e.g. subHeading = '(requirements' & description = ' 42 credits)')
				elif subHeading != empty and description != empty:
					space = ''
					if subHeadingStr != emptyStr and subHeadingStr[-1] != ' ' and info[0] != ' ':
						space = ' '
					subHeadingStr = subHeadingStr + space + info

				# If the description is not empty then it usually is an addition to the subheading (e.g. 'three of the following')
				elif description != empty:
					if ignore not in description:
						# Trailing/preceding space check
						if subHeadingStr != emptyStr:
							space = ''
							if subHeadingStr[-1] != ' ' and info[0] != ' ':
								space = ' '
							subHeadingStr = subHeadingStr + space + info
						else:
							descs.append(info)

				# Add the subHeading if it's not accompanied by a description
				elif subHeading != empty:
					descs.insert(len(descs), subHeading[0].encode('utf-8'))

				# If tableTxt is encountered, the subHeadingStr is added before the tableTxt
				if tableTxt != empty:
					# Fix for table description that doesn't have any links
					tableSel = tableTxt.xpath('p/a/text()')
					if tableSel == empty or tableSel == None:
						tableSel = tableTxt.xpath('p/text()').extract()
						tableDesc = ''
						for uTxt in tableSel:
							if nbsp not in uTxt:
								tableDesc += ' ' + uTxt.encode('utf-8')
						print 'tableDescNoLink: ', tableDesc
						stripChars  = ' '
						if subHeadingStr != emptyStr:
							reqs.insert(len(reqs), subHeadingStr)
							stripChars += subHeadingStr[-11] + subHeadingStr[-10]
							subHeadingStr = ''
						reqs.insert(len(reqs), tableDesc.strip(stripChars))

					# If the table consists of a list of subjects or is a description with links
					else:

#### could check if ignore not in the text because that will rule out the list of subjects??

						tableDesc = tableTxt.xpath('p/text()').extract()
						tableSel = tableSel.extract()
						if subHeadingStr != emptyStr:
							reqs.insert(len(reqs), subHeadingStr)
							subHeadingStr = ''
						descHack = True
						for i in range(len(tableSel)):
							if nbsp in tableDesc[i]:
								descHack = False
								# special condition where its a description with links
								tableDesc = tableTxt.xpath('p/text()').extract()
								del tableDesc[0]
								del tableDesc[-1]
								print tableDesc
								print tableSel
								for j in range(len(tableSel)):
									tableDesc.insert((2*j)+1, tableSel[j].encode('utf-8'))
								tableDesc = ''.join(tableDesc)
								tableSel = tableDesc
								break
							tableSel[i] = tableSel[i].encode('utf-8')
						if descHack and reqs != empty and isinstance(reqs[-1], list):
							if descs != empty:
								reqs.append(descs[-1])
								del descs[-1]
						if tableTxt.xpath('p[@class=\'chartcredits\']') != empty:
							reqs.append(tableSel)
						else:
							d = tableTxt.xpath('descendant-or-self::*/text()').extract()
							for i in range(len(d)):
								if ignore in d[i]:
									d[i] = d[i].replace(ignore, '')
							d = ''.join(d)
							d = d.encode('utf-8')
							descs.append(d)
						print 'subjList or descWithLink: ', tableSel
				print 'subHeadingStr: ', subHeadingStr
				print 'links: ', links
				print 'subHeading: ', subHeading
				print 'desc: ', description
				print
			print descs
			print reqs
			yield Major(title=majorTitle, department=department, description=descs, requirements=reqs)
			descs = []
			reqs = []

		# Used to get minor names
		# descs = []
		# reqs = []
		# for selector in response.xpath('//h3[re:test(., \'Minor in\', \'i\')]'):
		# 	minorTitle = selector.xpath('text()').extract()[0]
		# 	subHeadingStr = ''
		# 	for sel in selector.xpath('//*[(name()=\'p\' or name()=\'table\') and (preceding-sibling::h3[1][.=\''+minorTitle+'\'])]'):
		# 		links = sel.xpath('a/text()').extract()
		# 		subHeading = sel.xpath('span/text()').extract()
		# 		description = sel.xpath('text()').extract()
		# 		tableTxt = sel.xpath('tr/td')
		# 		# If there are links then they must be put into the description
		# 		if links != empty:
		# 			# Fix for links that are not adding if it's the first index
		# 			offset = 1
		# 			if description[0].encode('utf-8').startswith('–'):
		# 				offset = 0
		# 			for i in range(len(links)):
		# 				description.insert((2*i)+offset, links[i])
		# 			description = ''.join(description)
		# 			descs.insert(len(descs), description.encode('utf-8'))
		# 		elif subHeading != empty and description != empty:
		# 			for i in range(0, len(subHeading)):
		# 				subHeadingStr = subHeadingStr + subHeading[i] + description[i]
		# 		elif description != empty:
		# 			if ignore not in description:
		# 				if subHeadingStr != emptyStr:
		# 					subHeadingStr = subHeadingStr + ' ' + description[0]
		# 				else:
		# 					descs.insert(len(descs), description[0].encode('utf-8'))
		# 		elif subHeading != empty:
		# 			descs.insert(len(descs), subHeading[0].encode('utf-8'))
		# 		if tableTxt != empty:
		# 			# Fix for table description that doesn't have any links
		# 			tableSel = tableTxt.xpath('p/a/text()')
		# 			if tableSel == empty or tableSel == None:
		# 				tableSel = tableTxt.xpath('p/text()').extract()
		# 				tableDesc = ''
		# 				for uTxt in tableSel:
		# 					if nbsp not in uTxt:
		# 						tableDesc += ' ' + uTxt.encode('utf-8')
		# 				print tableDesc
		# 				reqs.insert(len(reqs), tableDesc.strip(' '))

		# 			# If the table consists of a list of subjects or is a description with links
		# 			else:
		# 				tableDesc = tableTxt.xpath('p/text()').extract()
		# 				tableSel = tableSel.extract()
		# 				reqs.insert(len(reqs), subHeadingStr.encode('utf-8'))
		# 				subHeadingStr = ''
		# 				for i in range(len(tableSel)):
		# 					if nbsp in tableDesc[i]:
		# 						# special condition where its a description with links
		# 						tableDesc = tableTxt.xpath('p/text()').extract()
		# 						del tableDesc[0]
		# 						del tableDesc[-1]
		# 						print tableDesc
		# 						print tableSel
		# 						for j in range(len(tableSel)):
		# 							tableDesc.insert((2*j)+1, tableSel[j].encode('utf-8'))
		# 						tableDesc = ''.join(tableDesc)
		# 						tableSel = tableDesc
		# 						break
		# 					tableSel[i] = tableSel[i].encode('utf-8')
		# 				reqs.insert(len(reqs), tableSel)
		# 				print tableSel
		# 		print subHeadingStr
		# 		print links
		# 		print subHeading
		# 		print description
		# 		print
		# 	print descs
		# 	print reqs
		# 	yield Minor(title=minorTitle, department='Schmid College of Science and Technology', description=descs, requirements=reqs)
		# 	descs = []
		# 	reqs = []

		# # Used to get courses
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
