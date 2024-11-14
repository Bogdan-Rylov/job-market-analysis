import scrapy


class DouVacanciesSpider(scrapy.Spider):
    name = "dou_vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/"]

    def parse(self, response):
        pass
