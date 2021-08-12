import mysql.connector
import operator

npmi_data = mysql.connector.connect(
    host="localhost",
    user="root",
    password="262956",
    database="forward",
)
npmi_cursor = npmi_data.cursor()

# fos_data = mysql.connector.connect(
#         host="104.198.163.126",
#         user="root",
#         password="yEBpALG6zHDoCFLn",
#         database="project"
#     )
# fos_cursor = fos_data.cursor()

def print_list(some_list):
    ret = "("
    for i in some_list:
        ret += "'"
        ret += i
        ret += "',"
    ret = ret[:-1]
    ret += ")"
    return ret

ins = print_list(["classification", "security"])
print(ins)
npmi_cursor.execute("SELECT * FROM fos WHERE FoS_name in " + ins)
print(npmi_cursor.fetchall())