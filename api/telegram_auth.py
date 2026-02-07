"""
Telegram Authentication Module
Uses Telethon with StringSession for serverless compatibility
"""
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

class TelegramAuth:
    def __init__(self):
        self.api_id = os.getenv('API_ID', '34829504')
        self.api_hash = os.getenv('API_HASH', '')
        self.client = None
        self.phone = None
        self.phone_code_hash = None
        
    async def send_code(self, phone):
        """Send verification code to phone number"""
        try:
            # Create client with empty StringSession for new login
            self.client = TelegramClient(StringSession(), self.api_id, self.api_hash)
            await self.client.connect()
            
            # Send code
            self.phone = phone
            result = await self.client.send_code_request(phone)
            self.phone_code_hash = result.phone_code_hash
            
            return {
                'success': True,
                'phone_code_hash': self.phone_code_hash,
                'message': f'Verification code sent to {phone}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def verify_code(self, phone, code, phone_code_hash):
        """Verify the code and complete login"""
        try:
            if not self.client:
                self.client = TelegramClient(StringSession(), self.api_id, self.api_hash)
                await self.client.connect()
            
            self.phone = phone
            self.phone_code_hash = phone_code_hash
            
            # Sign in with code
            try:
                await self.client.sign_in(phone, code, phone_code_hash=phone_code_hash)
            except SessionPasswordNeededError:
                # 2FA is enabled
                return {
                    'success': False,
                    'requires_password': True,
                    'message': '2FA enabled. Please enter your password.'
                }
            
            # Get session string
            session_string = self.client.session.save()
            
            # Get user info
            me = await self.client.get_me()
            user_data = {
                'id': me.id,
                'phone': me.phone,
                'username': me.username,
                'first_name': me.first_name,
                'last_name': me.last_name
            }
            
            await self.client.disconnect()
            
            return {
                'success': True,
                'session_string': session_string,
                'user_data': user_data,
                'message': 'Successfully logged in!'
            }
            
        except PhoneCodeInvalidError:
            return {
                'success': False,
                'error': 'Invalid verification code. Please try again.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def verify_password(self, password):
        """Verify 2FA password"""
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': 'Session expired. Please start over.'
                }
            
            # Sign in with password
            await self.client.sign_in(password=password)
            
            # Get session string
            session_string = self.client.session.save()
            
            # Get user info
            me = await self.client.get_me()
            user_data = {
                'id': me.id,
                'phone': me.phone,
                'username': me.username,
                'first_name': me.first_name,
                'last_name': me.last_name
            }
            
            await self.client.disconnect()
            
            return {
                'success': True,
                'session_string': session_string,
                'user_data': user_data,
                'message': 'Successfully logged in with 2FA!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_session_info(self, session_string):
        """Get info about an existing session"""
        try:
            client = TelegramClient(StringSession(session_string), self.api_id, self.api_hash)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.disconnect()
                return None
            
            me = await client.get_me()
            user_data = {
                'id': me.id,
                'phone': me.phone,
                'username': me.username,
                'first_name': me.first_name,
                'last_name': me.last_name
            }
            
            await client.disconnect()
            return user_data
            
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None
