#!/bin/bash

set -e

echo "[postrm] Removing shard files..."

# Remove if not 'upgrade'
if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    rm -rf /opt/shard
    rm -rf /var/log/shard
    rm -f /etc/shard/config.ini
    rm -f /lib/systemd/system/shard.service

    # No delete user if 'remove'
    if [ "$1" = "purge" ]; then
        if id "shard" &>/dev/null; then
            userdel shard
        fi
    fi
fi

echo "[postrm] Reloading systemd daemon..."
systemctl daemon-reload || true

echo "[postrm] Done."
exit 0
