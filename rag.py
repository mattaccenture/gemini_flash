import argparse
import json
import os
from typing import List, Dict, Any
import requests
from google import genai
from google.genai import types
from google.cloud import storage
from google.genai.types import EmbedContentConfig

# Few-shot examples for consistent output
FEW_SHOT_EXAMPLES = """
Example 1:
Input: Image of a red dress
Output: {"description": "A knee-length red dress with v-neckline, short sleeves, made of polyester. Features a floral pattern and slim fit silhouette. Color: bright red. Style: casual summer wear."}

Example 2:
Input: Image of blue jeans
Output: {"description": "Straight-cut blue denim jeans with five pockets and classic button fly. Material: 98% cotton, 2% elastane. Color: medium wash blue. Style: everyday casual."}

Example 3:
Input: Image of white sneakers
Output: {"description": "White leather sneakers with rubber soles and lace-up closure. Features padded collar and brand logo on the side. Color: pure white. Style: sporty casual."}
"""

def load_image_from_url(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def generate_image_description(client: genai.Client, model: str, image_bytes: bytes) -> str:
    prompt = f"""
    Analyze this clothing item and provide a detailed, structured description in JSON format.
    Follow exactly this structure and include all these fields:
    {FEW_SHOT_EXAMPLES}
    
    Your response must be valid JSON only, with these exact fields:
    - description: detailed description including key features
    - color: primary color(s)
    - material: fabric composition if visible
    - style: fashion style (e.g., casual, formal)
    - distinctive_features: special elements like patterns, cuts etc.
    """
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(
                    mime_type="image/jpeg",
                    data=image_bytes
                ),
            ],
        ),
    ]
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return response.text

def generate_embeddings(products: List[Dict[str, Any]], client: genai.Client) -> List[Dict[str, Any]]:
    """Generates embeddings for products using Gemini API"""
    embeddings = []
    
    for product in products:
        if not product.get("product_id"):
            print(f"Skipping product without ID: {product}")
            continue
        
        description = product.get("description")
        print(f"Generating embedding for: {product.get('product_id')}")
        
        try:
            result = client.models.embed_content(
                model="gemini-embedding-exp-03-07", 
                contents=[description],
                config=EmbedContentConfig(
                    task_type="SEMANTIC_SIMILARITY", 
                    output_dimensionality=768,  
                ))
            
            embedding_values = result.embeddings[0].values
            
            embeddings.append({
                'id': str(product['product_id']),
                'embedding': embedding_values,
                'metadata': {
                    "image_url": product.get("image_url"),
                    "features": product.get("features"),
                    "color": product.get("color"),
                    "material": product.get("material"),
                    "style": product.get("style"),
                    "original_name": product.get("original_name"),
                    "sku": product.get("sku")
                }
            })
            
        except Exception as e:
            print(f"Failed to generate embedding for {product['product_id']}: {str(e)}")
            continue
    
    return embeddings

def upload_to_gcs(data: List[Dict[str, Any]], bucket_name: str, destination_blob_name: str):
    """Uploads data to Google Cloud Storage as JSONL file"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
   
    jsonl_data = "\n".join(json.dumps(item) for item in data)
     
    blob.upload_from_string(jsonl_data, content_type="application/jsonl+json")
    print(f"Uploaded {len(data)} items to gs://{bucket_name}/{destination_blob_name}")

def process_products(input_file: str, number_of_products, output_file: str = None) -> List[Dict[str, Any]]:
    # Initialize clients
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-2.0-flash"
  
    print(f"Processing {number_of_products} products")

    with open(input_file, 'r') as f:
        products = json.load(f)
    
    results = []
    
    for index, product in enumerate(products):
        if index >= number_of_products and number_of_products != -1:
            break

        if not product.get('image_urls'):
            continue
            
        image_url = product['image_urls'][0]
        try:
            image_bytes = load_image_from_url(image_url)
            description_json = generate_image_description(client, model, image_bytes)
            description_data = json.loads(description_json)
            
            result = {
                'product_id': product.get('id'),
                'sku': product.get('sku'),
                'original_name': product.get('name'),
                'image_url': image_url,
                'description': description_data['description'],
                'color': description_data.get('color'),
                'material': description_data.get('material'),
                'style': description_data.get('style'),
                'features': description_data.get('distinctive_features'),
                'raw_gemini_response': description_json
            }
            results.append(result)
            
            print(f"Processed: {product.get('name')}")
            
        except Exception as e:
            print(f"Error processing {product.get('name')}: {str(e)}")
            continue
    
    # Save local JSON if output file specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate embeddings and upload to GCS
    try:
        embeddings = generate_embeddings(results, client)
        
        bucket_name = os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME environment variable not set")
            
        # Create timestamped filename
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_blob_name = f"fashion_product_embeddings/embeddings_{timestamp}.json"
        
        upload_to_gcs(embeddings, bucket_name, destination_blob_name)
        print("Successfully uploaded embeddings to GCS")
        
    except Exception as e:
        print(f"GCS upload failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Process product images with Gemini AI')
    parser.add_argument('input_file', help='Path to products JSON file')
    parser.add_argument('--output-file', help='Output file path (optional)', default=None)
    parser.add_argument('--products', help='Number of products', type=int, default=5)   
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist")
        return
    
    required_vars = ["GEMINI_API_KEY", "GCS_BUCKET_NAME"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        return
    
    results = process_products(args.input_file, args.products, args.output_file)
    print(json.dumps(results[:2], indent=2))  # Print first 2 results as sample

if __name__ == "__main__":
    main()
