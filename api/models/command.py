from enum import Enum as PyEnum
from sqlalchemy import Column, String, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from .base import Base

class CommandStatus(PyEnum):
  PENDING = "pending"
  COMPLETED = "completed"

class Command(Base):
  __tablename__ = "commands"

  id = Column(Integer, primary_key=True, autoincrement=True)
  machine_id = Column(String, ForeignKey('machines.id'))
  script_name = Column(String, ForeignKey('scripts.name'))
  status = Column(Enum(CommandStatus), nullable=False, default=CommandStatus.PENDING)
  output = Column(String)

  script = relationship("Script", back_populates="commands")