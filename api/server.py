from fastapi import FastAPI, Depends, HTTPException
from models import Base, Machine, Command, CommandStatus, Script
from db.session import engine, get_db
from sqlalchemy.orm import Session
from routes.dto.machine import MachineRequestDTO, MachineResponseDTO
from routes.dto.script import ScriptRequestDTO, ScriptResponseDTO
from routes.dto.command import CommandRequestDTO
from typing import List
import time
from uuid import UUID
from utils.date import five_minutes_ago

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/machines", response_model=List[MachineResponseDTO])
def list_machines(db: Session = Depends(get_db)):
  machines = db.query(Machine).filter(Machine.last_seen > five_minutes_ago()).all()

  return machines

@app.post("/register_machine", response_model=MachineResponseDTO)
def register_machine(machine_dto: MachineRequestDTO, db: Session = Depends(get_db)):
  if machine_dto.id:
    machine = db.query(Machine).filter(Machine.id == machine_dto.id).first()

    machine.last_seen = int(time.time())
  else:
    machine = Machine(name=machine_dto.name, last_seen=int(time.time()))
    
    db.add(machine)
    
  db.commit()

  db.refresh(machine)

  return machine

@app.post("/scripts", response_model=ScriptResponseDTO)
def scripts(script_dto: ScriptRequestDTO, db: Session = Depends(get_db)):
  new_script = Script(name = script_dto.name, content = script_dto.content)

  db.add(new_script)

  db.commit()

  db.refresh(new_script)

  return new_script

@app.post("/execute")
def execute_script(command_dto: CommandRequestDTO, db: Session = Depends(get_db)):
  machine = db.query(Machine).filter(Machine.name == command_dto.machine_name, Machine.last_seen > five_minutes_ago()).first()

  if not machine:
    raise HTTPException(status_code=404, detail="Máquina não encontrada ou inativa")

  script = db.query(Script).filter(Script.name == command_dto.script_name).first()

  if not script:
    raise HTTPException(status_code=404, detail="Script não encontrado")
  
  new_command = Command(machine_id=machine.id, script_name=script.name)

  db.add(new_command)

  db.commit()

  db.refresh(new_command)

  return new_command

@app.get("/commands/{machine_id}")
def list_machine_commands(machine_id: UUID, db: Session = Depends(get_db)):
  commands = db.query(Command).filter(
    Command.machine_id == machine_id,
    Command.status == CommandStatus.PENDING
  ).all()

  return commands

@app.post("/commands/{command_id}/result")
def get_command_result(command_id: UUID, db: Session = Depends(get_db)):
  command = db.query(Command).filter(Command.id == command_id).first()

  if not command:
    raise HTTPException(status_code=404, detail="Comando não encontrado!")
  

  return command.output