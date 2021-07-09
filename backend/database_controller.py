from getpass import getpass
from mysql.connector import connect, Error


def update_Professors_DB(extracted_professors):
    try:
        with connect(
                host="104.198.163.126",
                user="root",
                password="yEBpALG6zHDoCFLn",
                database='project'
        ) as connection:
            for professor in extracted_professors:
                sql = "INSERT INTO Professor" \
                      " VALUES (" \
                      "%s, %s, %s, %s, %s, %s) "
                mycursor = connection.cursor()
                data = (professor.name, professor.biography[:2047], professor.awards[:2047], professor.education[:2047],
                        professor.institution, professor.research_interests[:2047])

                mycursor.execute(sql, data)
                connection.commit()

                print(mycursor.rowcount, "was inserted.")

                connection.close()
    except Error as e:
        print(e)
