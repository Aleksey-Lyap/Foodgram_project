### Сайт для публикации рецептов Foodgram

![foodgram_workflow](https://github.com/Aleksey-Lyap/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание

Сервис, в котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Также у пользователей есть возможность создавать список продуктов, которые нужно купить для приготовления выбранных блюд, и загружать его в текстовом формате.

В рамках учебного проекта был разработан backend сервиса и настроен CI/CD.

# Стек технологий
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Github Actions

# Доступ

Проект запущен на сервере и доступен по адресам:
- http://foodgramm.myvnc.com/recipes
- http://130.193.39.227/recipes
- Админ-зона: http://foodgramm.myvnc.com/admin/
- API: http://foodgramm.myvnc.com/api/

# Зависимости
- Перечислены в файле backend/requirements.txt

### Для запуска на собственном сервере:

# 1.Установка приложения docker на севере

# Установите docker на сервер:
```
sudo apt install docker.io 
```
# Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
# Примените разрешения для исполняемого файла к двоичному файлу:
```
sudo chmod 777 /usr/local/bin/docker-compose
```

### Развертывание приложения на сервере:

# Отредактируйте файл nginx.conf и в строке server_name впишите свой IP

1. Скопируйте из репозитория файлы, расположенные в директории infra:
    - docker-compose.yml
    - nginx.conf
2. Создайте файл .env и заполните следующим образом:
```
SECRET_KEY=<КЛЮЧ>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<ИМЯ БАЗЫ ДАННЫХ>
POSTGRES_USER=<ИМЯ ЮЗЕРА БД>
POSTGRES_PASSWORD=<ПАРОЛЬ БД>
DB_HOST=db
DB_PORT=5432
```
3. В директории c файлом docker-comose.yml следует выполнить команды:
```
sudo docker-compose up -d
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
4. Для создания суперпользователя, выполните команду:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
5. Для добавления ингредиентов в базу данных, выполните команду:
```
sudo docker-compose exec backend python manage.py filling_database
```
После выполнения этих действий проект будет запущен в четырех контейнерах (backend, frontend, db, nginx) и доступен по адресам:
- Главная страница: http://<ip-адрес>/recipes/
- API проекта: http://<ip-адрес>/api/
- Admin-зона: http://<ip-адрес>/admin/
6. Теги вручную добавляются в админ-зоне в модель Tags;
7. Проект запущен и готов к регистрации пользователей и добавлению рецептов.

### Автор
Ляпин Алексей - [https://github.com/Aleksey-Lyap]
