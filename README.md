# ptt-comment-spider
A spider for collecting comments from PTT articles.

用來大量爬取 PTT 上的文章評論.

包含兩隻 scrapy 爬蟲,

一隻根據給定條件 (看板名稱, 看板起始頁, 要爬的頁數) 抓取對應的 URL,

另一隻則是從 URL 列表抓取對應文章的評論，儲存為 CSV 格式.

# Setup
pip install Scrapy

# Usage
1. Open main.py, change your setting in the `crawl` function. 

2. python main.py
