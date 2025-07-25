from .base import Base
from sqlalchemy import Column, String, Integer, UUID
import uuid

class Machine(Base):
  __tablename__ = "machines"

  id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
  name = Column(String) 
  last_seen = Column(Integer)