# Zabbix Notification Telegram

This project provides a Telegram bot and a small Django web application for interacting with a Zabbix server via its API. The bot can acknowledge events, send graphs and history, list active problems and download an Excel sheet with offline hosts.

## Requirements
* Python 3
* A running Zabbix server with API access

## Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r .requirements
   ```
3. Edit `webapp/settings.py` and update the Telegram token and Zabbix API connection parameters.

## Usage
Start the polling bot:
```bash
python3 bot.py
```

Run the web application for API access:
```bash
python3 webapp/manage.py runserver
```

The endpoint `/offline/` returns offline hosts for an authorised Telegram ID. Inline buttons in the bot allow viewing event history, last values, graphs, active problems and downloading an offline host list.

