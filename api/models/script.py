from sqlalchemy import Column, String
from .base import Base

class Script(Base):
  __tablename__ = "scripts"

  name = Column(String, primary_key=True)
  content = Column(String)