import scrapy
from scrapy import Request
from miyolab_crawl.items import CharacterItem, PropertyItem, WeaponItem


class MiyolabSpiderSpider(scrapy.Spider):
    name = 'miyolab_spider'
    allowed_domains = ['bbs.mihoyo.com']
    start_url = [
        'https://bbs.mihoyo.com/ys/obc/channel/map/189/25?bbs_presentation_style=no_header',
        'https://bbs.mihoyo.com/ys/obc/channel/map/189/5?bbs_presentation_style=no_header',
    ]
    detail_url = 'https://bbs.mihoyo.com'

    def start_requests(self):
        # 生成爬取角色数据的请求
        yield Request(
            url=self.start_url[0],
            callback=self.parse_char
        )
        # 生成爬取武器数据的请求
        yield Request(
            url=self.start_url[1],
            callback=self.parse_weapon
        )

    def parse_char(self, response):
        character_rule = self.settings.get('CHARACTER_RULE')
        char_path_list = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/ul/li/div/ul/li[1]/div/div/a/@href').extract()
        name_list = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/ul/li/div/ul/li[1]/div/div/a/div[2]/text()').extract()
        character_id = 1
        for i in range(len(char_path_list)):
            if name_list[i] in character_rule:
                continue
            detail_url = self.detail_url + char_path_list[i]
            yield Request(
                url=detail_url,
                callback=self.parse_char_detail,
                meta={'character_id': character_id, 'name': name_list[i]}
            )
            character_id += 1

    def parse_weapon(self, response):
        weapon_rule = self.settings.get('WEAPON_RULE')
        weapon_path_list = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/ul/li/div/ul/li[1]/div/div/a/@href').extract()
        name_list = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/ul/li/div/ul/li[1]/div/div/a/div[2]/text()').extract()
        weapon_id = 1
        for i in range(len(weapon_path_list)):
            if name_list[i] in weapon_rule:
                continue
            detail_url = self.detail_url + weapon_path_list[i]
            yield Request(
                url=detail_url,
                callback=self.parse_weapon_detail,
                meta={'weapon_id': weapon_id}
            )
            weapon_id += 1

    def parse_char_detail(self, response):
        character_item = CharacterItem()
        character_item['id'] = int(response.meta.get('character_id'))
        character_item['name'] = ''.join(response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[1]/h1/text()').extract()).strip()
        character_item['element'] = ''.join(response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[1]/table/tbody[1]/tr/td[2]/ul/li[1]/div/a/span/text()').extract()).strip()
        if character_item['element'] == '':
            character_item['element'] = ''.join(response.xpath(
                '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[1]/table/tbody[1]/tr/td[2]/ul/li[1]/div/a/span/text()').extract()).strip()
        character_item['type'] = ''.join(response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/text()').extract()).strip()
        character_item['mode'] = 1
        yield character_item

        # 是否继续提取角色的三维数据?
        for i in range(6, 9):
            property_item = PropertyItem()
            pattern = self.get_pattern(response.meta.get('name'), i)
            property_item['name_id'] = response.meta.get('character_id')
            property_item['Lv'] = (i + 1) * 10
            property_item['baseHP'] = ''.join(response.xpath(pattern[0]).extract()).strip()
            property_item['baseATK'] = ''.join(response.xpath(pattern[1]).extract()).strip()
            property_item['baseDEF'] = ''.join(response.xpath(pattern[2]).extract()).strip()
            yield property_item

    def parse_weapon_detail(self, response):
        weapon_item = WeaponItem()
        weapon_item['id'] = response.meta.get('weapon_id')
        weapon_item['name'] = ''.join(response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[1]/td[2]/text()').extract()).strip()
        weapon_item['baseATK'] = ''.join(response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[2]/div/div[1]/div[3]/div/ul[2]/li[8]/table/tbody/tr/td[1]/ul/li[1]/text()').extract()).strip()
        weapon_item['type'] = ''.join(response.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/table/tbody/tr[2]/td/text()').extract()).strip()
        yield weapon_item

    def get_pattern(self, name, n):
        """生成提取角色三维数据的xpath规则"""
        char1 = ['莫娜', '琴', '七七', '温迪', '枫原万叶', '神里绫华', '雷电将军', '安柏', '芭芭拉', '行秋', '菲谢尔', '雷泽', '重云', '迪奥娜', '罗莎利亚']
        pattern = []
        if name == '旅行者（空）':
            if n < 8:
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[1]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[3]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[1]/td[4]/div/span/text()')
            if n == 8:
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[1]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[1]/td[4]/div/span/text()')
            return pattern
        elif name == '罗莎莉亚':
            if n < 8:
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[2]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[4]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[2]/td[4]/div/span/text()')
            if n == 8:
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[3]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[4]/div/span/text()')
            return pattern
        if name in char1:
            if n < 8:
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[2]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[5]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[{n}]/table/tbody[2]/tr[3]/td[4]/div/span/text()')
            if n == 8:
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[3]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[4]/div/span/text()')
            return pattern
        else:
            if n < 8:
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[{n}]/table/tbody[2]/tr[3]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[{n}]/table/tbody[2]/tr[5]/td[2]/div/span/text()')
                pattern.append(f'//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[{n}]/table/tbody[2]/tr[3]/td[4]/div/span/text()')
            if n == 8:
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[8]/table/tbody[2]/tr[3]/td[2]/div/span/text()')
                pattern.append('//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[1]/div[2]/div/div/ul[2]/li[8]/table/tbody[2]/tr[2]/td[4]/div/span/text()')
            return pattern
