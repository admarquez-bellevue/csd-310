import mysql.connector
from mysql.connector import errorcode

# Configuration for MySQL connection
config = {
    "user": "root",
    "password": "Poppy^2020!",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}

try:
    # Connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    # Select all fields from the Studio table
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM Studio")
    studios = cursor.fetchall()
    for studio in studios:
        print(f"Studio ID: {studio[0]}")
        print(f"Studio Name: {studio[1]}\n")

    # Select all fields from the Genre table
    print("-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM Genre")
    genres = cursor.fetchall()
    for genre in genres:
        print(f"Genre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}\n")

    # Select movie names for movies with runtime less than two hours
    print("-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT Film_Name, Film_Runtime FROM Film WHERE Film_Runtime < 120")
    short_films = cursor.fetchall()
    for film in short_films:
        print(f"Film Name: {film[0]}")
        print(f"Runtime: {film[1]}\n")

    # List film names and directors grouped by director
    print("-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT Film_Name, Film_Director FROM Film ORDER BY Film_Director")
    directors = cursor.fetchall()
    for director in directors:
        print(f"Film Name: {director[0]}")
        print(f"Director: {director[1]}\n")

except mysql.connector.Error as err:
    # Handle errors
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")
    else:
        print(err)

finally:
    # Close the database connection
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\n Database connection closed.")