-- Create Telegram Sessions Table in Supabase
-- Run this SQL in your Supabase SQL Editor

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

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_telegram_sessions_phone ON telegram_sessions(phone);
CREATE INDEX IF NOT EXISTS idx_telegram_sessions_user_id ON telegram_sessions(user_id);

-- Add RLS policies (if you're using Row Level Security)
ALTER TABLE telegram_sessions ENABLE ROW LEVEL SECURITY;

-- Allow all operations for service role (backend can do everything)
CREATE POLICY "Enable all for service role" ON telegram_sessions
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Verify table was created
SELECT * FROM telegram_sessions LIMIT 1;
