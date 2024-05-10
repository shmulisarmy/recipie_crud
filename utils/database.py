import psycopg2


def connect_to_db():
    """This function establishes a connection to the postgres database"""
    try:
        connection = psycopg2.connect(
            database="master", user="postgres", password="postgres"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to Postgres", error)



