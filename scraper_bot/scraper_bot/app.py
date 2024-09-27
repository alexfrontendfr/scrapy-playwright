import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
from threading import Thread
from time import sleep

app = Flask(__name__)

# Global variables to track progress and search limit
progress = 0
search_limit = 0

# Function to simulate search progress for demonstration purposes
def simulate_progress(limit):
    global progress
    progress = 0
    for i in range(limit):
        sleep(1)
        progress += (100 // limit)

@app.route('/', methods=['GET', 'POST'])
def index():
    global search_limit
    if request.method == 'POST':
        search_term = request.form['search_term']
        search_engine = request.form['search_engine']
        format_option = request.form['format_option']
        tor_toggle = request.form.get('tor_toggle')
        search_limit = int(request.form['search_limit'])

        # Spider selection
        spider_name = ''
        if search_engine == 'bing':
            spider_name = 'bing_spider'
        elif search_engine == 'duckduckgo':
            spider_name = 'keyword_spider'
        elif search_engine == 'onion' and tor_toggle:
            spider_name = 'onion_spider'

        # Define file name
        file_name = f'{search_term.replace(" ", "_")}_results.{format_option}'

        # Start progress simulation in a separate thread
        Thread(target=simulate_progress, args=(search_limit,)).start()

        subprocess.Popen(['scrapy', 'crawl', spider_name, '-a', f'keyword={search_term}', '-o', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return redirect(url_for('result', term=search_term, format=format_option, engine=search_engine, file=file_name))

    return render_template('index.html')

@app.route('/progress')
def progress_status():
    return jsonify({'progress': progress})

@app.route('/result/<term>/<format>/<engine>/<file>')
def result(term, format, engine, file):
    
    try:
        with open(file, 'r') as f:
            data = f.read()
        return render_template('result.html', data=data)
    except Exception as e:
        return f"Error loading results: {str(e)}", 500
    

@app.route('/download/<file>')
def download_file(file):
    return send_file(file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
