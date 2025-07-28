#!/bin/bash

SERVICE_NAME=discord_linux_bot
INSTALL_DIR=/opt/discord_linux_bot

echo "🧹 Removendo agente Discord Linux..."

# Para o serviço
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME

# Remove o serviço do systemd
sudo rm -f /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload

# Remove a pasta de instalação
sudo rm -rf $INSTALL_DIR

echo "✅ Desinstalação concluída com sucesso!"