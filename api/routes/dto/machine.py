from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MachineRequestDTO(BaseModel):
  id: Optional[UUID] = None
  name: str

class MachineResponseDTO(BaseModel):
  id: UUID
  name: str
  last_seen: int