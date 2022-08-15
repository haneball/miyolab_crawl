# miyolab_crawl

#### 介绍
基于Scrapy开发的爬虫，用于爬取米游社的角色、武器的数据。


#### 安装
安装Python依赖的库: Scrapy、PyMySQL。

```
pip install -r requirements.txt
```
建议使用3.6+以上的Python版本。


#### 运行

1. 移至项目的目录位置，
```
cd miyolab_crawl
```
2. 使用以下命令运行爬虫
```
scrapy crawl miyolab_spider
```


#### 参数说明

在 miyolab_crawl 下的 setting.py 文件中有以下几个可选配置参数
1. CHARACTER_RULE 跳过爬取的角色；
2. WEAPON_RULE 跳过爬取的武器；
3. MODE_LIST 角色的有效词条模型列表；
4. ELEMENT_LIST 用于将「燃愿玛瑙碎屑」等突破碎屑名称转换为对应的元素名称（观测枢部分角色不显示神之眼的元素，故采用此法获取）；
5. TYPE_LIST 用于将武器类型转换为所需的格式。


#### 注意事项

1. 爬虫运行前，请务必确保已经在MySQL中创建了对应的数据库、数据表并连接MySQL；
1. 若进行多次爬取，请先将数据表的数据迁出或清空，否则会因为主键重复而报错。

