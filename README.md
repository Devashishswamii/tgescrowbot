# Telegram Escrow Bot

A secure Telegram escrow bot with admin panel for managing crypto transactions.

## 🌟 Features

- 💰 Multi-cryptocurrency support (BTC, ETH, USDT, LTC, TON, BNB, TRX)
- 🔐 Secure escrow transactions
- 📱 Telegram group creation for each deal
- 🛡️ Admin panel with session management
- 💼 Crypto address management
- 📊 User and transaction tracking
- ☁️ Cloud-ready (Koyeb + Vercel + Supabase)

## 🚀 Quick Start

### Prerequisites
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Telegram API credentials (from [my.telegram.org](https://my.telegram.org/apps))
- Supabase account
- Koyeb account (for bot hosting)
- Vercel account (for admin panel)

### Deployment

**Everything you need is in these two files:**

1. **`ENV_SETUP_GUIDE.md`** - Step-by-step environment variable setup
2. **`DEPLOYMENT_GUIDE.md`** - Detailed deployment instructions

### Quick Deploy Checklist

1. ✅ Create Supabase tables (run `supabase_crypto_addresses.sql`)
2. ✅ Run `python auth_telethon.py` to create session
3. ✅ Deploy to Koyeb with environment variables
4. ✅ Upload session file to Koyeb volumes
5. ✅ Deploy admin panel to Vercel
6. ✅ Add environment variables in Vercel

**See `ENV_SETUP_GUIDE.md` for detailed instructions!**

## 📁 Project Structure

```
TG ESCROW Bot/
├── bot.py                    # Main bot
├── telethon_service.py       # Group creation service
├── database.py               # Supabase integration
├── messages.py               # Bot messages
├── admin-panel/              # Web admin interface
│   ├── app.py
│   ├── templates/
│   └── static/
├── Dockerfile.bot            # Bot container
├── Dockerfile.telethon       # Telethon service container
├── koyeb.toml               # Koyeb configuration
├── ENV_SETUP_GUIDE.md       # 🌟 START HERE
└── DEPLOYMENT_GUIDE.md      # Deployment details
```

## 🔑 Environment Variables

See `ENV_SETUP_GUIDE.md` for the complete list and where to add them.

Required variables:
- `BOT_TOKEN` - Your Telegram bot token
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API hash
- `PHONE_NUMBER` - Your phone number
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SECRET_KEY` - Flask secret key

## 🛠️ Local Development

1. Clone the repository:
```bash
git clone https://github.com/kofficialworke-ship-it/TGBOTESCROW.git
cd TGBOTESCROW
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Create Telegram session:
```bash
python auth_telethon.py
```

5. Run the bot:
```bash
python bot.py
```

6. Run admin panel (separate terminal):
```bash
cd admin-panel
python app.py
```

## 📱 Admin Panel Features

- **Dashboard**: Overview of users and deals
- **Session Manager**: View/logout Telegram account
- **Crypto Addresses**: Manage wallet addresses
- **Users**: View all bot users
- **Settings**: Configure bot settings
- **Content**: Edit bot messages

Access at: `http://localhost:5000` (local) or your Vercel URL (deployed)

Default password: `admin123` (change immediately!)

## 🔒 Security

- Never commit `.env` or session files
- Change default admin password
- Use strong secrets for `SECRET_KEY`
- Enable 2FA on all service accounts
- Regularly rotate API keys

## 📚 Documentation

- **`ENV_SETUP_GUIDE.md`** - Environment setup (START HERE!)
- **`DEPLOYMENT_GUIDE.md`** - Full deployment guide
- **`walkthrough.md`** - Implementation details

## 🆘 Support

Check the logs in:
- **Koyeb Dashboard** for bot errors
- **Vercel Dashboard** for admin panel errors
- **Supabase Logs** for database issues

## 📄 License

MIT License - feel free to use for your projects!

## 🙏 Credits

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Telethon](https://github.com/LonamiWebs/Telethon)
- [Supabase](https://supabase.com)
- [Flask](https://flask.palletsprojects.com/)

---

**Repository**: https://github.com/kofficialworke-ship-it/TGBOTESCROW  
**Author**: Kofficial  
**Status**: Production Ready ✅
