# 🤖 LastPerson07XRexbots Save Restricted Content Bot V2

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Pyrofork-v2.3-yellow?style=for-the-badge&logo=telegram">
  <img src="https://img.shields.io/badge/MongoDB-Database-green?style=for-the-badge&logo=mongodb">
</p>

An advanced Telegram bot by **LastPerson07XRexbots** (V2 Upgrade) designed to save restricted content from channels. Supports high traffic, dynamic wallpapers, and anti-leech protection.

## 🚀 V2 Features (Upgrades)

- **High Traffic Optimized**: Handles 1000+ users with rate limiting and increased workers.
- **Dynamic Wallpapers**: Fetches random wallpapers via API (Picsum.photos) for UI.
- **Interconnected Settings**: All features (caption, thumbnail, words, session, etc.) in one menu.
- **Anti-Leech**: Hidden checks break bot if credits altered.
- **Batch Downloading**, **User Login**, **Premium System**, **Customizations**.

## 🛠 Deployment

### Prerequisites

- Python 3.12
- MongoDB
- Telegram API ID/Hash/Bot Token

### Environment Variables

| Variable         | Description                 |
| :--------------- | :-------------------------- |
| `BOT_TOKEN`      | Bot Token                   |
| `API_ID`         | API ID                      |
| `API_HASH`       | API Hash                    |
| `ADMINS`         | Admin IDs (comma-separated) |
| `DB_URI`         | MongoDB URI                 |
| `DB_NAME`        | DB Name                     |
| `LOG_CHANNEL`    | Log Channel ID              |
| `ERROR_MESSAGE`  | True/False for errors       |
| `KEEP_ALIVE_URL` | For keep-alive              |

### Local Run

```bash
git clone https://github.com/your-repo
cd your-repo
pip install -r requirements.txt
python3 bot.py
```
