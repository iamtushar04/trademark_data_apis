from sqlalchemy import Column, String, Integer, DateTime, BLOB, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Professionals(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(Text)
    name = Column(Text)
    designation = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    city = Column(Text)
    weblink = Column(Text)
    services = Column(Text)
    industry = Column(Text)
    keyword = Column(Text)
    description = Column(Text)
    inserted_at = Column(DateTime, default=datetime.utcnow)  # Set on insert
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint('name', 'email', 'keyword'),
    )

    # def __init__(self, id, items, work_group, main_dir, parent_, file_name, file_path, file_content, published_at,
    #              inserted_at, pdf_file):
    #     self.id = id
    #     self.items = items
    #     self.work_group = work_group
    #     self.main_dir = main_dir
    #     self.parent_ = parent_
    #     self.file_name = file_name
    #     self.file_path = file_path
    #     self.file_content = file_content
    #     self.published_at = published_at
    #     self.inserted_at = inserted_at
    #     self.pdf_file = pdf_file
    #
    # def __repr__(self):
    #     return f"({self.id}  {self.file_name}  {self.published_at}  {self.inserted_at})"


from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfessionalCreate(BaseModel):
    company: Optional[str]
    name: str
    designation: Optional[str]
    email: EmailStr
    phone: Optional[str]
    city: Optional[str]
    weblink: Optional[str]
    services: Optional[str]
    industry: Optional[str]
    keyword: Optional[str]
    description: Optional[str]