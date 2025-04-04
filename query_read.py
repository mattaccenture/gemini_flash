from google.cloud import bigquery

client = bigquery.Client()


QUERY = (
    'select name, photoDescription, image_url, price, url  from `acn-daipl.fashion_product.products` limit 25'
)

query_job = client.query(QUERY)  
rows = query_job.result()  

for row in rows:
    print(f"{row.photoDescription}: {row.price} zł - {row.url}")

