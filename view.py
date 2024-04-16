import sqlite3 as lite

con = lite.connect("estoquefinal.db")

def insert_info(i):
    with con:
        cursor = con.cursor()
        query = "INSERT INTO estoque(nome, num_serie, cliente, projeto, quantidade, defeitos, nota, data, imagem) VALUES (?,?,?,?,?,?,?,?,?)"
        cursor.execute(query, i)

def read_info():
    list = []
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM estoque")
        info = cursor.fetchall()
        print(info)

        for i in info:
            list.append(i)
    return list

def update_info(i):
    with con:
        cursor = con.cursor()
        query = "UPDATE estoque SET nome=?, num_serie=?, cliente=?, projeto=?, quantidade=?, defeitos=?, nota=?, data=?, imagem=? WHERE id=?"
        cursor.execute(query, i)

def delete_info(i):
    with con:
        cursor = con.cursor()
        query = "DELETE FROM estoque WHERE id=?"
        cursor.execute(query, i)
