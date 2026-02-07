"""
Telegram Authentication Module - WORKING VERSION
Uses Telethon with StringSession for serverless
Properly handles verification codes
"""
import os
import asyncio
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
        """Send verification code to phone number"""
        client = None
        try:
            # Create new client
            client = TelegramClient(StringSession(), self.api_id, self.api_hash)
            await client.connect()
            
            # Send code request
            result = await client.send_code_request(phone)
            
            await client.disconnect()
            
            return {
                'success': True,
                'phone_code_hash': result.phone_code_hash,
                'phone': phone
            }
            
        except FloodWaitError as e:
            if client:
                await client.disconnect()
            return {
                'success': False,
                'error': f'Too many requests. Please wait {e.seconds} seconds.'
            }
        except Exception as e:
            if client:
                await client.disconnect()
            return {
                'success': False,
                'error': f'Error sending code: {str(e)}'
            }
    
    async def verify_code(self, phone, code, phone_code_hash):
        """Verify the code and sign in"""
        client = None
        try:
            # Create new client
            client = TelegramClient(StringSession(), self.api_id, self.api_hash)
            await client.connect()
            
            # Try to sign in with the code
            try:
                await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
                
                # Success! Get session and user info
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
                # 2FA enabled - save temporary session
                temp_session = client.session.save()
                await client.disconnect()
                
                return {
                    'success': False,
                    'requires_password': True,
                    'temp_session': temp_session
                }
                
        except PhoneCodeInvalidError:
            if client and client.is_connected():
                await client.disconnect()
            return {
                'success': False,
                'error': 'Invalid verification code. Please check and try again.'
            }
        except PhoneCodeExpiredError:
            if client and client.is_connected():
                await client.disconnect()
            return {
                'success': False,
                'error': 'Verification code expired. Please request a new code.',
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
        """Complete 2FA login with password"""
        client = None
        try:
            # Restore client from temp session
            client = TelegramClient(StringSession(temp_session), self.api_id, self.api_hash)
            await client.connect()
            
            # Complete sign in with password
            await client.sign_in(password=password)
            
            # Get final session and user info
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

# Helper function to get client from saved session
async def get_telegram_client(session_string, api_id=None, api_hash=None):
    """
    Get a Telegram client from a saved session string
    Use this to create groups or perform other actions
    """
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

# Example: Create a group using saved session
async def create_escrow_group(session_string, title, description=""):
    """
    Example function to create a Telegram group using saved session
    """
    client = await get_telegram_client(session_string)
    if not client:
        return {'success': False, 'error': 'Session invalid or expired'}
    
    try:
        # Create the group
        result = await client.create_channel(
            title=title,
            about=description,
            megagroup=True  # True for supergroup, False for channel
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
        return {
            'success': False,
            'error': str(e)
        }
