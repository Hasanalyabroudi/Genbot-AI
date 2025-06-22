from dbs.sql_db.db import db as sql_db
from database_logger.dblogg import dblogg

sql_db_ = sql_db(
        SERVER_IP='localhost',
        DATABASE_NAME='genbot_logs',
        username='postgres',
        password='postgres',
     
    )
sql_db_.connect()


dblogg_ = dblogg(sql_db_)
id = dblogg_.setup_new_db('test.com')
dblogg_.update_number_of_pages(id,10)