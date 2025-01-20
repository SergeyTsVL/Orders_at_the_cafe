# Тестовое задание для программистов (основная деятельность)  

# Запускае команду для установки виртуального окружения
pip install -r requirements.txt
# Входим в директорию urban_project
cd cafe_order_system
# Производим миграции
python cafe_order_system/manage.py makemigrations
python cafe_order_system/manage.py migrate orders zero
# Запускаем DjangoProject
python cafe_order_system/manage.py runserver
python manage.py createsuperuser

1. Бронируем столик.
2. Создаем заказ