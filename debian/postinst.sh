#!/bin/bash

set -xe

shard_path="/opt/shard"
log_path="/var/log/shard"

echo "[postinst] Creating shard user if not exists..."
if ! id "shard" &>/dev/null; then
    useradd --system --no-create-home --shell /usr/sbin/nologin shard || {
        echo "[postinst] Failed to add user" >&2
        exit 1
    }
    echo "[postinst] User 'shard' created"
else
    echo "[postinst] User 'shard' already exists"
fi

echo "[postinst] Ensuring log directory exists..."
mkdir -p "$log_path"

echo "[postinst] Setting permissions..."
chown -R shard:shard "$shard_path"
chown -R shard:shard "$log_path"

echo "[postinst] Creating virtualenv..."
python3 -m venv "$shard_path/venv"

echo "[postinst] Installing dependencies..."
source "$shard_path/venv/bin/activate"
pip install --upgrade pip
pip install poetry

cd "$shard_path"
poetry install --no-root

echo "[postinst] Done."

exit 0
