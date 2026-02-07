-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Config Table
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Insert Default Config
INSERT INTO config (key, value) VALUES 
('admin_username', 'MiddleCryptoSupport'),
('admin_password', 'admin123')
ON CONFLICT (key) DO NOTHING;

-- 2. Statistics Table
CREATE TABLE IF NOT EXISTS statistics (
    key TEXT PRIMARY KEY,
    value BIGINT
);

-- Insert Default Stats
INSERT INTO statistics (key, value) VALUES 
('total_deals', 5542),
('disputes_resolved', 158)
ON CONFLICT (key) DO NOTHING;

-- 3. Bot Users Table
CREATE TABLE IF NOT EXISTS bot_users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Editable Content Table
CREATE TABLE IF NOT EXISTS editable_content (
    key TEXT PRIMARY KEY,
    content TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Crypto Addresses Table
CREATE TABLE IF NOT EXISTS crypto_addresses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    currency TEXT NOT NULL,
    address TEXT NOT NULL,
    network TEXT,
    label TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Telegram Sessions Table
CREATE TABLE IF NOT EXISTS telegram_sessions (
    phone TEXT PRIMARY KEY,
    session_string TEXT NOT NULL,
    user_id BIGINT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Media Files Table
CREATE TABLE IF NOT EXISTS media_files (
    file_type TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    description TEXT,
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Webhook Settings Table (Optional, if used)
CREATE TABLE IF NOT EXISTS webhook_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
