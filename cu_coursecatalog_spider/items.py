# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CuCoursecatalogSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Course(scrapy.Item):
	subject = scrapy.Field()
	number = scrapy.Field()
	name = scrapy.Field()
	description = scrapy.Field()

class Major(scrapy.Item):
	title = scrapy.Field()
	department = scrapy.Field()
	description = scrapy.Field()
	requirements = scrapy.Field()

class Minor(scrapy.Item):
	title = scrapy.Field()
	department = scrapy.Field()