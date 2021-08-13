import mysql.connector
import operator

npmi_data = mysql.connector.connect(
    host="localhost",
    user="root",
    password="262956",
    database="forward",
)
npmi_cursor = npmi_data.cursor()

fos_data = mysql.connector.connect(
        host="104.198.163.126",
        user="root",
        password="yEBpALG6zHDoCFLn",
        database="project"
    )
fos_cursor = fos_data.cursor()

