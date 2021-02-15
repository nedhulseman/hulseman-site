import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="dustPed15",
  database="recipes"
)

mycursor = mydb.cursor()


query = 'SELECT * FROM recipe'
mycursor.execute(query)
table_rows = mycursor.fetchall()
df = pd.DataFrame(table_rows)
print(df)



import pandas as pd
import MySQLdb
import pandas.io.sql as psql

HOST = 'localhost'
USER = 'root'
PW='dustPed15'
DBNAME='recipe'
# setup the database connection.  There's no need to setup cursors with pandas psql.
db=MySQLdb.connect(host=HOST, user=USER, passwd=PW, db=DBNAME)

# create the query
query = "select * from recipe"

# execute the query and assign it to a pandas dataframe
df = psql.read_sql(query, con=db)
# close the database connection
db.close()


import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# Define the MySQL engine using MySQL Connector/Python
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:dustPed15@localhost:3306/recipes', echo=True)



