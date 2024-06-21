import cx_Oracle
local_host = 'localhost'
port_no = '1521'
service_name='XE'
user_name = 'awad'
pwd = 'root'

dsn_tns = cx_Oracle.makedsn(local_host, port_no, service_name=service_name) 

conn = cx_Oracle.connect(user=user_name, password=pwd, dsn=dsn_tns)
creds = {'usernames':[], 'passwords':[], 'id':[]}
query = ('select * from credentials')
cur = conn.cursor()
cur.execute(query)
cur.execute('select * from credentials')
results = []
for row in cur.fetchall():
    results.append(row)
print(results)