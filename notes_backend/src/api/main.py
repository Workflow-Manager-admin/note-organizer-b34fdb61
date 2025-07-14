from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, crud, database

# --- FastAPI app setup ---
app = FastAPI(
    title="Notes Backend API",
    description="A REST API for managing notes. Features: List, create, update, delete, and search notes.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Notes", "description": "CRUD operations for notes"},
        {"name": "Utility", "description": "Utility/health endpoints"},
    ]
)

import os

# --- Run with: `python src/api/main.py` or by uvicorn. Default port 3001. ---
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 3001))
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port, reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB Initialization on Startup ---
@app.on_event("startup")
def on_startup():
    """Ensure tables are created on app startup."""
    models.Base.metadata.create_all(bind=database.engine)

# --- Routes ---

@app.get("/", tags=["Utility"])
def health_check():
    """Health check route."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/notes", response_model=models.NoteList, tags=["Notes"], summary="List all notes")
def list_notes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Returns all notes, most recently updated first.
    Supports skip/limit pagination.
    """
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return {"notes": notes}

# PUBLIC_INTERFACE
@app.post("/notes", response_model=models.NoteInDB, status_code=status.HTTP_201_CREATED, tags=["Notes"], summary="Create a new note")
def create_note(note: models.NoteCreate, db: Session = Depends(database.get_db)):
    """
    Create a new note.
    """
    db_note = crud.create_note(db, note)
    return db_note

# PUBLIC_INTERFACE
@app.get("/notes/{note_id}", response_model=models.NoteInDB, tags=["Notes"], summary="Get a single note by ID")
def get_note(note_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve a single note by its ID.
    """
    db_note = crud.get_note(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# PUBLIC_INTERFACE
@app.put("/notes/{note_id}", response_model=models.NoteInDB, tags=["Notes"], summary="Update a note by ID")
def update_note(note_id: int, note_update: models.NoteUpdate, db: Session = Depends(database.get_db)):
    """
    Update a note's fields.
    """
    db_note = crud.update_note(db, note_id, note_update)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# PUBLIC_INTERFACE
@app.delete("/notes/{note_id}", response_model=models.NoteDeleteResponse, tags=["Notes"], summary="Delete a note by ID")
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a note by its ID.
    """
    deleted = crud.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"success": True, "message": "Note deleted"}

# PUBLIC_INTERFACE
@app.get("/notes/search", response_model=models.NoteList, tags=["Notes"], summary="Search for notes")
def search_notes(
    query: str = Query(..., description="Query string to search for in notes' title or content"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """
    Search notes where title or content contains the query string (case-insensitive).
    """
    notes = crud.search_notes(db, query=query, skip=skip, limit=limit)
    return {"notes": notes}
