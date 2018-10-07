from django.db import connection

def selectBlike(u_id):
    cursor = connection.cursor()
    query_string = "SELECT b_id FROM book_blike where u_id = \'" + str(u_id) + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    book=[]
    for row in rows :
        book.append(row[0])
    return book

def countBlike(u_id):
    cursor = connection.cursor()
    query_string = "SELECT count(*) FROM book_blike where u_id = \'" + str(u_id) + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        cnt = row[0]
    return cnt
