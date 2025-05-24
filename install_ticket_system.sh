#!/bin/bash

REPO_URL="https://github.com/yourusername/ticket-system.git" # <-- Set your repo
INSTALL_DIR="/opt/ticket-system"
PYTHON_BIN="/usr/bin/python3"
SERVICE_NAME="ticket-system-gui"

# --- UPDATE & INSTALL DEPENDENCIES ---
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk python3-serial python3-pil python3-pil.imagetk libjpeg-dev libfreetype6-dev zlib1g-dev

# --- CLONE OR UPDATE REPO ---
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing repo..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repo..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR/pi"

# --- INSTALL PYTHON REQUIREMENTS ---
if [ -f requirements.txt ]; then
    $PYTHON_BIN -m pip install --upgrade pip
    $PYTHON_BIN -m pip install -r requirements.txt
fi

# --- OPTIONAL: SETUP UDEV RULES ---
# Uncomment and edit these lines if needed for your hardware
# echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="XXXX", ATTR{idProduct}=="YYYY", MODE="0666"' | sudo tee /etc/udev/rules.d/99-ticket-printer.rules
# echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="ZZZZ", ATTR{idProduct}=="WWWW", MODE="0666"' | sudo tee /etc/udev/rules.d/99-ticket-arduino.rules
# sudo udevadm control --reload-rules

# --- INSTALL SYSTEMD SERVICE FOR GUI ---
sudo cp ticket-system-gui.service /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service

echo "Installation complete. The Ticket System GUI will start at boot."
echo "To start the service now, run: sudo systemctl start $SERVICE_NAME.service"