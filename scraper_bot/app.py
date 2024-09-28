import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, flash
import threading
import asyncio
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Queue, Process
import json
from utils.cache_manager import cache_manager
from utils.result_processor import process_results
from spiders.google_spider import GoogleSpider
from spiders.bing_spider import BingSpider
from spiders.duckduckgo_spider import DuckDuckGoSpider
from spiders.onion_spider import OnionSpider
from spiders.keyword_spider import KeywordSpider
from scraper_bot.utils.progress_tracker import ProgressTracker

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# Global variable to store search results
results_data = []
scraping_status = {'is_scraping': False, 'progress': 0}


progress_tracker = ProgressTracker()

def run_spider_in_thread(spider_class, query, limit, use_tor):
    global results_data, scraping_status
    
    try:
        # Check cache first
        cached_results = cache_manager.get_cached_results(query, spider_class.name)
        if cached_results:
            results_data = cached_results[:limit]
            scraping_status = {'is_scraping': False, 'progress': 100}
            return

        scraping_status = {'is_scraping': True, 'progress': 0}
        
        def f(q):
            try:
                runner = CrawlerRunner()
                deferred = runner.crawl(spider_class, query=query, limit=limit, use_tor=use_tor, progress_tracker=progress_tracker)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run(installSignalHandlers=0)
                q.put(None)
            except Exception as e:
                q.put(e)

        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        
        while p.is_alive():
            scraping_status['progress'] = progress_tracker.get_progress()
            time.sleep(0.5)
        
        result = q.get()
        p.join()

        if result is not None:
            raise result

        results_data = process_results('output.json')[:limit]
        cache_manager.cache_results(query, spider_class.name, results_data)
        scraping_status = {'is_scraping': False, 'progress': 100}
    except Exception as e:
        app.logger.error(f"Error running spider: {e}")
        flash(f"An error occurred while scraping: {str(e)}", 'error')
        results_data = []
        scraping_status = {'is_scraping': False, 'progress': 0}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.form
    query = data.get('query')
    engine = data.get('engine')
    limit = int(data.get('limit', 10))
    use_tor = data.get('use_tor', 'false').lower() == 'true'

    spider_class = {
        'google': GoogleSpider,
        'bing': BingSpider,
        'duckduckgo': DuckDuckGoSpider,
        'onion': OnionSpider,
        'keyword': KeywordSpider
    }.get(engine)

    if not spider_class:
        flash(f"Invalid search engine selected: {engine}", 'error')
        return redirect(url_for('index'))

    threading.Thread(target=run_spider_in_thread, args=(spider_class, query, limit, use_tor)).start()
    return jsonify({'status': 'success'})

@app.route('/results')
def results():
    return render_template('results.html', results=results_data)

@app.route('/status')
def status():
    return jsonify(scraping_status)

@app.route('/download_results')
def download_results():
    if not results_data:
        flash("No results available for download", 'warning')
        return redirect(url_for('index'))
    
    with open('results.json', 'w') as f:
        json.dump(results_data, f)
    
    return send_file('results.json', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

