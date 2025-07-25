from sqlalchemy import Column, String
from .base import Base
from sqlalchemy.orm import relationship

class Script(Base):
  __tablename__ = "scripts"

  name = Column(String, primary_key=True)
  content = Column(String)

  commands = relationship("Command", back_populates="script")
