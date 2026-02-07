# URGENT: Create Telegram Sessions Table

## Problem
You're seeing: **"Login successful but failed to save session"**

This means the `telegram_sessions` table doesn't exist in your Supabase database.

## SOLUTION (2 minutes)

### Step 1: Open Supabase SQL Editor
1. Go to https://supabase.com/dashboard
2. Select your project
3. Click **SQL Editor** in the left sidebar

### Step 2: Run This SQL
Copy and paste this entire SQL into the editor and click **RUN**:

```sql
CREATE TABLE IF NOT EXISTS telegram_sessions (
    id SERIAL PRIMARY KEY,
    session_string TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    user_id BIGINT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_telegram_sessions_phone ON telegram_sessions(phone);
CREATE INDEX IF NOT EXISTS idx_telegram_sessions_user_id ON telegram_sessions(user_id);

ALTER TABLE telegram_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable all for service role" ON telegram_sessions
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

### Step 3: Verify
After running the SQL, you should see the table in:
- **Table Editor** → `telegram_sessions`

### Step 4: Try Login Again
1. Go back to your Vercel app
2. Click "Start Over"
3. Enter phone number
4. Enter code
5. ✅ **SUCCESS!** Session will save and display!

## What This Creates
- **telegram_sessions** table to store your Telegram login
- Fields: session_string, phone, user_id, username, first_name, last_name
- Indexes for fast lookups
- Security policies

## After Creating Table
Your login will work perfectly and you'll see:
- ✅ User ID
- ✅ Phone Number
- ✅ Full Name
- ✅ Session String
- ✅ Logout Button

**Do this now and try logging in again!**
