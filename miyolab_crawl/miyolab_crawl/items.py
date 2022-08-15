# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class MiyolabCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CharacterItem(scrapy.Item):
    table = 'gs_app_character'    # MySQL表名
    id = Field()
    name = Field()
    element = Field()
    type = Field()
    mode = Field()


class PropertyItem(scrapy.Item):
    table = 'gs_app_property'   # MySQL表名
    id = Field()
    name_id = Field()   # 角色的外键
    Lv = Field()
    baseHP = Field()
    baseATK = Field()
    baseDEF = Field()


class WeaponItem(scrapy.Item):
    table = 'gs_app_weapon'    # MySQL表名
    id = Field()
    name = Field()
    baseATK = Field()
    type = Field()
