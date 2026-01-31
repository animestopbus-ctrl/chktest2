# ========================================================
# LastPerson07XRexbots V2
# Don't Remove Credit 🥺
# Telegram Channel @RexBots_Official
#
# Maintained & Updated by:
# Dhanpal Sharma
# GitHub: https://github.com/LastPerson07
# DEVs: 1. @DmOwner 2. @akaza7902
# ========================================================

FROM python:3.12.9-slim-bookworm

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure logs are shown instantly
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start ONLY the bot
# Flask keep_alive server handles port binding
CMD ["python3", "bot.py"]

# ========================================================
# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
#
# Updated & Managed by:
# Dhanpal Sharma | https://github.com/LastPerson07
# DEVs: 1. @DmOwner 2. @akaza7902
# ========================================================