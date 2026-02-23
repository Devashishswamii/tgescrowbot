"""
Telegram Authentication Module
Fetches API_ID and API_HASH from Supabase (configured via admin panel Settings tab).
"""
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    FloodWaitError
)

def _get_tg_credentials():
    """Fetch API_ID and API_HASH from Supabase config table."""
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL', '')
        key = os.getenv('SUPABASE_KEY', '')
        if not url or not key:
            raise ValueError("Supabase credentials not set in environment")
        sb = create_client(url, key)
        result = sb.table('config').select('key, value').in_('key', [
            'telegram_api_id', 'telegram_api_hash', 'telegram_phone'
        ]).execute()
        creds = {row['key']: row['value'] for row in (result.data or [])}
        api_id = int(creds.get('telegram_api_id') or os.getenv('API_ID', '0'))
        api_hash = creds.get('telegram_api_hash') or os.getenv('API_HASH', '')
        phone = creds.get('telegram_phone') or os.getenv('PHONE_NUMBER', '')
        return api_id, api_hash, phone
    except Exception as e:
        print(f"[telegram_auth] Error fetching credentials from Supabase: {e}")
        # Fallback to env
        return (
            int(os.getenv('API_ID', '0')),
            os.getenv('API_HASH', ''),
            os.getenv('PHONE_NUMBER', '')
        )


class TelegramAuth:
    def __init__(self):
        self.api_id, self.api_hash, self.phone = _get_tg_credentials()

    def _check_creds(self):
        if not self.api_id or not self.api_hash:
            return False, "API_ID and API_HASH not configured. Go to Admin Panel â†’ Settings â†’ Telegram API Credentials."
        return True, None

    async def send_code(self, phone):
        """Send verification code and return temp session + phone_code_hash"""
        ok, err = self._check_creds()
        if not ok:
            return {'success': False, 'error': err}

        client = None
        try:
            client = TelegramClient(StringSession(), self.api_id, self.api_hash)
            await client.connect()
            result = await client.send_code_request(phone)
            temp_session = client.session.save()
            phone_code_hash = result.phone_code_hash
            await client.disconnect()
            return {
                'success': True,
                'temp_session': temp_session,
                'phone_code_hash': phone_code_hash,
                'phone': phone
            }
        except FloodWaitError as e:
            if client: await client.disconnect()
            return {'success': False, 'error': f'Too many requests. Wait {e.seconds} seconds.'}
        except Exception as e:
            if client: await client.disconnect()
            return {'success': False, 'error': f'Error: {str(e)}'}

    async def verify_code(self, temp_session, phone, code, phone_code_hash):
        """Verify OTP code"""
        ok, err = self._check_creds()
        if not ok:
            return {'success': False, 'error': err}

        client = None
        try:
            client = TelegramClient(StringSession(temp_session), self.api_id, self.api_hash)
            await client.connect()
            try:
                await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
                session_string = client.session.save()
                me = await client.get_me()
                user_data = {
                    'id': me.id, 'phone': me.phone, 'username': me.username,
                    'first_name': me.first_name, 'last_name': me.last_name
                }
                await client.disconnect()
                return {'success': True, 'session_string': session_string, 'user_data': user_data}
            except SessionPasswordNeededError:
                temp_session_2fa = client.session.save()
                await client.disconnect()
                return {'success': False, 'requires_password': True, 'temp_session': temp_session_2fa}
        except PhoneCodeInvalidError:
            if client and client.is_connected(): await client.disconnect()
            return {'success': False, 'error': 'Invalid code. Please check and try again.'}
        except PhoneCodeExpiredError:
            if client and client.is_connected(): await client.disconnect()
            return {'success': False, 'error': 'Code expired. Click Start Over to get a new code.', 'expired': True}
        except Exception as e:
            if client and client.is_connected(): await client.disconnect()
            return {'success': False, 'error': f'Error: {str(e)}'}

    async def verify_password(self, temp_session, password):
        """Complete 2FA login"""
        ok, err = self._check_creds()
        if not ok:
            return {'success': False, 'error': err}

        client = None
        try:
            client = TelegramClient(StringSession(temp_session), self.api_id, self.api_hash)
            await client.connect()
            await client.sign_in(password=password)
            session_string = client.session.save()
            me = await client.get_me()
            user_data = {
                'id': me.id, 'phone': me.phone, 'username': me.username,
                'first_name': me.first_name, 'last_name': me.last_name
            }
            await client.disconnect()
            return {'success': True, 'session_string': session_string, 'user_data': user_data}
        except Exception as e:
            if client and client.is_connected(): await client.disconnect()
            return {'success': False, 'error': f'Invalid password: {str(e)}'}


async def get_telegram_client(session_string, api_id=None, api_hash=None):
    """Get an authenticated Telegram client from saved session."""
    if not api_id or not api_hash:
        api_id, api_hash, _ = _get_tg_credentials()
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        return None
    return client


async def create_escrow_group(session_string, title, description=""):
    """Create a Telegram group using saved session."""
    client = await get_telegram_client(session_string)
    if not client:
        return {'success': False, 'error': 'Session invalid or expired. Please re-login via admin panel.'}
    try:
        result = await client.create_channel(title=title, about=description, megagroup=True)
        group_id = result.chats[0].id
        await client.disconnect()
        return {'success': True, 'group_id': group_id, 'title': title}
    except Exception as e:
        if client.is_connected(): await client.disconnect()
        return {'success': False, 'error': str(e)}
