from database import get_db
from models import DetectionResultCreate

def create_detection_result(db, result: DetectionResultCreate):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO detection_results (model_id, bounding_box, confidence_score) VALUES (%s, %s, %s) RETURNING id",
        (1, result.bounding_box, result.confidence_score)
    )
    db.commit()
    result_id = cursor.fetchone()[0]
    cursor.close()
    return {"id": result_id, "model_id": 1, **result.dict()}

def read_detection_results(db, model_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM detection_results WHERE model_id = %s", (model_id,))
    results = cursor.fetchall()
    cursor.close()
    return [{"id": r[0], "model_id": r[1], "bounding_box": r[2], "confidence_score": r[3]} for r in results]

def update_detection_result(db, result_id: int, result: DetectionResultCreate):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE detection_results SET bounding_box = %s, confidence_score = %s WHERE id = %s",
        (result.bounding_box, result.confidence_score, result_id)
    )
    db.commit()
    cursor.close()
    return {"id": result_id, "model_id": 1, **result.dict()}

def delete_detection_result(db, result_id: int):
    cursor = db.cursor()
    cursor.execute("DELETE FROM detection_results WHERE id = %s", (result_id,))
    db.commit()
    cursor.close()
