import os
import aiohttp
from dotenv import load_dotenv
from logger import setup_logger
import asyncio
import subprocess

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
MACHINE_ID = os.getenv("MACHINE_ID")
MACHINE_NAME = os.getenv("MACHINE_NAME")
logger = setup_logger("linux_agent")

async def ping():
  try:
    async with aiohttp.ClientSession() as session:
      payload = {'id': MACHINE_ID, 'name': MACHINE_NAME}

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
      async with session.get(f"{SERVER_URL}/commands/{MACHINE_ID}") as response:
        if response.status == 200:
          data = await response.json()

          for command in data:
            result = subprocess.run(command['script']['content'], capture_output=True, text=True)
            
            async with session.post(f"{SERVER_URL}/commands/{command['id']}/result", json={'result': result.stdout}) as res:
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