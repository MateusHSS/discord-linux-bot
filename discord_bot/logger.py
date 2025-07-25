import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str) -> logging.Logger:
  os.makedirs("logs", exist_ok=True)

  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG if os.getenv("ENV") == "dev" else logging.INFO)

  if logger.hasHandlers():
    return logger

  formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

  file_handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
  file_handler.setFormatter(formatter)

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  return logger