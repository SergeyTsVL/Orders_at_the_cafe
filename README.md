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

![Uploading 1.png…](https://github.com/SergeyTsVL/TZ_vacancy/blob/main/images/1.png)