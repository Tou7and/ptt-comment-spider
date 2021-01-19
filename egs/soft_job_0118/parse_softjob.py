""" Collect PTT comments using Scrapy. """
import os
import time
import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

CWD = os.getcwd()

class PTTSpider1(scrapy.Spider):
    """ This Spider collects article URLs """
    name = "ptt_spider1"
    def __init__(self, board="C_Chat", start_page=17500, n_page=5, outpath=CWD+"/urls.csv"):
        super().__init__()
        self.allowed_domains = ['ptt.cc']
        self.board = board
        self.start_page = start_page
        self.n_page = n_page
        self.outpath = outpath
        self.start_urls = ['https://www.ptt.cc/bbs/{}/index.html'.format(board)]

    def parse(self, response):
        for ind in range(self.n_page):
            time.sleep(1)
            current_page = self.start_page - ind
            url = "https://www.ptt.cc/bbs/{}/index{}.html".format(self.board, str(current_page))
            yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.parse_kanban)

    def parse_kanban(self, response):
        article_list = response.xpath("//div[@class='title']")

        for article in article_list:
            try:
                title = article.xpath("a/text()")[0].extract()
                article_url = self.allowed_domains[0] + article.xpath("a/@href")[0].extract()
                # print(title, article_url)
                title = title.replace(",", "") # Remove comma, since we want a CSV
                with open(self.outpath, "a") as writer:
                    writer.write("{},{}\n".format(title, article_url))
            except Exception as error:
                self.log(error)

class PTTSpider2(scrapy.Spider):
    """ This spider collect comments from the URL list. """
    name = "ptt_spider2"
    def __init__(self, url_csv=CWD+"/urls.csv", outpath=CWD+"/comments.csv"):
        super().__init__()
        self.outpath = outpath
        self.allowed_domains = ['ptt.cc']
        # start_urls = ["https://www.ptt.cc/bbs/Gossiping/M.1606466492.A.8CA.html"]
        self.start_urls = []
        with open(url_csv, "r") as reader:
            article_lines = reader.readlines()
            for article_line in article_lines:
                self.start_urls.append("https://www."+article_line.split(",")[1].replace("\n", ""))

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.parse_article)

    def parse_article(self, response):
        """ Try to parse good and bad comments from a ptt article.
            Comments are stored in <div> sections, with class="push".
        """
        # item = ArticleItem()
        # item['title'] = response.xpath("/html/head/title/text()").extract_first()
        # item["content"] = response.xpath("//div[@id='main-content']/text()").extract()
        try:
            title = response.xpath("/html/head/title/text()").extract_first()
            comment_list = response.xpath("//div[@class='push']") #.extract()
            with open(self.outpath, 'a') as writer:
                for comment in comment_list:
                    # writer.write(remove_html_tags(comment.replace(" ", "")))
                    try:
                        tag = comment.xpath("span[@class='f1 hl push-tag']/text()")[0].extract()
                    except:
                        tag = comment.xpath("span[@class='hl push-tag']/text()")[0].extract()
                    content = comment.xpath("span[@class='f3 push-content']/text()")[0].extract()
                    # remove comma, since we use this as separator
                    content = content.replace(",", "")+"\n"
                    content = content.replace(":", "")
                    writer.write(tag+","+content)
        except Exception as error:
            self.log(error)

# running the spiders sequentially by chaining the deferreds
configure_logging({'LOG_LEVEL': 'INFO'})
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    settings = {
        "board": "Soft_Job",
        "start_page": 1600,
        "n_page": 10,
        "url_path": "data/urls.csv",
        "comment_path": "data/comments.csv"
    }
    yield runner.crawl(
            PTTSpider1,
            board=settings["board"],
            start_page=settings["start_page"],
            n_page=settings["n_page"],
            outpath=settings["url_path"])
    yield runner.crawl(
            PTTSpider2, 
            url_csv=settings["url_path"],
            outpath=settings["comment_path"])
    reactor.stop()

crawl()
reactor.run()
