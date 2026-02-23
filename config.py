import os
from dotenv import load_dotenv

load_dotenv()

# â”€â”€â”€ REQUIRED: Only these 3 must be in .env â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# â”€â”€â”€ ADMIN â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ADMIN_PANEL_URL = os.getenv("ADMIN_PANEL_URL", "http://localhost:5000")
ADMIN_PANEL_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "escrow-secret-key")

# Admin user IDs (still from env for security, comma-separated)
ADMIN_USERNAMES = [u.strip() for u in os.getenv("ADMIN_USERNAMES", "@MiddleCryptoSupport").split(",")]
try:
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
except (ValueError, TypeError):
    ADMIN_USER_ID = 0
ADMIN_USER_IDS = []

# â”€â”€â”€ TELEGRAM API CREDS: Fetched from Supabase (configured via admin panel) â”€â”€â”€
# These are NOT in .env â€” set them in Admin Panel â†’ Settings â†’ Telegram API
_tg_creds_cache = {}

def _get_supabase_config(key, default=None):
    """Fetch a config value from Supabase config table."""
    try:
        from supabase import create_client
        sb = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = sb.table('config').select('value').eq('key', key).execute()
        if result.data:
            return result.data[0]['value']
    except Exception as e:
        print(f"[config] Could not fetch '{key}' from Supabase: {e}")
    return default

def get_api_id():
    """Get API_ID - from Supabase first, fallback to env."""
    if 'api_id' not in _tg_creds_cache:
        val = _get_supabase_config('telegram_api_id') or os.getenv('API_ID', '0')
        try:
            _tg_creds_cache['api_id'] = int(val)
        except (ValueError, TypeError):
            _tg_creds_cache['api_id'] = 0
    return _tg_creds_cache['api_id']

def get_api_hash():
    """Get API_HASH - from Supabase first, fallback to env."""
    if 'api_hash' not in _tg_creds_cache:
        _tg_creds_cache['api_hash'] = _get_supabase_config('telegram_api_hash') or os.getenv('API_HASH', '')
    return _tg_creds_cache['api_hash']

def get_phone_number():
    """Get PHONE_NUMBER - from Supabase first, fallback to env."""
    if 'phone_number' not in _tg_creds_cache:
        _tg_creds_cache['phone_number'] = _get_supabase_config('telegram_phone') or os.getenv('PHONE_NUMBER', '')
    return _tg_creds_cache['phone_number']

def clear_tg_creds_cache():
    """Call this after saving new credentials via admin panel."""
    global _tg_creds_cache
    _tg_creds_cache = {}

# Legacy compatibility â€” use get_api_id() etc. where possible
# These will be 0/'' if not set in Supabase yet
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '')

MEDIA_DIR = "media"
MAX_VIDEO_SIZE_MB = 50
