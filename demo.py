import psycopg2

#connect to the db
con = psycopg2.connect (
database = "exam1",
user = "postgres",
password = "11012202"
)

#cursor
cur = con.cursor()

#execute query
cur.execute("select id, name from employee")

rows = cur.fetchall()

for r in rows:
   print(f"id {r[0]} name {r[1]}")

# close cursor
cur.close()

#close the connection
con.close()