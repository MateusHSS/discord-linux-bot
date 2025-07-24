import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, String, UUID, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from .base import Base

class CommandStatus(PyEnum):
  PENDING = "pending"
  COMPLETED = "completed"

class Commands(Base):
  __tablename__ = "commands"

  id = Column(Integer, primary_key=True, autoincrement=True)
  machine_id = Column(String, ForeignKey('machines.id'))
  script_name = Column(String)
  status = Column(Enum(CommandStatus), nullable=False, default=CommandStatus.PENDING)
  output = Column(String)