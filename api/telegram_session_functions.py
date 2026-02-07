# Telegram Session Management Functions
# Add these to your database.py

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
