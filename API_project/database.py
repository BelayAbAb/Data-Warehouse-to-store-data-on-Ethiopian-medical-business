import psycopg2
from psycopg2.extras import RealDictCursor
from models import DetectionResultCreate


# Function to get a database connection
def get_db():
    conn = psycopg2.connect(
        dbname="FastAPI_week7",
        user="postgres",
        password="belay",
        host="127.0.0.1",
        port="5432"
    )
    return conn

# Function to create a detection result
def create_detection_result(db, result: DetectionResultCreate):
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO detection_results (model_id, bounding_box, confidence_score) VALUES (%s, %s, %s) RETURNING id",
            (1, result.bounding_box, result.confidence_score)
        )
        db.commit()
        result_id = cursor.fetchone()[0]
    return {"id": result_id, "model_id": 1, **result.dict()}

# Function to read detection results
def read_detection_results(db, model_id):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM detection_results WHERE model_id = %s", (model_id,))
        results = cursor.fetchall()
    return results

# Function to update a detection result
def update_detection_result(db, result_id: int, result: DetectionResultCreate):
    with db.cursor() as cursor:
        cursor.execute(
            "UPDATE detection_results SET bounding_box = %s, confidence_score = %s WHERE id = %s",
            (result.bounding_box, result.confidence_score, result_id)
        )
        db.commit()
    return {"id": result_id, "model_id": 1, **result.dict()}

# Function to delete a detection result
def delete_detection_result(db, result_id: int):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM detection_results WHERE id = %s", (result_id,))
        db.commit()
