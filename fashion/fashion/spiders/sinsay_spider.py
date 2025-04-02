import scrapy
import json
from urllib.parse import urlencode

class SinsayAPISpider(scrapy.Spider):
    name = "sinsay"
    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
        'DOWNLOAD_DELAY': 0.25,
        'RETRY_TIMES': 3,
        'FEED_EXPORT_FIELDS': ['id', 'sku', 'photoDescription', 'image_url', 'name', 'url'],
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    def start_requests(self):
        base_url = "https://arch.sinsay.com/api/17/category/66593/productsWithoutFilters"
        base_params = {
            'filters[sortBy]': 3,
            'pageSize': 100, 
            'flags[producttilewithpreview]': 'true'
        }

        yield scrapy.Request(
            url=f"{base_url}?{urlencode({**base_params, 'offset': 0, 'pageSize': 1})}",
            callback=self.parse_total,
            meta={'base_url': base_url, 'base_params': base_params}
        )

    def parse_total(self, response):
        try:
            data = json.loads(response.text)
            total_products = data.get('productsTotalAmount', 21000)
            base_url = response.meta['base_url']
            base_params = response.meta['base_params']

            for offset in range(0, total_products, 100):
                yield scrapy.Request(
                    url=f"{base_url}?{urlencode({**base_params, 'offset': offset, 'pageSize': 100})}",
                    callback=self.parse_products
                )
        except json.JSONDecodeError:
            self.logger.error("Błąd parsowania odpowiedzi API")

    def parse_products(self, response):
        try:
            data = json.loads(response.text)
            
            for product in data.get('products', []):
                yield {
                    'id': product.get('id'),
                    'sku': product.get('sku'),
                    'photoDescription': product.get('photoDescription', ''),
                    'image_url': self.extract_original_image(product),
                    'name': product.get('name'),
                    'url': product.get('url')
                }
        except json.JSONDecodeError:
            self.logger.error(f"Błąd parsowania produktów: {response.url}")

    def extract_original_image(self, product):
        """Wyciąga pierwszy oryginalny obrazek z galerii"""
        if not product.get('gallery'):
            return None
            
        for image in product['gallery']:
            if image.get('type') == 'photo' and image.get('sizes', {}).get('original'):
                return image['sizes']['original']
        
        return None
