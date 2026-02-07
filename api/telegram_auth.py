"""
Telegram Authentication Module - PROPER FIX
Stores both temp_session AND phone_code_hash
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

class TelegramAuth:
    def __init__(self):
        self.api_id = int(os.getenv('API_ID', '34829504'))
        self.api_hash = os.getenv('API_HASH', '')
        
    async def send_code(self, phone):
        """Send verification code and return temp session + phone_code_hash"""
        client = None
        try:
            client = TelegramClient(StringSession(), self.api_id, self.api_hash)
            await client.connect()
            
            # Send code request
            result = await client.send_code_request(phone)
            
            # Save session AND phone_code_hash
            temp_session = client.session.save()
            phone_code_hash = result.phone_code_hash
            
            await client.disconnect()
            
            return {
                'success': True,
                'temp_session': temp_session,
                'phone_code_hash': phone_code_hash,  # Need this too!
                'phone': phone
            }
            
        except FloodWaitError as e:
            if client:
                await client.disconnect()
            return {
                'success': False,
                'error': f'Too many requests. Wait {e.seconds} seconds.'
            }
        except Exception as e:
            if client:
                await client.disconnect()
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    async def verify_code(self, temp_session, phone, code, phone_code_hash):
        """Verify code using temp session AND phone_code_hash"""
        client = None
        try:
            # Restore client from temp session
            client = TelegramClient(StringSession(temp_session), self.api_id, self.api_hash)
            await client.connect()
            
            # Sign in with code AND phone_code_hash
            try:
                await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
                
                # Success!
                session_string = client.session.save()
                me = await client.get_me()
                
                user_data = {
                    'id': me.id,
                    'phone': me.phone,
                    'username': me.username,
                    'first_name': me.first_name,
                    'last_name': me.last_name
                }
                
                await client.disconnect()
                
                return {
                    'success': True,
                    'session_string': session_string,
                    'user_data': user_data
                }
                
            except SessionPasswordNeededError:
                # 2FA enabled
                temp_session_2fa = client.session.save()
                await client.disconnect()
                
                return {
                    'success': False,
                    'requires_password': True,
                    'temp_session': temp_session_2fa
                }
                
        except PhoneCodeInvalidError:
            if client and client.is_connected():
                await client.disconnect()
            return {
                'success': False,
                'error': 'Invalid code. Please check and try again.'
            }
        except PhoneCodeExpiredError:
            if client and client.is_connected():
                await client.disconnect()
            return {
                'success': False,
                'error': 'Code expired. Click Start Over to get a new code.',
                'expired': True
            }
        except Exception as e:
            if client and client.is_connected():
                await client.disconnect()
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
    
    async def verify_password(self, temp_session, password):
        """Complete 2FA login"""
        client = None
        try:
            client = TelegramClient(StringSession(temp_session), self.api_id, self.api_hash)
            await client.connect()
            
            await client.sign_in(password=password)
            
            session_string = client.session.save()
            me = await client.get_me()
            
            user_data = {
                'id': me.id,
                'phone': me.phone,
                'username': me.username,
                'first_name': me.first_name,
                'last_name': me.last_name
            }
            
            await client.disconnect()
            
            return {
                'success': True,
                'session_string': session_string,
                'user_data': user_data
            }
            
        except Exception as e:
            if client and client.is_connected():
                await client.disconnect()
            return {
                'success': False,
                'error': f'Invalid password: {str(e)}'
            }

# Helper functions
async def get_telegram_client(session_string, api_id=None, api_hash=None):
    """Get Telegram client from saved session"""
    if not api_id:
        api_id = int(os.getenv('API_ID', '34829504'))
    if not api_hash:
        api_hash = os.getenv('API_HASH', '')
    
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.disconnect()
        return None
    
    return client

async def create_escrow_group(session_string, title, description=""):
    """Create Telegram group using saved session"""
    client = await get_telegram_client(session_string)
    if not client:
        return {'success': False, 'error': 'Session invalid'}
    
    try:
        result = await client.create_channel(
            title=title,
            about=description,
            megagroup=True
        )
        
        group_id = result.chats[0].id
        await client.disconnect()
        
        return {
            'success': True,
            'group_id': group_id,
            'title': title
        }
        
    except Exception as e:
        if client.is_connected():
            await client.disconnect()
        return {'success': False, 'error': str(e)}
