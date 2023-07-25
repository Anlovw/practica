# Замените значения ниже на свои данные для подключения к PostgreSQL
db_host = '127.0.0.1'
db_name = 'OSA'
db_user = 'postgre'
db_password = '3008'
table_name = 'worlds_best'

import psycopg2
import threading

def query_table_data(ret_val: list):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="postgres",
                                      password="3008",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="OSA")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        # print("PostgreSQL server information")
        #print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        # insert_query = "INSERT INTO {} (name, score) VALUES ('red_hot', 123);".format(table_name)
        # cursor.execute(insert_query)
        # "SELECT * FROM worlds_best;"
        cursor.execute("SELECT name, score FROM worlds_best;")
        # Fetch result
        all_data = cursor.fetchall()

        # Вывод полученных данных
        for row in all_data:
            ret_val.append(row)
            #print(row)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        pass
        #print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def update_or_insert_data(id_value, name_value, score_value):
    try:
        # Формирование строки подключения
        connection = psycopg2.connect(user="postgres",
                                      password="3008",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="OSA")

        # Создание курсора для выполнения SQL-запросов
        cursor = connection.cursor()

        # SQL-запрос на проверку наличия id в таблице
        check_query = f"SELECT tg_id FROM {table_name} WHERE tg_id = {id_value};"
        cursor.execute(check_query)

        # Проверяем, есть ли запись с данным id
        if cursor.fetchone():
            # Если запись существует, выполняем обновление значения score
            update_query = f"UPDATE {table_name} SET score = %s WHERE tg_id = %s;"
            cursor.execute(update_query, (score_value, id_value))
        else:
            # Если записи нет, выполняем вставку новой строки
            insert_query = f"INSERT INTO {table_name} (tg_id, name, score) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (id_value, name_value, score_value))

        # Подтверждение транзакции
        connection.commit()

        #print("Данные успешно обновлены или добавлены.")

    except (Exception, psycopg2.Error) as error:
        pass
        #print("Ошибка при работе с PostgreSQL:", error)

    finally:
        # Закрытие курсора и соединения с базой данных
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def start_query_thread(ret_list):
    # Запуск функции в отдельном потоке
    thread = threading.Thread(target=query_table_data, args=(ret_list,))
    thread.start()
def update_or_insert_data_thread(*args):
    # Запуск функции в отдельном потоке
    thread = threading.Thread(target=update_or_insert_data, args=args)
    thread.start()

# Вызов функции для запуска запроса в отдельном потоке
#start_query_thread()
#update_or_insert_data_thread(30083008, 'Bogdan', 113)