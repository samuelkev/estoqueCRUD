import sqlite3 as lite

con = lite.connect("estoquefinal.db")

with con:
    cursor = con.cursor()
    cursor.execute("CREATE TABLE estoque(id INTEGER PRIMARY KEY, nome TEXT, num_serie INTEGER, cliente TEXT, projeto TEXT, quantidade INTEGER, defeitos INTEGER,nota TEXT, data DATE, imagem TEXT)")