# TP-LINK TELEGRAM BOT

Telegram bot for routers TP-Link.

# Supported Devices

This bot is designed for budget models with firmware without API.
Tested on TL-WR840N v5 with firmware version 0.9.1 3.16 v0283.0.

# Run on local machine

1. Clone repository
2. Install dependencies with poetry: `poetry install`
3. Set environment variables in `.env` file
4. Run script in virtual environment: `poetry run python -m app`

# Features

-   Shows all devices connected to the router
-   Adds a device to the blacklist by mac address
-   Removes a device from the blacklist by mac address
-   Reboots the router
