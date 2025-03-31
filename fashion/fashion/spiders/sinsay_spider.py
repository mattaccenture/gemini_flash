import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin

class SinsaySpider(scrapy.Spider):
    name = "sinsay"
    allowed_domains = ["sinsay.com"]
    start_urls = [
        "https://www.sinsay.com/pl/pl/kobieta",
        "https://www.sinsay.com/pl/pl/mezczyzna"
    ]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False, 
            "timeout": 60 * 1000, 
        },
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "article.es-product"),
                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 3000), 
                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 3000),
                    ],
                    "playwright_include_page": True,
                },
                callback=self.parse,
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        for _ in range(10):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000) 

        html = await page.content()
        await page.close()

        selector = scrapy.Selector(text=html)
        
        for product in selector.css("article.es-product"):
            urls = self.extract_image_urls(product)

            if len(urls) == 0:
                continue

            yield {
                #"name": product.css("figcaption::text").get().strip(),
                "image_urls": urls,
                "product_url": urljoin(response.url, product.css("a.es-product-photo::attr(href)").get()),
            }

    def extract_image_urls(self, product):
        urls = []
        for img in product.css("img"):
            for attr in ["src", "data-src", "data-front", "data-original"]:
                url = img.attrib.get(attr)
                if url and "media/catalog/product" in url:
                    urls.append(url.split("?")[0])  
        return list(set(urls)) 

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        if page:
            await page.close()
