import pandas as pd
import psycopg2
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the scraped data from CSV
scraped_data_path = r'C:\Users\User\Desktop\10Acadamy\Week 7\Data Warehouse to store data on Ethiopian medical business\scraped_data.csv'
scraped_data = pd.read_csv(scraped_data_path)

# Check for required columns
required_columns = ['ID', 'Channel Title', 'Channel Username', 'Message', 'Date', 'Media Path']
missing_columns = [col for col in required_columns if col not in scraped_data.columns]

if missing_columns:
    raise ValueError(f"Missing columns in scraped_data.csv: {', '.join(missing_columns)}")

# Establish the database connection
conn = psycopg2.connect(
    dbname="FastAPI_week7",  # Database name
    user="postgres",          # Username
    password="belay",        # Password
    host="127.0.0.1",        # Host
    port="5432"               # Port
)

# Create a cursor object
cursor = conn.cursor()

# Drop the table if it exists
cursor.execute("DROP TABLE IF EXISTS business_data")
conn.commit()

# Create a new table for the collected data
cursor.execute("""
CREATE TABLE business_data (
    id SERIAL PRIMARY KEY,
    scraped_id INT,
    channel_title VARCHAR(255),
    channel_username VARCHAR(255),
    message TEXT,
    date TIMESTAMP,
    media_path TEXT
)
""")
conn.commit()

# Insert the scraped data into the database
for index, row in scraped_data.iterrows():
    try:
        cursor.execute("""
        INSERT INTO business_data (scraped_id, channel_title, channel_username, message, date, media_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['ID'], row['Channel Title'], row['Channel Username'], row['Message'], row['Date'], row['Media Path']))
        conn.commit()  # Commit after each successful insertion
    except Exception as e:
        logging.error(f"Error inserting row {index}: {e}")
        conn.rollback()  # Roll back the transaction on error

# Close the cursor and connection
cursor.close()
conn.close()

print("Data import process completed.")
