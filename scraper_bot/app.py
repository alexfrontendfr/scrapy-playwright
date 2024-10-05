# scraper_bot/app.py

from flask import Flask, render_template, request, jsonify
from scraper_bot.tasks import run_spider
from scraper_bot.utils.cache_manager import cache_manager
from scraper_bot.utils.tor_manager import renew_tor_ip
import logging
from celery.result import AsyncResult

app = Flask(__name__)
app.config.from_object('scraper_bot.settings')

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
    task = AsyncResult(task_id)
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
        if task.state == 'SUCCESS':
            response['result'] = task.result
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

@app.route('/renew_tor_ip', methods=['POST'])
def renew_tor_ip_route():
    renew_tor_ip()
    return jsonify({'status': 'Tor IP renewed successfully'})

if __name__ == '__main__':
    app.run(debug=False)