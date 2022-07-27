from celery import shared_task
from celery.schedules import crontab

from config.celery import app


@app.on_configure.connect
def setup_periodic_task(sender, **kwargs):
    """Планирует переодические задачи"""

    # Вызывает print_periodic('Hello from periodic task!') каждые 10 секунд
    sender.add_periodic_task(10.0, print_periodic.s('Hello from periodic task!'), name='add every 10')

    # Вызывает print_periodic('Hello from periodic task on Thursday 1:20a.m.') в определенное время
    sender.add_periodic_task(
        crontab(hour=1, minute=20, day_of_week=4),
        print_periodic.s('Hello from periodic task on Thursday at 1:20a.m.')
    )


@app.task
def print_periodic(args):
    print(args)
    return 'Periodic task done!'


@app.task
def print_hello():
    print('Hello from Celery')
    return 'It done!'


@shared_task
def add(x, y):
    return x + y


# тоже переодическая задача, но вручную
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'print_periodic.add',
        'schedule': 30.0,
        'args': 'Hello from handler periodic task!' # может принимать tuple с несколькими аргументами
    },
}

# ручной crontab
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=1, minute=21, day_of_week=4),
        'args': 'Hello from handler periodic task on Thursday at 1:21a.m.'
    },
}