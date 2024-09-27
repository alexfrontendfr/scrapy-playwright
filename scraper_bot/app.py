from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import threading
import os
import json
from utils.cache_manager import cache_manager

app = Flask(__name__)

# Global variable to store search results
results_data = []

def run_spider(spider_name, query, limit, use_tor):
    global results_data
    
    # Check cache first
    cached_results = cache_manager.get_cached_results(query, spider_name)
    if cached_results:
        results_data = cached_results
        return

    process = CrawlerProcess(get_project_settings())
    
    try:
        process.crawl(spider_name, query=query, limit=int(limit), use_tor=use_tor)
        process.start()
        
        # Load the results from the generated JSON file
        if os.path.exists('output.json'):
            with open('output.json', 'r') as f:
                results_data = json.load(f)
        else:
            results_data = []
        
        # Cache the results
        cache_manager.cache_results(query, spider_name, results_data)
    except Exception as e:
        print(f"Error running spider: {e}")
        results_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.form
    query = data.get('query')
    engine = data.get('engine')
    limit = data.get('limit', 10)
    use_tor = data.get('use_tor', 'false')

    # Run the spider in a separate thread to avoid blocking the web UI
    spider_name = f"{engine}_spider"
    thread = threading.Thread(target=run_spider, args=(spider_name, query, int(limit), use_tor))
    thread.start()
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    global results_data
    return jsonify(results_data)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)