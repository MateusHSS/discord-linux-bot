import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiohttp
from datetime import datetime
from logger import setup_logger

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")

logger = setup_logger("discord_bot")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
  logger.info(f"Logado como {bot.user}")

@bot.command(name="list_machines")
async def list_machines(ctx):
  
  async with aiohttp.ClientSession() as session:
    try:
      async with session.get(f"{SERVER_URL}/machines") as response:
        if response.status == 200:
          data = await response.json()

          if not data:
            await ctx.send("Nenhuma máquina ativa no momento")
            return

          msg = ""

          for maquina in data:
            msg += f"- Nome: {maquina['name']} - Visto por último: {datetime.fromtimestamp(maquina['last_seen']).strftime('%d/%m/%Y %H:%M:%S')}\n"

          await ctx.send(msg)
        else:
          await ctx.send(f"Erro ao buscar máquinas: código {response.status}")

    except Exception as e:
      await ctx.send(f"Erro de conexão: {e}")

@bot.command(name="register_script")
async def register_script(ctx, name: str = None, content: str = None):
  if not name or not content: 
    await ctx.send(f"O uso correto do comando é `!register_script <nome> <conteúdo>`")
    return
  
  payload = {
    "name": name,
    "content": content
  }

  async with aiohttp.ClientSession() as session:
    try:
      async with session.post(f"{SERVER_URL}/scripts", json=payload) as response:
        if response.status == 200:
          await ctx.send(f"Script `{name}` registrado com sucesso!")
        else:
          error = await response.text()
          logger.error(f"Erro ao registrar script: `{response.status}`\n {error}")
          await ctx.send(f"Erro ao registrar script: `{response.status}`\n{error}")
    except Exception as e:
      logger.error(f"Erro de conexão: {e}")
      await ctx.send(f"Erro de conexão: {e}")

@bot.command(name="execute_script")
async def execute_script(ctx, machine_name: str = None, script_name: str = None):
  if not machine_name or not script_name:
    await ctx.send(f"O uso correto do comando é `!execute_script <nome_máquina> <nome_script>`")
    return
  
  payload = {
    'machine_name': machine_name,
    'script_name': script_name
  }

  async with aiohttp.ClientSession() as session:
    try:
      async with session.post(f"{SERVER_URL}/execute", json=payload) as response:
        if(response.status == 200):
          await ctx.send(f"Script {script_name} agendado para execução na máquina {machine_name}")
        else:
          error = await response.text()
          await ctx.send(f"Erro ao agendar execução do script {script_name}\n{error}")
    except Exception as e:
      await ctx.send(f"Erro de conexão: {e}")

bot.run(os.getenv("BOT_TOKEN"))