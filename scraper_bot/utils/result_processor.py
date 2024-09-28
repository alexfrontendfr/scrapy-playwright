import json
from typing import List, Dict, Any

def process_results(file_path: str) -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'r') as f:
            results = json.load(f)
        
        processed_results = []
        for result in results:
            processed_result = {
                'title': result.get('title', '').strip(),
                'url': result.get('url', '').strip(),
                'snippet': result.get('snippet', '').strip(),
                'keywords': [kw.strip() for kw in result.get('keywords', [])],
                'tags': [tag.strip() for tag in result.get('tags', [])]
            }
            processed_results.append(processed_result)
        
        return processed_results
    except Exception as e:
        print(f"Error processing results: {e}")
        return []