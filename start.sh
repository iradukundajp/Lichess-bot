#!/bin/sh
set -e

# 1) If config.yml doesn’t exist in the container, copy the default
if [ ! -f config.yml ]; then
  cp config.yml.default config.yml
fi

# 2) Inject the token from the environment into config.yml
python - << 'EOF'
import os, yaml

path = "config.yml"
with open(path) as f:
    data = yaml.safe_load(f)

token = os.environ.get("LICHESS_TOKEN")
if not token:
    raise SystemExit("LICHESS_TOKEN environment variable is not set!")

data["token"] = token

with open(path, "w") as f:
    yaml.safe_dump(data, f)
EOF

# 3) Start the bot
exec python3 lichess-bot.py
