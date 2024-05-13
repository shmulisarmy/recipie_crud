"""
GLOBAL CONSTSANTS:
    M_T_N: (stands for main table name) = "recipies"
    #! any values inside (f_string){} must come from server 

"""


# from utils.database import connect_to_db
import psycopg2
M_T_N: str = "recipies"


def connect_to_db():
    """This function establishes a connection to the postgres database"""
    try:
        connection = psycopg2.connect(
            database="master", user="postgres", password="postgres"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to Postgres", error)







# def get_recipies() -> list[tuple[str, str, str, int, int]]:
#     """gets name, ingredients, instructions andtime_to_make, id"""
#     connection = connect_to_db()
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT name, ingrediants, instructions, total_time_to_make, id FROM {M_T_N} limit 100")
#     recipies = cursor.fetchall()
#     connection.close()
#     return recipies


def get_100_most_recent_recipies(user_id: int) -> list[tuple[str, str, str, int, int]]:
    """Gets 100 most recent name, ingrediants, instructions, and time_to_make, id, posted_by liked (CASE) """
    connection = connect_to_db()
    cursor = connection.cursor()
    # Assuming M_T_N is a placeholder for the table name
    Case = "CASE WHEN liked_posts.user_id IS NOT NULL THEN 1 ELSE 0 END"
    Join = f"LEFT JOIN liked_posts ON liked_posts.post_id = {M_T_N}.id AND liked_posts.user_id = %s"
    q = f"SELECT {M_T_N}.name, {M_T_N}.ingrediants, {M_T_N}.instructions, {M_T_N}.total_time_to_make, {M_T_N}.id, {M_T_N}.posted_by, {Case} FROM {M_T_N} {Join}"
    order_by_str = f"ORDER BY {M_T_N}.id DESC"  # Assuming you want to order by time_to_make
    cursor.execute(f"{q} {order_by_str} LIMIT 100", (str(user_id))) 
    recipies = cursor.fetchall()
    connection.close()
    return recipies


def get_recipie(id: int) -> list[tuple[str, str, str, int, int]]:
    """Gets name, ingrediants, instructions, and time_to_make, id, posted_by liked (CASE) by id """
    connection = connect_to_db()
    cursor = connection.cursor()
    # Assuming M_T_N is a placeholder for the table name
    Case = "CASE WHEN liked_posts.user_id IS NOT NULL THEN 1 ELSE 0 END"
    Join = f"LEFT JOIN liked_posts ON liked_posts.post_id = {M_T_N}.id AND liked_posts.user_id = %s"
    q = f"SELECT {M_T_N}.name, {M_T_N}.ingrediants, {M_T_N}.instructions, {M_T_N}.total_time_to_make, {M_T_N}.id, {M_T_N}.posted_by, {Case} FROM {M_T_N} {Join}"
    cursor.execute(f"{q} WHERE {M_T_N}.id = %s", (str(id), str(id))) 
    recipie = cursor.fetchone()
    connection.close()
    return recipie



# def get_recipies_by_time_to_make(min_time: int, max_time: int, desc: bool = False) -> list[tuple[str, str, str, int, int]]:
#     """gets name, ingredients, instructions andtime_to_make FROM where time_to_make is"""
#     connection = connect_to_db()
#     cursor = connection.cursor()
#     order_by_str = f"order by total_time_to_make {'desc' if desc else 'asc'}"
#     cursor.execute(f"select name, ingrediants, instructions, total_time_to_make, id from recipies where total_time_to_make between %s and %s {order_by_str};", (min_time, max_time, )) 
#     recipies = cursor.fetchall()
#     connection.close()
#     return recipies



# def get_recipies_new(user_id: int, min_time: int, max_time: int, desc: bool = False) -> list[tuple[str, str, str, int, int]]:
#     """gets name, ingredients, instructions andtime_to_make FROM where time_to_make is"""
#     connection = connect_to_db()
#     cursor = connection.cursor()
#     q = f"select {M_T_N}.name, {M_T_N}.ingredients, {M_T_N}.instructions, {M_T_N}.time_to_make, case when liked_posts.user_id is not null then 1 else 0 end from recipies left join liked_posts on liked_posts.post_id = recipies.id and liked_posts.user_id = ? where {M_T_N}.time_to_make between ? and ?"
#     order_by_str = f"order by total_time_to_make {'desc' if desc else 'asc'}"
#     cursor.execute(f"{q} {order_by_str}", (user_id, min_time, max_time)) 
#     recipies = cursor.fetchall()
#     connection.close()
#     return recipies

def get_recipies_by_time_to_make(user_id: int, min_time: int, max_time: int, desc: bool = False) -> list[tuple[str, str, str, int, int]]:
    """Gets name, ingrediants, instructions, and time_to_make, id, posted_by, liked (CASE) where time_to_make is between min_time and max_time."""
    connection = connect_to_db()
    cursor = connection.cursor()
    # Assuming M_T_N is a placeholder for the table name
    q = f"SELECT {M_T_N}.name, {M_T_N}.ingrediants, {M_T_N}.instructions, {M_T_N}.total_time_to_make, {M_T_N}.id, {M_T_N}.posted_by, CASE WHEN liked_posts.user_id IS NOT NULL THEN 1 ELSE 0 END FROM {M_T_N} LEFT JOIN liked_posts ON liked_posts.post_id = {M_T_N}.id AND liked_posts.user_id = %s"
    where_statment = f"where {M_T_N}.total_time_to_make between %s and %s"
    order_by_str = f"ORDER BY {M_T_N}.total_time_to_make {'DESC' if desc else 'ASC'}"  # Assuming you want to order by time_to_make
    cursor.execute(f"{q} {where_statment} {order_by_str}", (user_id, min_time, max_time)) 
    recipies = cursor.fetchall()
    connection.close()
    return recipies





# print(f"{get_recipies_new(1, 1, 1000, True)}")
# print(f"{get_recipies_new(1, 1, 1000, False)}")




def create_recipie(name: str, ingrediants: dict, instructions: str, total_time_to_make: int, cost_to_make: int, posted_by: int = 1):
    """creates new recipie"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {M_T_N} (posted_by, ingrediants, name, instructions, total_time_to_make, cost_to_make) VALUES (%s, %s, %s, %s, %s, %s)", (posted_by, str(ingrediants), name, instructions, total_time_to_make, cost_to_make))
    connection.commit()



def like_recipie(user_id: int, recipie_id: int):
    """likes recipie"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO liked_posts (user_id, post_id) VALUES (%s, %s)", (user_id, recipie_id))
    connection.commit()


def unlike_recipie(user_id: int, recipie_id: int):
    """likes recipie"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"delete from liked_posts where user_id = %s and post_id = %s", (user_id, recipie_id))
    connection.commit()


def get_liked_recipies(user_id):
    """gets liked recipies"""
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT name, ingrediants, instructions, total_time_to_make, id FROM {M_T_N} join liked_posts on {M_T_N}.id = liked_posts.post_id where liked_posts.user_id = %s", (user_id, ))
    liked_recipies = cursor.fetchall()
    connection.close()
    return liked_recipies


