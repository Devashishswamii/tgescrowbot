import os
from datetime import datetime

# Database module v1.2 - With Telegram session support

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Initialize Supabase client
try:
    from supabase import create_client, Client
    if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "YOUR_SUPABASE_URL_HERE":
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        print("⚠️ WARNING: Supabase credentials not configured. Using mock database.")
        supabase = None
except Exception as e:
    print(f"❌ Error initializing Supabase: {e}")
    supabase = None

def init_db():
    """Initialize database tables in Supabase"""
    if not supabase:
        print("⚠️ Database not initialized - Supabase client is None")
        return
    
    try:
        result = supabase.table('config').select('*').eq('key', 'admin_username').execute()
        if not result.data:
            supabase.table('config').insert([
                {'key': 'admin_username', 'value': 'MiddleCryptoSupport'},
                {'key': 'admin_password', 'value': 'admin123'}
            ]).execute()
        
        result = supabase.table('statistics').select('*').eq('key', 'total_deals').execute()
        if not result.data:
            supabase.table('statistics').insert([
                {'key': 'total_deals', 'value': 5542},
                {'key': 'disputes_resolved', 'value': 158}
            ]).execute()
        
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database init error: {e}")

def get_statistics():
    """Get current bot statistics"""
    if not supabase:
        return {'total_deals': 0, 'disputes_resolved': 0}
    
    try:
        result = supabase.table('statistics').select('*').execute()
        stats = {}
        for row in result.data:
            stats[row['key']] = row['value']
        return stats
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {'total_deals': 0, 'disputes_resolved': 0}

def get_all_bot_users():
    """Get all bot users"""
    if not supabase:
        return []
    
    try:
        result = supabase.table('bot_users').select('*').order('started_at', desc=True).execute()
        return [(u['user_id'], u.get('username'), u.get('first_name'), u.get('last_name'), u.get('started_at')) 
                for u in result.data] if result.data else []
    except Exception as e:
        print(f"Error getting bot users: {e}")
        return []

def get_config(key):
    """Get configuration value"""
    if not supabase:
        return None
    try:
        result = supabase.table('config').select('value').eq('key', key).execute()
        return result.data[0]['value'] if result.data else None
    except Exception as e:
        print(f"Error getting config: {e}")
        return None

def update_config(key, value):
    """Update configuration value"""
    if not supabase:
        return False
    try:
        supabase.table('config').upsert({'key': key, 'value': value}).execute()
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def get_all_editable_content():
    """Get all editable content"""
    if not supabase:
        return []
    try:
        result = supabase.table('editable_content').select('*').order('updated_at', desc=True).execute()
        return [(c['key'], c['content'], c['updated_at']) for c in result.data]
    except Exception as e:
        print(f"Error getting editable content: {e}")
        return []

def update_editable_content(key, content):
    """Update editable content"""
    if not supabase:
        return False
    try:
        supabase.table('editable_content').upsert({
            'key': key,
            'content': content,
            'updated_at': datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        print(f"Error updating editable content: {e}")
        return False

def get_crypto_addresses():
    """Get all crypto addresses"""
    if not supabase:
        return []
    try:
        result = supabase.table('crypto_addresses').select('*').order('created_at', desc=True).execute()
        return [(a['id'], a['currency'], a['address'], a['network'], a['label'], a['created_at']) 
                for a in result.data]
    except Exception as e:
        print(f"Error getting crypto addresses: {e}")
        return []

def add_crypto_address(currency, address, network='', label=''):
    """Add a new crypto address"""
    if not supabase:
        return False
    try:
        supabase.table('crypto_addresses').insert({
            'currency': currency,
            'address': address,
            'network': network,
            'label': label
        }).execute()
        return True
    except Exception as e:
        print(f"Error adding crypto address: {e}")
        return False

def delete_crypto_address(address_id):
    """Delete a crypto address"""
    if not supabase:
        return False
    try:
        supabase.table('crypto_addresses').delete().eq('id', address_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting crypto address: {e}")
        return False

def update_crypto_address(address_id, currency, address, network='', label=''):
    """Update a crypto address"""
    if not supabase:
        return False
    try:
        supabase.table('crypto_addresses').update({
            'currency': currency,
            'address': address,
            'network': network,
            'label': label
        }).eq('id', address_id).execute()
        return True
    except Exception as e:
        print(f"Error updating crypto address: {e}")
        return False

# Telegram Session Management
def save_telegram_session(session_string, phone, user_data=None):
    """Save Telegram session string to database"""
    if not supabase:
        return False
    
    try:
        data = {
            'session_string': session_string,
            'phone': phone,
            'user_id': user_data.get('id') if user_data else None,
            'username': user_data.get('username') if user_data else None,
            'first_name': user_data.get('first_name') if user_data else None,
            'last_name': user_data.get('last_name') if user_data else None,
            'updated_at': datetime.now().isoformat()
        }
        
        # Check if session exists
        result = supabase.table('telegram_sessions').select('*').eq('phone', phone).execute()
        
        if result.data:
            # Update existing
            supabase.table('telegram_sessions').update(data).eq('phone', phone).execute()
        else:
            # Insert new
            data['created_at'] = datetime.now().isoformat()
            supabase.table('telegram_sessions').insert(data).execute()
        
        return True
    except Exception as e:
        print(f"Error saving Telegram session: {e}")
        return False

def get_telegram_session(phone=None):
    """Get Telegram session string from database"""
    if not supabase:
        return None
    
    try:
        if phone:
            result = supabase.table('telegram_sessions').select('*').eq('phone', phone).execute()
        else:
            # Get the most recent session
            result = supabase.table('telegram_sessions').select('*').order('updated_at', desc=True).limit(1).execute()
        
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        print(f"Error getting Telegram session: {e}")
        return None

def delete_telegram_session(phone):
    """Delete Telegram session from database"""
    if not supabase:
        return False
    
    try:
        supabase.table('telegram_sessions').delete().eq('phone', phone).execute()
        return True
    except Exception as e:
        print(f"Error deleting Telegram session: {e}")
        return False
