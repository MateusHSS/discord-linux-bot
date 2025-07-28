import os
import aiohttp
from dotenv import load_dotenv, set_key
import uuid
from logger import setup_logger
import asyncio
import subprocess
import shlex

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
MACHINE_NAME = os.getenv("MACHINE_NAME")
ALLOWED_COMMANDS = os.getenv("ALLOWED_COMMANDS", "")
logger = setup_logger("linux_agent")

def get_machine_id():
  machine_id = os.getenv("MACHINE_ID")
  if not machine_id:
    machine_id = str(uuid.uuid4())
    set_key(".env", "MACHINE_ID", machine_id)
  
  return machine_id

def parse_allowed_commands():
    commands = {}

    for item in ALLOWED_COMMANDS.split(";"):
        if not item.strip():
            continue

        if ":" in item:
            cmd, args_str = item.split(":", 1)
            if args_str.strip() == "*":
                commands[cmd.strip()] = None
            else:
                commands[cmd.strip()] = [arg.strip() for arg in args_str.split(",")]
        else:
            commands[item.strip()] = []

    return commands

def is_safe_command(command_str):
  try:
    args = shlex.split(command_str)
    allowed_cmmds = parse_allowed_commands()

    if not args:
        return False

    command = args[0]
    cmd_args = args[1:]

    if command not in allowed_cmmds:
        return False

    allowed_args = allowed_cmmds[command]
    if allowed_args is None:
        return True

    return all(arg in allowed_args for arg in cmd_args)
  except Exception:
    return False

async def ping():
  try:
    async with aiohttp.ClientSession() as session:
      payload = {'id': get_machine_id(), 'name': MACHINE_NAME}

      async with session.post(f"{SERVER_URL}/register_machine", json=payload) as response:
        if response.status == 200:
          logger.info("Ping enviado com sucesso!")
        else:
          logger.warning(f"Ping falhou. Status: {response.status}")
  except Exception as e:
    logger.error(f"Erro ao enviar ping: {e}")

async def execute_commands():
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{SERVER_URL}/commands/{get_machine_id()}") as response:
        if response.status == 200:
          data = await response.json()
          for command in data:

            if not is_safe_command(command['script']['content']):
              logger.warning(f"Comando não permitido: {command['script']['content']}")
              result = "Comando não permitido"
            else:
              args = shlex.split(command['script']['content'])
              completed_process = subprocess.run(args, capture_output=True, text=True)

              result = completed_process.stdout if completed_process.returncode == 0 else completed_process.stderr
            
            async with session.post(f"{SERVER_URL}/commands/{command['id']}/result", json={'result': result}) as res:
              if res.status == 200:
                logger.info("Comando executado com sucesso")
              else:
                logger.warning(f"Execução do comando falhou. Status: {res.status}")
        else:
          logger.warning(f"Busca de comandos falhou: {response.status}")
  except Exception as e:
    logger.error(f"Erro ao buscar comandos: {e}")

async def main():
  while True:
    await ping()
    await execute_commands()
    await asyncio.sleep(20)

if __name__ == "__main__":
  asyncio.run(main())