import json

import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin

class SinsaySpider(scrapy.Spider):
    name = "sinsay"
    allowed_domains = ["sinsay.com"]
    
    start_urls = [
        'https://www.sinsay.com/pl/pl/kobieta', 
        'https://www.sinsay.com/pl/pl/mezczyzna'
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
                        PageMethod('wait_for_selector', '#cookiebotDialogOkButton'),
                        PageMethod('click', '#cookiebotDialogOkButton'),
                        PageMethod('wait_for_selector', 'article.es-product'),
                        PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'), 
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
        
        for _ in range(5):  # Zmniejszona liczba scrollowań
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)  # Krótszy timeout
        
       
        html = await page.content()
        await page.close()

        selector = scrapy.Selector(text=html)
        
        for product in selector.css("article.es-product"):
      
            product_data = {
                "id": product.attrib.get("data-id"),
                "sku": product.attrib.get("data-sku"),
                "name": product.css("img::attr(alt)").get("").strip(),
                "product_url": urljoin(response.url, product.css("a.es-product-photo::attr(href)").get()),
                "image_urls": self.extract_image_urls(product),
                # Dodatkowe dane z data-json
                "json_data": self.extract_json_data(product)
            }
           
            if not product_data["image_urls"]:
                continue

            yield product_data

    def extract_image_urls(self, product) -> list:
        """Wyciąga wszystkie możliwe URL-e obrazków produktu"""
        urls = set()
        for img in product.css("img"):
            for attr in ["src", "data-src", "data-front", "data-back"]:
                url = img.attrib.get(attr)
                if url and "media/catalog/product" in url:
                    urls.add(url.split("?")[0])  # Usuń parametry URL
        return list(urls)

    def extract_json_data(self, product) -> dict:
        """Parsuje dane JSON z atrybutów data-*"""
        json_data = {}
        for script in product.css('script[data-json-name]'):
            json_name = script.attrib.get("data-json-name")
            if json_name and "TopWonder" in json_name:
                try:
                    json_str = script.css("::text").get()
                    if json_str:
                        json_data[json_name] = json.loads(json_str)
                except json.JSONDecodeError:
                    continue
        return json_data
    
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        if page:
            await page.close()
