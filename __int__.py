# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

import base64
import sys

# Hidden anti-leech check (obfuscated)
def _check_credits():
    cred = "REVWczogMS4gQERtT3duZXIgMi4gQGFrYXphNzkwMg=="  # base64 of "DEVs: 1. @DmOwner 2. @akaza7902"
    if base64.b64decode(cred).decode() != "DEVs: 1. @DmOwner 2. @akaza7902":
        sys.exit("Credits altered - Bot breaking...")  # Breaks if changed
    # Additional hidden check: If community string missing, infinite loop
    comm = "Q29tbXVuaXR5OiBAUmV4Qm90c19PZmZpY2lhbA=="  # base64 of "Community: @RexBots_Official"
    if base64.b64decode(comm).decode() != "Community: @RexBots_Official":
        while True:
            pass  # Infinite loop breaks bot

_check_credits()  # Exec on import

from LastPerson07XRexbots.database.db import db

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902