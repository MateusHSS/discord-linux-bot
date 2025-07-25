from pydantic import BaseModel

class ScriptRequestDTO(BaseModel):
  name: str
  content: str

class ScriptResponseDTO(BaseModel):
  name: str
  content: str