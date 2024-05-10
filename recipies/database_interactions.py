from utils.database import connect_to_db


#! any values inside {} must come from server 
table_name = "recipies"


def get_recipies() -> list[tuple[str, str, str, int, int]]:
    """gets name, ingredients, instructions andtime_to_make, id"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT name, ingrediants, instructions, total_time_to_make, id FROM {table_name}")
    recipies = cursor.fetchall()
    connection.close()
    return recipies


print(f"{get_recipies()}")




def get_recipies_by_time_to_make(min_time: int, max_time: int, desc: bool = False) -> list[tuple[str, str, str, int, int]]:
    """gets name, ingredients, instructions andtime_to_make FROM where time_to_make is"""
    connection = connect_to_db()
    cursor = connection.cursor()
    order_by_str = f"order by total_time_to_make {'desc' if desc else 'asc'}"
    cursor.execute(f"select name, ingrediants, instructions, total_time_to_make, id from recipies where total_time_to_make between %s and %s {order_by_str};", (min_time, max_time, )) 
    recipies = cursor.fetchall()
    connection.close()
    return recipies






def create_recipie(name: str, ingrediants: dict, instructions: str, total_time_to_make: int, cost_to_make: int, posted_by: int = 1):
    """creates new recipie"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table_name} (posted_by, ingrediants, name, instructions, total_time_to_make, cost_to_make) VALUES (%s, %s, %s, %s, %s, %s)", (posted_by, str(ingrediants), name, instructions, total_time_to_make, cost_to_make))
    connection.commit()



def like_recipie(user_id: int, recipie_id: int):
    """likes recipie"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO liked_posts (user_id, post_id) VALUES (%s, %s)", (user_id, recipie_id))
    connection.commit()


def get_liked_recipies(user_id):
    """gets liked recipies"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT name, ingrediants, instructions, total_time_to_make, id FROM {table_name} inner join liked_posts on {table_name}.id = liked_posts.post_id where liked_posts.user_id = %s", (user_id, ))
    liked_recipies = cursor.fetchall()
    connection.close()
    return liked_recipies