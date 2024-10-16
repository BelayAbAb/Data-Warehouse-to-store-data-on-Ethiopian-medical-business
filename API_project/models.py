from pydantic import BaseModel

class DetectionResultCreate(BaseModel):
    bounding_box: str
    confidence_score: float

class DetectionResult(DetectionResultCreate):
    id: int
    model_id: int

    class Config:
        orm_mode = True
