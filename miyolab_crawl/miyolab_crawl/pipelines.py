# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from miyolab_crawl.items import CharacterItem, PropertyItem, WeaponItem
import re
import pymysql


class MiyolabCrawlPipeline:
    def process_item(self, item, spider):
        return item


class CharacterPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CharacterItem):
            element_list = spider.settings.get('ELEMENT_LIST')
            type_list = spider.settings.get('TYPE_LIST')
            mode_list = spider.settings.get('MODE_LIST')
            element = self.trans_element(element_list, item.get('element'))
            if element:
                item['element'] = element
            type = self.trans_type(type_list, item.get('type'))
            if type:
                item['type'] = type
            mode = self.set_mode(mode_list, item.get('name'))
            if mode:
                item['mode'] = mode
        return item

    def trans_element(self, element_list, sliver):
        element = 'Anemo'
        for key, value in element_list.items():
            if sliver == value:
                element = key
                break
        return element

    def trans_type(self, type_list, weapon):
        type = ''
        for key, value in type_list.items():
            if weapon in value:
                type = key
                break
        return type

    def set_mode(self, mode_list, name):
        mode = 0
        for key, value in mode_list.items():
            if name in value:
                mode = key
                break
        return mode

class PropertyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PropertyItem):
            re_exp = re.compile(r'\d+.?（无武器(\d+)）')
            item['baseHP'] = int(item['baseHP'].replace(',', ''))
            item['baseDEF'] = int(item['baseDEF'].replace(',', ''))
            if re.findall(re_exp, item.get('baseATK')):
                item['baseATK'] = int(re.findall(re_exp, item['baseATK'])[0])
            else:
                item['baseATK'] = int(item.get('baseATK'))
        return item


class WeaponPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeaponItem):
            re_exp1 = re.compile(r'名称：(.*)')
            re_exp2 = re.compile(r'基础攻击力: (\d+)')
            re_exp3 = re.compile(r'基础攻击力：(\d+)')
            type_list = spider.settings.get('TYPE_LIST')
            item['type'] = self.trans_type(type_list, item.get('type'))
            if re.findall(re_exp1, item.get('name')):
                item['name'] = re.findall(re_exp1, item.get('name'))
            if re.findall(re_exp2, item.get('baseATK')):
                item['baseATK'] = int(re.findall(re_exp2, item['baseATK'])[0])
                return item
            if re.findall(re_exp3, item.get('baseATK')):
                item['baseATK'] = int(re.findall(re_exp3, item['baseATK'])[0])
        return item

    def trans_type(self, type_list, weapon):
        type = ''
        for key, value in type_list.items():
            if weapon in value:
                type = key
                break
        return type


class MysqlPipeline:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
