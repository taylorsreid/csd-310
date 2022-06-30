'''
Taylor Reid
6/29/2022
Module 8.3
'''

#
import mysql.connector
from mysql.connector import errorcode

#
config = {
    "user": "pysports_user",
    "password": "seasprite",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}

#
db = mysql.connector.connect(**config)
cursor = db.cursor()

#
cursor.execute("SELECT team_id, team_name, mascot FROM team")
teams = cursor.fetchall()
print("-- DISPLAYING TEAM RECORDS --\n")
for team in teams:
    print(f"Team ID: {team[0]}")
    print(f"Team Name: {team[1]}")
    print(f"Mascot: {team[2]}")
    print()

#
cursor.execute("SELECT player_id, first_name, last_name, team_id FROM player")
players = cursor.fetchall()
print("-- DISPLAYING PLAYER RECORDS --\n")
for player in players:
    print(f"Player ID: {player[0]}")
    print(f"First Name: {player[1]}")
    print(f"Last Name: {player[2]}")
    print(f"Team ID: {player[3]}")
    print()

input("Press any key to continue...")