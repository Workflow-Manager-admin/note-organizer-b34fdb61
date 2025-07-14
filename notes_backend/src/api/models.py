# models.py — SQLAlchemy data and Pydantic schemas for notes

from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()

class Note(Base):
    """SQLAlchemy model for notes table."""
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False, index=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# -----------------------------
# Pydantic Schemas

# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Request model for creating a note."""
    title: str = Field(..., description="Title of the note")
    content: Optional[str] = Field("", description="Content of the note")

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Request model for updating a note."""
    title: Optional[str] = Field(None, description="Title of the note")
    content: Optional[str] = Field(None, description="Content of the note")

# PUBLIC_INTERFACE
class NoteInDB(BaseModel):
    """Represents a note in the database (as returned by API)."""
    id: int
    title: str
    content: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class NoteList(BaseModel):
    """Response model for a list of notes."""
    notes: List[NoteInDB]


# PUBLIC_INTERFACE
class NoteDeleteResponse(BaseModel):
    """Response for note deletion."""
    success: bool
    message: str
