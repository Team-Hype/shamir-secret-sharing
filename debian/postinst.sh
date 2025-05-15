#!/bin/bash

set -e

echo "[postinst] Creating shard user if not exists..."
id -u shard &>/dev/null || useradd -r -s /bin/false shard

echo "[postinst] Setting permissions..."
chown -R shard:shard /usr/local/shard
chown -R shard:shard /var/log/shard

echo "[postinst] Creating virtualenv..."
python3 -m venv /usr/local/shard/venv
source /usr/local/shard/venv/bin/activate
pip install --upgrade pip

echo "[postinst] Installing dependencies..."
pip install poetry
cd /usr/local/shard/shard
poetry install --no-root --no-dev

echo "[postinst] Enabling and starting service..."
systemctl daemon-reload
systemctl enable shard
systemctl restart shard

exit 0
