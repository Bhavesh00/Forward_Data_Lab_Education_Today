from getpass import getpass
from mysql.connector import connect, Error


def update_Professors_DB(extracted_professors):
    try:
        with connect(
            host="104.198.163.126",
            user= input("Enter username: "),
            password = "yEBpALG6zHDoCFLn",
            database = 'project'
        ) as connection:
            # sql = "INSERT INTO Professor (name, bio, award, education, institution) VALUES (%s, %s, %s, %s, %s)"
            print(connection)
            mycursor = connection.cursor()
            mycursor.executemany(sql, extracted_professors)
            connection.commit()

            print(mycursor.rowcount, "was inserted.")

            connection.close()
    except Error as e:
        print(e)