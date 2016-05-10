# import the necessary packages
from cu_coursecatalog_spider.items import SchmidCatalog
import scrapy

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
		for sel in response.xpath('//p//span//a'):
			major = sel.xpath('@title').extract()
			sample = sel.xpath('text()').extract()
			link = sel.xpath('@href').extract()
			print major
			print sample
			print link
			print "\n"

	# def parse_page(self, response):
	# 	# loop over all links in the page that contain
	# 	# "Bachelor of Science In "
	# 	response.xpath('//p//span//a/@title').extract()
	# 	#for data in response.xpath("//h1)

