import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from flask import Flask, render_template, request, jsonify
from scraper_bot.spiders.google_spider import GoogleSpider
from scraper_bot.spiders.bing_spider import BingSpider
from scraper_bot.spiders.duckduckgo_spider import DuckDuckGoSpider
from scraper_bot.spiders.onion_spider import OnionSpider
from scraper_bot.spiders.keyword_spider import KeywordSpider
from scraper_bot.tasks import run_spider
from scraper_bot.utils.cache_manager import cache_manager
from scraper_bot.utils.proxy_helper import tor_manager
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    engines = request.form.getlist('engines')
    limit = int(request.form.get('limit', 10))
    use_tor = request.form.get('use_tor', 'false').lower() == 'true'

    if not query:
        return jsonify({'error': 'Search query is required'}), 400

    if not engines:
        return jsonify({'error': 'At least one search engine must be selected'}), 400

    tasks = []
    for engine in engines:
        task = run_spider.delay(engine, query, limit, use_tor)
        tasks.append(task)

    return jsonify({'task_ids': [task.id for task in tasks]})

@app.route('/results/<task_id>')
def get_results(task_id):
    task = run_spider.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    cache_manager.clear_expired_cache()
    return jsonify({'status': 'Cache cleared successfully'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=False)