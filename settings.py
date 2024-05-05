from kombu import Queue, Exchange

imports = 'celery'
task_track_started = True
task_default_delivery_mode = 'transient'
broker_connection_retry_on_startup = True


task_queues = (
    Queue('analyze_code', Exchange('analyze_code'), routing_key='analyze_code'),
    Queue('translate_code', Exchange('translate_code'), routing_key='translate_code'),

)

task_routes = {
    'app.analyze': {
        'queue': 'analyze_code',
        'routing_key': 'analyze_code'
    },
    'app.translate': {
        'queue': 'translate_code',
        'routing_key': 'translate_code'
    },
}
