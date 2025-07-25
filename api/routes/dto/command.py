from pydantic import BaseModel

class CommandRequestDTO(BaseModel):
  machine_name: str
  script_name: str

class CommandResultRequestDTO(BaseModel):
  result: str
