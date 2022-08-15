# Scrapy settings for miyolab_crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'miyolab_crawl'

SPIDER_MODULES = ['miyolab_crawl.spiders']
NEWSPIDER_MODULE = 'miyolab_crawl.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'miyolab_crawl (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'miyolab_crawl.middlewares.MiyolabCrawlSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'miyolab_crawl.middlewares.MiyolabCrawlDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'miyolab_crawl.pipelines.MiyolabCrawlPipeline': 300,
    'miyolab_crawl.pipelines.CharacterPipeline': 301,
    'miyolab_crawl.pipelines.PropertyPipeline': 302,
    'miyolab_crawl.pipelines.WeaponPipeline': 303,
    'miyolab_crawl.pipelines.MysqlPipeline': 305,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 配置 MySQL 参数, 默认为本地 localhost
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'database name'
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'password'
MYSQL_PORT = 3306

# 跳过爬取的角色
CHARACTER_RULE = [
    '旅行者（荧）',
]

# 跳过爬取的武器
WEAPON_RULE = [
            '无锋剑', '训练大剑', '学徒笔记', '猎弓', '新手长枪',
            '银剑', '佣兵重剑', '口袋魔导书', '历练的猎弓', '铁尖枪',
            '旅行剑', '吃虎鱼刀', '暗铁剑', '冷刃', '飞天御剑',
            '白铁大剑', '飞天大御剑', '沐浴龙血的剑', '铁影阔剑',
            '翡玉法球', '异世界行记', '甲级宝珏', '魔导绪论',
            '反曲弓', '信使', '神射手之誓', '鸦羽弓',
            '钺矛',
        ]

# 有效词条模型
MODE_LIST = {
    # 攻双暴
    1: ['刻晴', '可莉', '甘雨', '魈', '神里绫华', '埃洛伊', '安柏', '菲谢尔', '雷泽', '凯亚', '凝光'],
    # 攻精双暴
    2: ['迪卢克', '达达利亚', '宵宫', '烟绯', '重云', '鹿野院平藏'],
    # 攻充双暴
    3: ['莫娜', '琴', '优菈', '雷电将军', '北斗', '罗莎莉亚', '九条裟罗'],
    # 攻精充双暴
    4: ['温迪', '八重神子', '丽莎', '香菱', '行秋'],
    # 攻精充
    5: ['早柚'],
    # 攻充
    6: ['七七', '申鹤'],
    # 生攻双暴
    7: ['神里绫人'],
    # 生攻精双暴
    8: ['胡桃'],
    # 生充双暴
    9: ['夜兰'],
    # 生攻充
    10: ['珊瑚宫心海'],
    # 生精
    11: ['久岐忍'],
    # 生充
    12: ['钟离', '班尼特', '芭芭拉', '迪奥娜', '托马'],
    # 攻防充双暴
    13: ['荒泷一斗'],
    # 防充双暴
    14: ['诺艾尔'],
    # 防双暴
    15: ['阿贝多'],
    # 防充
    16: ['辛焱', '五郎', '云堇'],
    # 精充
    17: ['旅行者（空）', '枫原万叶', '砂糖'],
}

# 突破碎屑转化元素
ELEMENT_LIST = {
    'Pyro': '燃愿玛瑙碎屑',
    'Hydro': '涤净青金碎屑',
    'Anemo': '自在松石碎屑',
    'Electro': '最胜紫晶碎屑',
    'Dendro': '生长碧翡碎屑',
    'Cryo': '哀叙冰玉碎屑',
    'Geo': '坚牢黄玉碎屑',
}

TYPE_LIST = {
    'Sword': ['单手剑', '装备类型：单手剑'],
    'Claymore': ['双手剑', '装备类型：双手剑'],
    'Catalyst': ['法器', '装备类型：法器'],
    'Bow': ['弓', '装备类型：弓'],
    'Polearm': ['长柄武器', '装备类型：长柄武器'],
}
