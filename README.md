# Тестовое задание для программистов (основная деятельность)  

# Запускае команду для установки виртуального окружения
pip install -r requirements.txt
# Входим в директорию urban_project
cd cafe_order_system
# Производим миграции
python cafe_order_system/manage.py makemigrations
python cafe_order_system/manage.py migrate
# Запускаем DjangoProject
python cafe_order_system/manage.py runserver
python manage.py createsuperuser

# Так выглядит начальная страница проекта

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/1.png)

# Заходим во вкладку "регистрация", регистрируемся.

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/2.png)

# Так выглядит список заявок на доставку.

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/3.png)

# Входим в заявку.

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/4.png)

# Редактируем заявку.

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/5.png)

# Управляем заявками пользователей как админ сайта.

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/6.png)
