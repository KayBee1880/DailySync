import psycopg2
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5555,
        user="habit_tracker_user",
        password="T3@Mdatabase!",
        database="teamprojectdb"
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)