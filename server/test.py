import MysqlHandler
def checkUser(account):
    mysql=MysqlHandler.sql()
    select="SELECT account,password,nickname FROM user WHERE account='%s'"%account
    info=mysql.select(select)
    mysql.con_close()
    return info

def checkNick(nickname):
    mysql=MysqlHandler.sql()
    select="SELECT account,password,nickname FROM user WHERE nickname='%s'"%nickname
    info=mysql.select(select)
    mysql.con_close()
    return info

def insertUser(account,password,nickname):
    mysql=MysqlHandler.sql()
    insert="INSERT INTO user(account,password,nickname) VALUES('%s','%s','%s')"%(account,password,nickname)
    mysql.insert(insert)
    mysql.con_close()

