# Проект 4 "Сервис управления рассылками"

---

## Оглавление

<a id="content"></a>

1. [Описание](#description)
2. [Установка и настройка проекта](#instruction)
3. [Структура проекта](#structure)
4. [Запуск и тестирование проекта](#launch)
5. [Лицензия](#license)

---

## Описание<a id="description"></a>

Проект 

---

## Установка и настройка проекта<a id="instruction"></a>

1. Клонируйте репозиторий:

```
git clone https://github.com/username/project-x.git
```

2. Перейдите в директорию проекта:

```
cd ваш_проект
```

3. Установите зависимости проекта:

```
poetry install
```

или

```
pip install -r requirements.txt
```

4. Зайдите в файл .env.example и следуйте инструкциям из него.

---

## Структура проекта<a id="structure"></a>

```
.
├──  - приложение на django
│ ├── migrations - папка с миграциями
│ ├── templates - папка с шаблонами страниц
│     ├── 
│         ├── .html, .html, .html, .html - шаблоны файлов
│     ├── admin.py, apps.py, models.py, tests.py, urls.py, views.py - необходимые модули для работы приложения
├──  - приложение на django
│ ├── management
│     ├── commands
│         ├──  - команда для автоматического добавления категорий и товаров в БД
│ ├── migrations - папка с миграциями
│ ├── templates - папка с шаблонами страниц
│     ├── catalog
│         ├── .html, .html, .html, .html - шаблоны файлов
│     ├── admin.py, apps.py, forms.py, models.py, tests.py, urls.py, views.py - необходимые модули для работы приложения
├── config
│     ├── asgi.py, settings.py, urls.py, wsgi.py необходимые модули для работы приложения
├── media
│ ├── photos - фото товаров, используются в бд при создании товара
├── static - папка со стилями и фото
│ ├── css
│     ├── bootstrap.min.css
│ ├── js
│     ├── bootstrap.bundle.min.js
├── users - приложение на django
│ ├── management
│     ├── commands
│         ├── createadmin - команда для автоматического создания суперпользователя
│ ├── migrations - папка с миграциями
│ ├── templates - папка с шаблонами страниц
│     ├── users
│         ├── login.html, register.html - шаблоны файлов
│     ├── admin.py, apps.py, forms.py, models.py, tests.py, urls.py, views.py - необходимые модули для работы приложения
├── .env.example - env экземпляр для доступа к закрытым данным
├── .flake8
├── .gitignore
├── _fixture.json - фикстура для заполнения БД
├── _fixture.json - фикстура для заполнения БД
├── manage.py
├── pyproject.toml
├── poetry.lock
├── requirements.text - файл с зависимостями
└── README.md
```

---

## Запуск и тестирование проекта<a id="launch"></a>

1. После установки и настройки проекта в консоль введите python/python3 manage.py runserver для запуска сервера
2. Откройте сервер (ссылка в консоли: http://127.0.0.1:8000)
3. Для просмотра страниц приложения **1** используйте http://127.0.0.1:8000/// или
http://127.0.0.1:8000///.
4. Для просмотра страниц приложения **2** используйте http://127.0.0.1:8000///.
4. Для входа в админ-панель используйте http://127.0.0.1:8000/admin/

---

## Лицензия<a id="license"></a>

Этот проект лицензирован по [лицензии MIT](LICENSE).

##### [Оглавление](#content)