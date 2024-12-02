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

def show_films(cursor, label):
    print(f"\n-- {label} --")
    query = """
        SELECT Film.Film_Name, Film.Film_Director, Genre.Genre_Name, Studio.Studio_Name
        FROM Film
        INNER JOIN Genre ON Film.Genre_ID = Genre.Genre_ID
        INNER JOIN Studio ON Film.Studio_ID = Studio.Studio_ID
    """
    cursor.execute(query)
    films = cursor.fetchall()
    for film in films:
        print(f"Film Name: {film[0]} \nDirector: {film[1]} \nGenre Name ID: {film[2]} \nStudio Name: {film[3]}\n") 

try:
    # Connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    show_films(cursor, "DISPLAYING FILMS")

    print("\nInserting new film record...")
    insert_film_query = """
        INSERT INTO Film (Film_Name, Film_Director, Genre_ID, Studio_ID, Film_ReleaseDate, Film_Runtime)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    new_film = ("Halloween Kills", "David Gordon Green", 1, 2, "2021", 105)
    cursor.execute(insert_film_query, new_film)
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    update_film_query = "UPDATE Film SET Genre_ID = %s WHERE Film_Name = %s"
    cursor.execute(update_film_query, (1, "Alien"))  # Horror genre ID = 1
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    delete_film_query = "DELETE FROM Film WHERE Film_Name = %s"
    cursor.execute(delete_film_query, ("Gladiator",))
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

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