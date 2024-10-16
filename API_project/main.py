from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crud import create_detection_result, read_detection_results, update_detection_result, delete_detection_result
from models import DetectionResultCreate, DetectionResult
from database import get_

app = FastAPI()

# Mount static files for serving favicon
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detection_results/")
async def create_detection_result_api(request: Request):
    form = await request.form()
    bounding_box = form.get("bounding_box")
    confidence_score = float(form.get("confidence_score"))
    db = get_db()
    result = create_detection_result(db, DetectionResultCreate(bounding_box=bounding_box, confidence_score=confidence_score))
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

@app.get("/detection_results/{model_id}", response_class=HTMLResponse)
async def read_detection_results_api(request: Request, model_id: int):
    db = get_db()
    results = read_detection_results(db, model_id)
    return templates.TemplateResponse("result.html", {"request": request, "results": results})

@app.put("/detection_results/{result_id}")
async def update_detection_result_api(request: Request, result_id: int):
    form = await request.form()
    bounding_box = form.get("bounding_box")
    confidence_score = float(form.get("confidence_score"))
    db = get_db()
    updated_result = update_detection_result(db, result_id, DetectionResultCreate(bounding_box=bounding_box, confidence_score=confidence_score))
    return {"message": "Detection result updated successfully", "result": updated_result}

@app.delete("/detection_results/{result_id}")
async def delete_detection_result_api(result_id: int):
    db = get_db()
    delete_detection_result(db, result_id)
    return {"message": "Detection result deleted successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
