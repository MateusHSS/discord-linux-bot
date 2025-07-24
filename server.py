from fastapi import FastAPI
from models import Base, Machine, Script, Command
from db.session import engine, SessionLocal
from sqlalchemy import inspect

# Criar as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI()

session = SessionLocal()

@app.get("/machines")
def list_machines():
  machines = session.query(Machine).all()
  return {"machines": machines}

@app.post("/register_machine")
def register_machine():
  return "To be implemented..."

@app.post("/scripts")
def scripts():
  return "To be implemented..."

@app.post("/execute")
def read_root():
  return "To be implemented..."

@app.get("/commands/{machine_id}")
def list_machine_commands():
  return "To be implemented..."

@app.post("/commands/{command_id}/result")
def get_command_result():
  return "To be implemented..."


# # Exemplo de uso
# if __name__ == "__main__":
#     # session = SessionLocal()

#     # inspector = inspect(engine)

#     # tabelas = inspector.get_table_names(schema='public')

#     # print(f"Tabelas: {tabelas}")