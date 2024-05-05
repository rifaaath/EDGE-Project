from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import config
from analysis import analyze_code
from celery import Celery
from celery.result import AsyncResult
import json
from readability import Readability

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
CORS(app, origins="*", methods=['GET', 'POST', 'OPTIONS'])
broker_host = os.getenv('RABBITMQ_HOST', 'localhost')
app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'db+postgresql://app:app@localhost:5432/celery'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)
celery.config_from_object('settings')

@app.route('/api/analyze', methods=['POST'])
def handle_code():
    data = json.loads(request.get_json())
    code_content = data['fileContent']
    source_lang, dest_lang = data['source'], data['dest']
    # print(type(data))
    task = analyze_code(code_content, source_lang, dest_lang)
    # print(task,1)
    response = {
        'result':task
    }
    return response


if __name__ == '__main__':
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 0  # Persistent cache
    app.run(host='0.0.0.0',port=8000,debug=True)