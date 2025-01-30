import sqlite3
import psycopg2

# Подключение к SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

# Подключение к PostgreSQL
postgres_conn = psycopg2.connect(
    dbname="django",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
postgres_cursor = postgres_conn.cursor()

# Извлечение данных из таблицы cars в SQLite
table_name = 'cars'
sqlite_cursor.execute(f"SELECT * FROM {table_name}")
rows = sqlite_cursor.fetchall()

# Проверка структуры данных
sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
columns_info = sqlite_cursor.fetchall()
columns = [col[1] for col in columns_info]  # Имена столбцов
print(f"Столбцы в SQLite: {columns}")  # Для отладки

# Изменение типа столбца power_volume в PostgreSQL
alter_table_query = """
ALTER TABLE cars
ALTER COLUMN power_volume TYPE TEXT;
"""
try:
    postgres_cursor.execute(alter_table_query)
    postgres_conn.commit()
except Exception as e:
    print(f"Ошибка при изменении типа столбца power_volume: {e}")

# Вставка данных в PostgreSQL
insert_query = """
INSERT INTO cars (model, year, mileage, price, transmission, engine_volume, drive, color, power_volume, brand_country_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Исключаем первый элемент (id) из каждой строки
rows_without_id = [row[1:] for row in rows]

# Вставка данных с обработкой ошибок
for row in rows_without_id:
    try:
        postgres_cursor.execute(insert_query, row)
        postgres_conn.commit()  # Фиксация каждой строки отдельно
    except Exception as e:
        print(f"Ошибка при вставке строки {row}: {e}")
        postgres_conn.rollback