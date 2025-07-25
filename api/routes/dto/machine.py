from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MachineRequestDTO(BaseModel):
  id: str
  name: str

class MachineResponseDTO(BaseModel):
  id: str
  name: str
  last_seen: int