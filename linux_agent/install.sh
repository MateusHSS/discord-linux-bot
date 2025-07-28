#!/bin/bash

set -e

SERVICE_NAME=discord_linux_bot
INSTALL_DIR=/opt/discord_linux_bot
ENV_FILE=$INSTALL_DIR/.env
VENV_DIR=$INSTALL_DIR/venv
PYTHON_EXEC=$(which python3)

echo "🔧 Instalando o agente Discord Linux..."

# 1. Cria o diretório da aplicação
sudo mkdir -p $INSTALL_DIR
sudo cp -r ./* $INSTALL_DIR
sudo cp .env $INSTALL_DIR
sudo chmod +x $INSTALL_DIR/agent.py

# 2. Gera o UUID da máquina e salva no .env
if [ ! -f "$ENV_FILE" ]; then
  echo "🔑 Gerando UUID da máquina..."
  UUID=$(uuidgen)
  echo "MACHINE_ID=$UUID" | sudo tee -a $ENV_FILE
fi

# 3. Cria e ativa o ambiente virtual
echo "🐍 Criando ambiente virtual..."
sudo $PYTHON_EXEC -m venv $VENV_DIR

# 4. Instala dependências no venv
echo "📦 Instalando dependências no ambiente virtual..."
sudo $VENV_DIR/bin/pip install --upgrade pip
sudo $VENV_DIR/bin/pip install -r $INSTALL_DIR/requirements.txt

# 4. Cria o serviço systemd
echo "🛠️ Criando serviço systemd..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOL
[Unit]
Description=Agente de integração com bot do discord
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $INSTALL_DIR/agent.py
WorkingDirectory=$INSTALL_DIR
EnvironmentFile=$ENV_FILE
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOL

# 5. Recarrega systemd e inicia o serviço
echo "🚀 Iniciando serviço..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "✅ Instalação concluída com sucesso!"
