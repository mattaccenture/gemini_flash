import argparse
import os
from typing import List, Dict, Any
from google.cloud import aiplatform
from google import genai
from google.genai.types import EmbedContentConfig

PROJECT_ID = os.getenv("GCP_PROJECT_ID")  
LOCATION = "europe-central2"  
INDEX_ENDPOINT_ID = "7060272025205473280"  
DEPLOYED_INDEX_ID = "ev_fashion_products_embedd_1743495505094" 

aiplatform.init(project=PROJECT_ID, location=LOCATION)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model = "gemini-2.0-flash"
 
def get_text_embedding(text: str) -> List[float]:
    """Generuje embedding tekstu za pomocą Vertex AI Text Embedding."""
    
    result = client.models.embed_content(
        model="gemini-embedding-exp-03-07", 
        contents=[text],
        config=EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY", 
            output_dimensionality=768,  
        ))
    
    embedding_values = result.embeddings[0].values

    return embedding_values 

def query_index(
    text: str,
    num_neighbors: int = 5,
    filter: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Wyszukuje podobne produkty w Matching Engine.
    
    Args:
        text: Zapytanie tekstowe
        num_neighbors: Liczba wyników do zwrócenia
        filter: Opcjonalne filtry (np. {"color": "red"})
    
    Returns:
        Lista wyników z metadanymi
    """

    query_embedding = get_text_embedding(text)
    

    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/indexEndpoints/{INDEX_ENDPOINT_ID}"
    )
    
    response = index_endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_embedding],
        num_neighbors=num_neighbors,
        filter=filter
    )
    
  
    results = []
    for neighbor in response[0]:  


        results.append({
            "id": neighbor.id,
            "distance": neighbor.distance,
            #"metadata": neighbor.metadata  
        })
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Wyszukaj podobne produkty za pomocą Vertex AI Vector Search")
    parser.add_argument("--text", required=True, help="Tekst zapytania (np. 'czerwona sukienka')")
    parser.add_argument("--num_results", type=int, default=5, help="Liczba wyników do zwrócenia")
    parser.add_argument("--filter", type=str, help="Filtr w formacie JSON (np. '{\"color\":\"red\"}')")
    
    args = parser.parse_args()
    
    filter_dict = None
    if args.filter:
        import json
        filter_dict = json.loads(args.filter)
     
    results = query_index(
        text=args.text,
        num_neighbors=args.num_results,
        filter=filter_dict
    )
     
    for i, result in enumerate(results, 1):
        print(f"#{i}: ID={result['id']}, Distance={result['distance']:.4f}")
#        print(f"   Metadata: {result['metadata']}\n")

if __name__ == "__main__":
    main()
