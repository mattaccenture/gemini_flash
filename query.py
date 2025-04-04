from google.cloud import bigquery

client = bigquery.Client()

table_id = "acn-daipl.fashion_product.products"

job_config = bigquery.LoadJobConfig( 
    autodetect=True, 
    ignore_unknown_values=True, 
    max_bad_records=10,
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
)

uri = 'gs://acn-daipl-fashion-products/scraped_fashion_products/products.json'

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
) 

load_job.result()  

destination_table = client.get_table(table_id)  
print("Loaded {} rows.".format(destination_table.num_rows))
