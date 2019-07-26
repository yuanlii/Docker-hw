import pyodbc
# conn_str = (
#     "DRIVER={PostgreSQL Unicode};"
#     "DATABASE=postgres;"
#     "UID=postgres;"
#     "PWD=whatever;"
#     "SERVER=localhost;"
#     "PORT=5432;"
#     )
# conn = pyodbc.connect(conn_str)

conn = pyodbc.connect(dsn="my_driver")
crsr = conn.execute("SELECT 123 AS n")
row = crsr.fetchone()
print(row)
crsr.close()
conn.close()

