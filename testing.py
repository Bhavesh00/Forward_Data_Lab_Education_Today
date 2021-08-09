import mysql.connector

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


def similarity_score(npmi_cursor, word_1, word_2):
    if word_1 == word_2:
        return 1
    npmi_cursor.execute("SELECT id FROM fos WHERE FoS_name = '%s'" % word_1)
    token1 = npmi_cursor.fetchone()
    if token1 is None:
        return 0
    else:
        token1 = token1[0]
    npmi_cursor.execute("SELECT id FROM fos WHERE FoS_name = '%s'" % word_2)
    token2 = npmi_cursor.fetchone()
    if token2 is None:
        return 0
    else:
        token2 = token2[0]
    npmi_cursor.execute("SELECT npmi FROM fos_npmi_springer WHERE id1 = %d AND id2 = %d" % (token1, token2))
    ret = npmi_cursor.fetchone()
    if ret is None:
        npmi_cursor.execute("SELECT npmi FROM fos_npmi_springer WHERE id1 = %d AND id2 = %d" % (token2, token1))
        ret_alt = npmi_cursor.fetchone()
        if ret_alt is None:
            return 0
        return ret_alt[0]
    return ret[0]


print(similarity_score(npmi_cursor, "feature selection", "neural network"))