from django.core.management.base import BaseCommand
from postolit.clickhouse import create_connection
from web.clickhouse_models import Distsipliny1, Vedomost3

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Подключаемся к бд
        db = create_connection()
        # Создание таблиц
          #db.create_table(Distsipliny1)
        db.create_table(Vedomost3)

        print("Tables create!")