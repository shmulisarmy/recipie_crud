from utils.database import connect_to_db


table_name = "recipies"


def get_recipies():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    recipies = cursor.fetchall()
    connection.close()
    return recipies


print(f"{get_recipies()}")