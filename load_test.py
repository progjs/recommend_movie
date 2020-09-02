import pymysql

def save_data():
    connection = pymysql.connect(host='localhost', user='young', password='1234', db='recommend_db', local_infile=True);

    try:
        with connection.cursor() as cursor:
            sql = "LOAD DATA LOCAL INFILE 'C:/mypython/data/movieapp_genre.csv' INTO TABLE movieapp_genre FIELDS TERMINATED BY ','"
            delete_truncate = "truncate table movieapp_genre;"
            cursor.execute(delete_truncate)
            cursor.execute("set foreign_key_checks = 0;")
            cursor.execute(sql)
            connection.commit()

    finally:
        connection.close()
