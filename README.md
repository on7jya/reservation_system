# project-011



#### Celery
Для успешной отработки фоновой задачи по автоматическому удалению неподтвержденного бронирования после начала встречи:
- в config.settings должен быть указан параметр AUTO_CANCEL_INTERVAL (в минутах)
- должны быть запущены следующие процессы:
```
# django
$ python manage.py runserver

# celery worker
$ celery -A config worker -l info

# celery beat
$ celery -A config beat -l info -S django

# redis server
$ redis-server
```
