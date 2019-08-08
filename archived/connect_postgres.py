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
crsr = conn.cursor()

# Open and read the file as a single buffer
script_path = '/Users/liyuan/Desktop/Docker-hw/create_banking_db.sql'
fd = open(script_path, 'r')
sql_script = fd.read()
fd.close()

# Get all SQL statements (split on ';')
sql_statements = sql_script.split(';')

# Execute SQL statements
for statement in sql_statements:
    if not statement.strip():
        continue
    crsr.execute(statement)
    print('Statement executed:'+ ' %s' % str(statement) + '\n')

conn.commit()
crsr.close()
conn.close()








