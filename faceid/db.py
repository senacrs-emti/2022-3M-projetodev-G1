# import das bibliotecas 
import pymysql, pymysql.cursors

# conexao com o banco
con = pymysql.connect(host='localhost',user='root',password='',database='faceid',cursorclass=pymysql.cursors.DictCursor)
# criar a consulta e executá-la no banco e executa o codigo
sql = "SELECT * FROM pessoas WHERE PessoaID = 1"

# percorre oa consulta de dados
with con.cursor() as cur:
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        ## escreve os dados da pessoa
        print(row['Nome'])

# Desconectar do servidor
con.close()