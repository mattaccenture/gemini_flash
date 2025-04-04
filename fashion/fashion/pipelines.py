# W pipelines.py
from google.cloud import storage
import json


class DuplicatesPipeline:
    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        url = item.get('url')  

        if not url:
            return item  

        if url in self.seen_urls:
            spider.logger.debug(f"Skipped duplicate: {url}")
            return None 
        else:
            self.seen_urls.add(url)
            return item


class GCSUploadPipeline:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.buffer = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(bucket_name=crawler.settings.get('GCS_BUCKET_NAME'))

    def open_spider(self, spider):
        spider.logger.info(f"Preparing spider, BUCKET_NAME={self.bucket_name}")
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
        self.blob = self.bucket.blob('scraped_fashion_products/products.json')

    def process_item(self, item, spider):
        if item is None:
            return

        self.buffer.append(dict(item))  
        return item

    def close_spider(self, spider):
        with self.blob.open("w") as f:
            for item in self.buffer:
                spider.logger.info('Writing data to the bucket')
                f.write(json.dumps(item) + "\n") 
