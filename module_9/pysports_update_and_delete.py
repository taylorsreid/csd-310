'''
Taylor Reid
7/8/2022
Module 9.3
'''

#library imports
import mysql.connector
from mysql.connector import errorcode

#credentials configuration
config = {
    "user": "pysports_user",
    "password": "seasprite",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}
try:
    #credentials loaded in and connection created
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    #made it a function so we don't have to repeat code
    def outputDB():

        #selects the specified data and assigns it to the players variable
        cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id;")
        players = cursor.fetchall()  
        
        #for loop to output the results of the join query in a readable format
        for player in players:
            print(f"Player ID: {player[0]}")
            print(f"First Name: {player[1]}")
            print(f"Last Name: {player[2]}")
            print(f"Team Name: {player[3]}")
            print()
        
        #extra line for formatting
        print()

    #inserts Smeagol into the table
    cursor.execute("INSERT INTO player (first_name, last_name, team_id) VALUES('Smeagol', 'Shire Folk', 1);")
    print("-- DISPLAYING PLAYERS AFTER INSERT --")
    outputDB()

    #updates Smeagol Shire Folk to Gollum Ring Stealer and switches him to Team Sauron
    cursor.execute("UPDATE player SET team_id = 2, first_name = 'Gollum', last_name = 'Ring Stealer' WHERE first_name = 'Smeagol';")
    print("-- DISPLAYING PLAYERS AFTER UPDATE --")
    outputDB()

    #deletes Gollum completely
    cursor.execute("DELETE FROM player WHERE first_name = 'Gollum';")
    print("-- DISPLAYING PLAYERS AFTER DELETE --")
    outputDB()
    
    #closes connections, this was technically out of scope when under "finally:", don't know why it didn't throw an error
    db.close()
    
    #holds the command line open
    input("Press any key to continue...")

#in case there's a connection error
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")

    else:
        print(err)