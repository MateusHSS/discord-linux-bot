from .base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import uuid

class Machine(Base):
  __tablename__ = "machines"

  id = Column(String, primary_key=True)
  name = Column(String)
  last_seen = Column(Integer)

  scripts = relationship("Command", back_populates="machine")