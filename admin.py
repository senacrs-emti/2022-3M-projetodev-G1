# biblioteca mysql
import pymysql
# conexao com o banco
con = pymysql.connect(host='localhost',user='root',password='',database='faceid',cursorclass=pymysql.cursors.DictCursor)

 # Criar a consulta e executá-la no banco
 with con.cursor() as c:
    # Criar a consulta e executá-la no banco
    sql = "SELECT * FROM pessoas WHERE PessoaID = 1"
    
         


# Desconectar do servidor
con.close()