from getpass import getpass
from mysql.connector import connect, Error


def update_Professors_DB(extracted_professors):

    try:
        with connect(
            host="104.198.163.126",
            user= "root",
            password = "yEBpALG6zHDoCFLn",
            database = 'project'
        ) as connection:
            for professor in extracted_professors:    
                sql = "INSERT INTO Professor (name, bio, award, education, institution, research interest) VALUES (%s, %s, %s, %s, %s, %s)"
                mycursor = connection.cursor()
                data = (professor.name, professor.biography[:2048], professor.awards, professor.education, professor.institution, professor.research_interests)

                mycursor.execute(sql, data)
                connection.commit()

                print(mycursor.rowcount, "was inserted.")

                connection.close()
    except Error as e:
        print(e)