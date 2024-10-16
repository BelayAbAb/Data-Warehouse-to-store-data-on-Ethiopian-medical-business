import os

# Define the project structure
project_structure = {
    "your_project": {
        "main.py": '''from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import get_db
from crud import get_items
from models import Item
from sqlalchemy.orm import Session

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=templates.TemplateResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/", response_class=templates.TemplateResponse)
async def read_items(request: Request, db: Session = Depends(get_db)):
    items = get_items(db)
    return templates.TemplateResponse("result.html", {"request": request, "items": items})
''',
        "database.py": '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Adjust as needed for your database

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''',
        "models.py": '''from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
''',
        "crud.py": '''from sqlalchemy.orm import Session
from models import Item

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()
''',
        "static": {
            "favicon.ico": ''  # You can add an actual favicon file here
        },
        "templates": {
            "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico">
    <title>FastAPI Project</title>
</head>
<body>
    <h1>Welcome to FastAPI!</h1>
    <form action="/items/" method="get">
        <button type="submit">Get Items</button>
    </form>
</body>
</html>
''',
            "result.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico">
    <title>Results</title>
</head>
<body>
    <h1>Items</h1>
    <ul>
        {% for item in items %}
            <li>{{ item.name }}: {{ item.description }}</li>
        {% endfor %}
    </ul>
    <a href="/">Go back</a>
</body>
</html>
'''
        },
        "requirements.txt": '''fastapi
uvicorn
sqlalchemy
jinja2
'''
    }
}

# Function to create the directory and files
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as file:
                file.write(content)

# Create the project structure
create_project_structure(os.getcwd(), project_structure)
print("Project structure created successfully!")
