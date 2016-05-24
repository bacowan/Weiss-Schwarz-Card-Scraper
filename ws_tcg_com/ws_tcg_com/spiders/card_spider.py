from functools import partial
from urlparse import urljoin
import scrapy

from scrapy.selector import Selector
from ws_tcg_com.items import WsTcgComItem

class CardSpider(scrapy.Spider):
    name = "cardSpider"
    start_urls = ["http://ws-tcg.com/en/cardlist/list/"]
    
    def parse(self, response):
        a = 0
        for sel in response.xpath('//ul/li[a[@onclick]]'):
            expansionVal = sel.xpath('a/@onclick').extract()
            expansionVal = [i for i in expansionVal[0].split('\'') if i.isdigit()][0] # todo: refactor
            yield scrapy.http.FormRequest(
                "http://ws-tcg.com/en/jsp/cardlist/expansionDetail",
                callback=partial(self.parse_card_list, expansionId=expansionVal, page=1),
                formdata={"expansion_id": str(expansionVal), "page": '1'})
    
    def parse_card_list(self, response, expansionId, page):
        a = 0
        for sel in response.xpath('//table/tbody/tr/td[3]'):          
            cardLink = sel.xpath('a/@href').extract()[0]
            yield scrapy.Request("http://ws-tcg.com/en/cardlist/list/"+cardLink, self.parse_card_page)
        if page < pageCount(response):
            yield scrapy.http.FormRequest(
                "http://ws-tcg.com/en/jsp/cardlist/expansionDetail",
                callback=partial(self.parse_card_list, expansionId=expansionId, page=page+1),
                formdata={"expansion_id": str(expansionId), "page": str(page+1)})
            
    # todo: the rest of the attributes
    def parse_card_page(self, response):
        item = WsTcgComItem()
        for sel in response.xpath("//div[@id='cardDetail']/table"):
            item['CardName'] = getCellText(sel, 'Card Name')
            item['CardNameJapanese'] = Selector(text=getCell(sel, 'Card Name')).xpath('//td/span/text()[1]').extract()[0]
            item['CardNo'] = getCellText(sel, 'Card No.')
            item['Expansion'] = getCellText(sel, 'Expansion')
            item['CardType'] = getCellText(sel, 'Card Type')
            item['Level'] = getCellText(sel, 'Level')
            item['Power'] = getCellText(sel, 'Power')
            item['Trigger'] = getAllCellImageNames(sel, 'Trigger')
            item['Rarity'] = getCellText(sel, 'Rarity')
            item['Side'] = getCellImageName(sel, 'Side')
            item['Color'] = getCellImageName(sel, 'Color')
            item['Cost'] = getCellText(sel, 'Cost')
            item['Soul'] = getCellImageName(sel, 'Soul')
            item['SpecialAttribute'] = getCellText(sel, 'Special Attribute')
            item['Text'] = getCellText(sel, 'Text')
            item['FlavorText'] = getCellText(sel, 'Flavor Text')
            item['ImageLink'] = urljoin(response.url, sel.xpath("//tr/td/img/@src").extract()[0])
            yield item

def pageCount(response):
    buttonVals = response.xpath("//p[@class='pageLink']/a/text()").extract()
    return max([int(i) for i in buttonVals if i.isdigit()])
        
def getCellText(sel, title):
    val = Selector(text=getCell(sel, title)).xpath('//td/text()[1]').extract()
    if len(val) > 0:
        return Selector(text=getCell(sel, title)).xpath('//td/text()[1]').extract()[0].strip()
    return '-'

def getCellImageName(sel, title):
    return getAllCellImageNames(sel, title)[0]

def getAllCellImageNames(sel, title):
    textList = getAllCellImageLinks(sel, title)
    return [getImageNameFromImageLink(text) for text in textList]

def getImageNameFromImageLink(link):
    if link is not '-':
        return link[link.rfind('/')+1:link.rfind('.')]
    return '-'

def getCellImageLink(sel, title):
    return getAllCellImageLinks[0]

def getAllCellImageLinks(sel, title):
    val = Selector(text=getCell(sel, title)).xpath('//td/img/@src').extract()
    if len(val) > 0:
        return Selector(text=getCell(sel, title)).xpath('//td/img/@src').extract()
    return ['-'] 
        
def getCell(sel, title):
    return sel.xpath("//table/tr/th[text()='" + title + "']/following-sibling::*[1]").extract()[0]