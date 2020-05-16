# project-011

=======
Финальный проект на Django, разработанный с помощью python 3.7.

#### Setup
Используйте `pip install -U -r requirements.txt` (в виртуальной среде python /virtualenv) для установки зависимостей.

#### Development
1. Выполнить `python manage.py makemigrations` для создания миграции
1. Выполнить `python manage.py migrate` для инициализации БД
2. Выполнить `python manage.py createsuperuser` для создания суперюзера
3. Выполнить `python manage.py runserver` для запуска проекта на локальной машине

#### Production
Настроить параметры в `settings.py` для использования в продакшене.
* `ALLOWED_HOSTS`
* `DEBUG` (выставить `False`)
* `SECRET_KEY` (должен быть случайным)
* `SITE_URL` (абсолютный URL)
* `DATABASES`

Здесь дополнительные параметры [Django Docs](https://docs.djangoproject.com/en/2.2/ref/settings/) или по комментариям в `settings.py`.

#### Tests
Используется pytest, для запуска тестов выполнить `python manage.py test` или `py.test --cov=apps`.
Для генерации отчета в HTML использовать команду `py.test --cov-report html` .

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

## Links for localhost
[Admin page](http://localhost:8000/admin)
[Swagger](http://localhost:8000/swagger)
[Redoc](http://localhost:8000/redoc)

## API:
### Reservation:
| Method        | URL           | Description  | Required Data Parameters |
| ------------- | ------------- | ------------ | ------ |
| **GET** | `/reservation/list/` |  Список всех бронирований | - |
| **GET** | `/reservation/list/{id}` |  Список всех бронирований переговорной {id} | id |
| **GET** | `/reservation/list/today/` |  Список всех бронирований на день вперед | - |
| **GET** | `/reservation/list/today/{id}` |  Список бронирований переговорной {id} на день вперед | id |
| **GET** | `/reservation/list/?start_date_range={date}&end_date_range={date}` |  Список бронирований по временному интервалу | start_date_range, end_date_range |
| **POST** | `/reservation/add/` |  Добавить новое бронирование | data: {created_by, room, subject, start_meeting_time, end_meeting_time} |
| **GET** | `/reservation/{id}` |  Получить информацию о бронировании {id} | id |
| **PUT** | `/reservation/{id}` |  Изменить информацию о бронировании {id} | id, data: {created_by, room, subject, start_meeting_time, end_meeting_time} |
| **PATCH** | `/reservation/{id}` |  Частично изменить информацию о бронировании {id} | id, data: {created_by, room, subject, start_meeting_time, end_meeting_time} |
| **DELETE** | `/reservation/{id}` |  Удалить бронирование {id} | id |
| **GET** | `/reservation/{id}/approve/` |  Подтвердить бронирование {id} | id |
| **GET** | `/reservation/{id}/reject/` |  Отменить бронирование {id} | id |

### Office:
| Method        | URL           | Description  | Required Data Parameters |
| ------------- | ------------- | ------------ | ------ |
| **GET** | `/office/list/` |  Список всех офисов | - |
| **GET** | `/office/{id}/` |  Информация по конкретному офису {id} | id |
| **GET** | `/office/{id}/rooms/` |  Список всех переговорных в офисе | - |
| **GET** | `/office/{id}/users/` |  Список всех сотрудников в офисе {id} | id |

### Room:
| Method        | URL           | Description  | Required Data Parameters |
| ------------- | ------------- | ------------ | ------ |
| **GET** | `/room/list/` |  Список всех переговорных | - |
| **GET** | `/room/{id}/` |  Информация по конкретной переговорной {id} | id |
| **GET** | `/room/{id}/equipment/` |  Список всего оборудования в переговорной {id} | id |

### Equipment:
| Method        | URL           | Description  | Required Data Parameters |
| ------------- | ------------- | ------------ | ------ |
| **GET** | `/equipment/list/` |  Список всего оборудования | - |
| **GET** | `/equipment/{id}/` |  Информация по конкретной единице оборудования {id} | id |

### User:
| Method        | URL           | Description  | Required Data Parameters |
| ------------- | ------------- | ------------ | ------ |
| **GET** | `/user/list/` |  Список всех сотрудников | - |
| **GET** | `/user/{id}/` |  Информация по конкретному сотруднику {id} | id |
