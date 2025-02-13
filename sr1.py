start='2023-11-14'
end='2023-12-14'
start_date = start+' 00:00:00'
end_date = end+' 00:00:00'
print(start_date)
print(end_date)
conn = mysql.connect()
cursor = conn.cursor()

        # Assuming your Request table has a 'date' column
query = "SELECT * FROM requests WHERE timestamp_column BETWEEN %s AND %s"
cursor.execute(query, (start_date, end_date))
data = cursor.fetchall()
print(data)