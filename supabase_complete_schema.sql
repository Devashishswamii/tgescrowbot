-- =============================================
-- COMPLETE SUPABASE DATABASE SCHEMA
-- Telegram Escrow Bot
-- =============================================
-- Run this ENTIRE file in Supabase SQL Editor
-- It will create all tables needed for the bot
-- =============================================

-- 1. USERS TABLE (for escrow participants)
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    role VARCHAR(20),
    wallet_address TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. BOT_USERS TABLE (tracks all users who started the bot)
CREATE TABLE IF NOT EXISTS bot_users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    started_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bot_users_username ON bot_users(username);

-- 3. DEALS TABLE (escrow transactions)
CREATE TABLE IF NOT EXISTS deals (
    id BIGSERIAL PRIMARY KEY,
    deal_id VARCHAR(50) UNIQUE NOT NULL,
    buyer_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    group_id BIGINT,
    buyer_address TEXT,
    seller_address TEXT,
    bot_address TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_deals_deal_id ON deals(deal_id);
CREATE INDEX IF NOT EXISTS idx_deals_group_id ON deals(group_id);
CREATE INDEX IF NOT EXISTS idx_deals_status ON deals(status);

-- 4. STATISTICS TABLE (bot stats)
CREATE TABLE IF NOT EXISTS statistics (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert default statistics
INSERT INTO statistics (key, value) VALUES 
    ('total_deals', 5542),
    ('disputes_resolved', 158)
ON CONFLICT (key) DO NOTHING;

-- 5. CONFIG TABLE (bot configuration)
CREATE TABLE IF NOT EXISTS config (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert default config
INSERT INTO config (key, value) VALUES 
    ('admin_username', 'MiddleCryptoSupport'),
    ('admin_password', 'admin123'),
    ('bot_address_btc', ''),
    ('bot_address_ltc', ''),
    ('bot_address_usdt_trc20', ''),
    ('bot_address_usdt_bep20', ''),
    ('bot_address_ton', '')
ON CONFLICT (key) DO NOTHING;

-- 6. MEDIA_FILES TABLE (uploaded videos/images)
CREATE TABLE IF NOT EXISTS media_files (
    id BIGSERIAL PRIMARY KEY,
    file_type VARCHAR(50) NOT NULL,
    file_path TEXT NOT NULL,
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_media_files_type ON media_files(file_type);

-- 7. EDITABLE_CONTENT TABLE (bot messages/content)
CREATE TABLE IF NOT EXISTS editable_content (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    content TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert default content
INSERT INTO editable_content (key, content) VALUES 
    ('instructions', 'Default instructions'),
    ('terms', 'Default terms and conditions'),
    ('welcome', 'Welcome to Escrow Bot!')
ON CONFLICT (key) DO NOTHING;

-- 8. CRYPTO_ADDRESSES TABLE (managed crypto wallets)
CREATE TABLE IF NOT EXISTS crypto_addresses (
    id BIGSERIAL PRIMARY KEY,
    currency VARCHAR(10) NOT NULL,
    address TEXT NOT NULL,
    network VARCHAR(50) DEFAULT '',
    label VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_crypto_addresses_currency ON crypto_addresses(currency);
CREATE INDEX IF NOT EXISTS idx_crypto_addresses_network ON crypto_addresses(currency, network);

-- =============================================
-- TRIGGERS FOR AUTO-UPDATE TIMESTAMPS
-- =============================================

-- Function to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bot_users_updated_at 
    BEFORE UPDATE ON bot_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deals_updated_at 
    BEFORE UPDATE ON deals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_statistics_updated_at 
    BEFORE UPDATE ON statistics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_config_updated_at 
    BEFORE UPDATE ON config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_editable_content_updated_at 
    BEFORE UPDATE ON editable_content
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_crypto_addresses_updated_at 
    BEFORE UPDATE ON crypto_addresses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- ROW LEVEL SECURITY (RLS) - OPTIONAL
-- =============================================
-- Uncomment if you want to enable RLS

-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE bot_users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE statistics ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE config ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE media_files ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE editable_content ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE crypto_addresses ENABLE ROW LEVEL SECURITY;

-- Create policies (allow service role full access)
-- CREATE POLICY "Allow service role all" ON users FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON bot_users FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON deals FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON statistics FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON config FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON media_files FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON editable_content FOR ALL USING (true);
-- CREATE POLICY "Allow service role all" ON crypto_addresses FOR ALL USING (true);

-- =============================================
-- VERIFICATION QUERIES
-- =============================================
-- Run these after creating tables to verify

-- Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Check statistics
SELECT * FROM statistics;

-- Check config
SELECT * FROM config;

-- =============================================
-- SUCCESS MESSAGE
-- =============================================
-- If you see this without errors, your database is ready!
-- Next step: Deploy your bot to Koyeb and admin panel to Vercel
