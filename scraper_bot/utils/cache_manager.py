import json
import os
import time
from typing import List, Dict, Any
import hashlib

class CacheManager:
    def __init__(self, cache_dir: str = 'search_cache', cache_duration: int = 86400):
        self.cache_dir = cache_dir
        self.cache_duration = cache_duration
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_file_path(self, query: str, engine: str) -> str:
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{engine}_{query_hash}.json")

    def get_cached_results(self, query: str, engine: str) -> List[Dict[str, Any]]:
        cache_file = self._get_cache_file_path(query, engine)
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
            if time.time() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['results']
        return []

    def cache_results(self, query: str, engine: str, results: List[Dict[str, Any]]) -> None:
        cache_file = self._get_cache_file_path(query, engine)
        with open(cache_file, 'w') as f:
            json.dump({'timestamp': time.time(), 'results': results}, f)

    def clear_expired_cache(self):
        current_time = time.time()
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    cached_data = json.load(f)
                if current_time - cached_data['timestamp'] >= self.cache_duration:
                    os.remove(file_path)

cache_manager = CacheManager()