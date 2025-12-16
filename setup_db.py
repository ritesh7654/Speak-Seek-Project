import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    database=os.environ.get('MYSQL_DATABASE')
)
cursor = conn.cursor()

# Create the missing table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_voice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),
    severity VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    is_anonymous BOOLEAN,
    status VARCHAR(50) DEFAULT 'Pending',
    date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

print("✅ SUCCESS: 'student_voice' table created successfully!")
conn.commit()
conn.close()