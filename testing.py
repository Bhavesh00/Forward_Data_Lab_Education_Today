import mysql.connector

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="262956",
#     database="forward",
# )

fos_data = mysql.connector.connect(
        host="104.198.163.126",
        user="root",
        password="yEBpALG6zHDoCFLn",
        database="project"
    )
fos_cursor = fos_data.cursor()

fos_cursor.execute("SELECT name FROM Professor")
list_of_professors = list(fos_cursor.fetchall())
for name in list_of_professors:
    fos_cursor.execute("SELECT keyword, occurrence FROM Keywords WHERE name = '%s'" % name[0])
    rows = list(fos_cursor.fetchall())
    dict_of_focus_to_weight = {}
    for r in rows:
        print(r)
        dict_of_focus_to_weight[r[0]] = r[1]
    print(dict_of_focus_to_weight)