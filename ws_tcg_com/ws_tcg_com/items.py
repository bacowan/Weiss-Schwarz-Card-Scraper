import scrapy


class WsTcgComItem(scrapy.Item):
    CardName = scrapy.Field()
    CardNameJapanese = scrapy.Field()
    CardNo = scrapy.Field()
    Expansion = scrapy.Field()
    CardType = scrapy.Field()
    Level = scrapy.Field()
    Power = scrapy.Field()
    Trigger = scrapy.Field()
    Rarity = scrapy.Field()
    Side = scrapy.Field()
    Color = scrapy.Field()
    Cost = scrapy.Field()
    Soul = scrapy.Field()
    SpecialAttribute = scrapy.Field()
    Text = scrapy.Field()
    FlavorText = scrapy.Field()
    ImageLink = scrapy.Field()