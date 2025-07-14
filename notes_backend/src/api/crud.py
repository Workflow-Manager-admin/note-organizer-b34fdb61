# crud.py — CRUD operations for notes

from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from . import models

# PUBLIC_INTERFACE
def get_note(db: Session, note_id: int):
    """Fetch a specific note by id."""
    return db.query(models.Note).filter(models.Note.id == note_id).first()

# PUBLIC_INTERFACE
def get_notes(db: Session, skip: int = 0, limit: int = 100):
    """Return a list of all notes, paginated."""
    return db.query(models.Note).order_by(models.Note.updated_at.desc()).offset(skip).limit(limit).all()

# PUBLIC_INTERFACE
def create_note(db: Session, note: models.NoteCreate):
    """Create (insert) a new note."""
    db_note = models.Note(
        title=note.title,
        content=note.content,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# PUBLIC_INTERFACE
def update_note(db: Session, note_id: int, note_update: models.NoteUpdate):
    """Update a note by id."""
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        return None
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.content is not None:
        db_note.content = note_update.content
    db_note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_note)
    return db_note

# PUBLIC_INTERFACE
def delete_note(db: Session, note_id: int):
    """Delete a note by id."""
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        return False
    db.delete(db_note)
    db.commit()
    return True

# PUBLIC_INTERFACE
def search_notes(db: Session, query: str, skip: int = 0, limit: int = 100):
    """
    Search notes where title or content contains query string (case-insensitive).
    """
    q = f"%{query}%"
    return db.query(models.Note).filter(
        or_(
            models.Note.title.ilike(q),
            models.Note.content.ilike(q)
        )
    ).order_by(models.Note.updated_at.desc()).offset(skip).limit(limit).all()
