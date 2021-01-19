# PTT Spiders
A spiders for collecting articles and comments from PTT kanbans.

PTT爬蟲，用來大量爬取 PTT 上的文章及評論。

目前有三種 scrapy spider。

PTTSpider1: 根據給定條件 (看板名稱, 看板起始頁, 要爬的頁數) 抓取對應的文章 URL 

PTTSpider2: 從 URL 列表抓取對應文章的評論，儲存為 CSV 格式 (`egs/stock_0117/`)

PTTArticleSpider: 從給定的文章 URL 爬取文章內容 (`egs/gossip_article`)

# Setup
pip install Scrapy

# Usage
```
cp -r egs/gossip_article egs/your_task
cd egs/your_task 
mkdir data
# edit parse.py
python parse.py
```

