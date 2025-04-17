# API Renter Session Simulation

This project simulates the creation and status polling of a renter session using a mock version of a RESTful API.

## 🔧 What This Does

- Authenticates using mock client credentials
- Creates a renter session with test renter & property data
- Polls session status every 2 seconds
- Logs the final status to `session_status.json`

## 📁 File Structure

- `session_runner.py` — Main script
- `.env` — Stores fake credentials (must be configured in postman or other mock server tool)
- `session_status.json` — Output of approved session

## 🧪 Setup

1. Clone this repo
2. Install requirements:
   ```bash
   pip install requests python-dotenv
   python session_runner.py
