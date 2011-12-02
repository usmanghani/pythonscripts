from scrapy.spider import BaseSpider
from scrapy.http import Request
from dli.items import DliMetaItem
from scrapy import log
from scrapy.conf import settings

import BeautifulSoup

class DliSpider(BaseSpider):
	# override the base class attributes.
	name = "dliSpider"
	allowed_domains = ["www.new1.dli.ernet.in"]
	baseUrl = "http://www.new1.dli.ernet.in/cgi-bin/advsearch_db.cgi?listStart=%d&language1=Urdu&perPage=%d"
	start_urls = ["http://www.new1.dli.ernet.in/cgi-bin/advsearch_db.cgi?listStart=0&language1=Urdu&perPage=20"]
	
	# these are our local instance variables.
	currentIndex = 0
	stepSize = 20
	stopIndex = 2000
	
	# Extract partial meta data from book list.
	def extractItems(self, response):
		# we keep this dictionary for partially filled items. 
		temp_items = {}
		item = DliMetaItem()
		soup = BeautifulSoup.BeautifulSoup(response.body)
		table = soup.find('table', width='90%')
		rows = table.findAll('tr')
		for row in rows:
			cell = row.find('td')
			if not cell:
				continue
			anchorTag = cell.find('a')
			if anchorTag and anchorTag.attrMap:
				item.metadataLink = anchorTag.attrMap['href']
			metaText = cell.findAll(text=True)
			item['pages'] = metaText[1].split('.')[-2].strip('\n \t') # -1 is empty since there is a dot at the end.
			item['title'] = metaText[0]
			item['barcode'] = metaText[1].lstrip(', ')
			self.temp_items[item['barcode']] = item
		return temp_items
		
	def extractMetadata(self, response, items):
		localDict = {}
		soup = BeautifulSoup.BeautifulSoup(response.body)
		table = soup.find('table', height='157')
		rows = table.findAll('tr')
		for row in rows:
			cells = row.findAll('td')
			if not cells:
				continue
			allText = cells[0].findAll(text=True)
			colname = allText[1].strip()
			allText = cells[1].findAll(text=True)
			colvalue = allText[0].strip()
			localDict[colname] = colvalue
		
		selected_item = items[localDict['Barcode']]
		# yayy, we found the item.
		if selected_item:
			item['author'] = (localDict['Author'] or localDict['Author1'] or localDict['Author2'])
			item['subject'] = localDict['Subject']
			item['language'] = localDict['Language']
			item['year'] = localDict['Year']
			item['readerLinks'] = [localDict['BookReader-1'], localDict['BookReader-2'], localDict['BookReader-3']]
		
		return selected_item
		
	def parse(self, response):
        # filename = response.url.split("/")[-2]
        # open(filename, 'wb').write(response.body)
		log.msg(response.url, level=log.INFO)
		log.msg(settings['ROOT_STORAGE_DIR'], level=log.INFO)
		log.msg(settings['FEED_URI'], level=log.INFO)
		log.msg(settings['FEED_FORMAT'], level=log.INFO)
		
		items = self.extractItems(response)
		for item in items:
			yield item.metadatalink
		self.extractMetadata(response, items)
		# This is the collection stage.
		if self.currentIndex <= self.stopIndex:
			self.currentIndex += self.stepSize
			return Request(self.baseUrl % (self.currentIndex, self.stepSize), callback=self.parse)
		else: # This is the phase when we completely fill the metadata.
			# start yielding meta data links now.
			for item in self.temp_items:
				yield Request(item.metadataLink, callback=self.parse)
			
			# done with all meta data now. Once we have this, we can start downloading the actual data.
			for item in self.temp_items:
				for link in getContentLinks(item):
					yield Request(link, callback=self.parse)
