import psycopg2
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

try:
    # Establish the database connection
    with psycopg2.connect(
        dbname="FastAPI_week7",  # Database name
        user="postgres",          # Username
        password="belay",         # Password
        host="127.0.0.1",        # Host
        port="5432"               # Port
    ) as conn:
        
        with conn.cursor() as cursor:
            # Create the models table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id SERIAL PRIMARY KEY,
                model_name VARCHAR(255),
                model_path VARCHAR(255),
                version VARCHAR(50)
            );
            ''')
            
            # Create a table for detection results
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_results (
                id SERIAL PRIMARY KEY,
                model_id INT REFERENCES models(id),
                bounding_box VARCHAR(50),
                confidence_score FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''')

            # Insert model metadata (you can skip this if it's already present)
            model_name = 'YOLOv8'
            model_path = os.path.join(
                'C:', 'Users', 'User', 'Desktop', 
                '10Acadamy', 'Week 7', 
                'Data Warehouse to store data on Ethiopian medical business', 
                'yolov8n.pt'
            )
            version = 'v1.0'

            cursor.execute(
                "INSERT INTO models (model_name, model_path, version) VALUES (%s, %s, %s) RETURNING id",
                (model_name, model_path, version)
            )
            model_id = cursor.fetchone()[0]
            conn.commit()
            logging.info("Model metadata inserted successfully.")

            # Simulated detection results (replace with actual detection logic)
            detection_results = [
                {'bounding_box': '(100, 150, 200, 250)', 'confidence_score': 0.85},
                {'bounding_box': '(120, 160, 210, 260)', 'confidence_score': 0.90},
            ]

            # Insert detection results into the database
            for result in detection_results:
                cursor.execute(
                    "INSERT INTO detection_results (model_id, bounding_box, confidence_score) VALUES (%s, %s, %s)",
                    (model_id, result['bounding_box'], result['confidence_score'])
                )

            conn.commit()
            logging.info("Detection results inserted successfully.")

except Exception as e:
    logging.error(f"Error: {e}")
