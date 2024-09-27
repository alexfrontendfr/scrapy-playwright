import json

def save_to_json(data, filename):
    """
    Save the provided data dictionary to a JSON file.
    :param data: Dictionary to save.
    :param filename: The filename for the saved JSON file.
    """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_from_json(filename):
    """
    Load data from a JSON file and return as a dictionary.
    :param filename: The filename of the JSON file.
    :return: Data loaded from the file as a dictionary.
    """
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def validate_search_query(query):
    """
    Validate a search query to ensure it is non-empty and well-formed.
    :param query: Search query string.
    :return: Cleaned and validated query string.
    :raises ValueError: If query is invalid.
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Search query cannot be empty.")
    return query.strip()

# Example usage
def process_results(results):
    """
    Process and format the scraping results.
    :param results: List of raw results.
    :return: List of formatted results.
    """
    processed_results = []
    for result in results:
        processed_results.append({
            'title': result.get('title', 'No Title'),
            'url': result.get('url', 'No URL'),
            'description': result.get('description', 'No Description')
        })
    return processed_results
