-- NMB Bank BI Portal Database Schema
-- PostgreSQL Database Schema for Authentication and User Management
-- Version: 1.0
-- Created: October 21, 2025

-- ============================================================================
-- USER MANAGEMENT
-- ============================================================================

-- Users table: Core user authentication and profile
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role_level INTEGER NOT NULL DEFAULT 4,  -- 1=Executive, 2=Manager, 3=Analyst, 4=Read-Only, 5=External
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    CONSTRAINT chk_role_level CHECK (role_level BETWEEN 1 AND 5)
);

-- Roles table: Role definitions and permissions
CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_level INTEGER UNIQUE NOT NULL,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB,  -- Flexible permissions structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_role_level_valid CHECK (role_level BETWEEN 1 AND 5)
);

-- Insert default roles
INSERT INTO roles (role_level, role_name, description, permissions) VALUES
(1, 'Executive', 'C-suite and VPs - Full access to all dashboards and export', 
 '{"dashboards": ["all"], "export": true, "admin": true}'::jsonb),
(2, 'Manager', 'Department heads - Full dashboard access with limited export', 
 '{"dashboards": ["all"], "export": "limited", "admin": false}'::jsonb),
(3, 'Analyst', 'Marketing analysts - Operational dashboards only', 
 '{"dashboards": ["operational"], "export": false, "admin": false}'::jsonb),
(4, 'Read-Only', 'Junior staff - View selected dashboards only', 
 '{"dashboards": ["selected"], "export": false, "admin": false}'::jsonb),
(5, 'External', 'Board members, consultants - Executive summary KPIs only', 
 '{"dashboards": ["executive_summary_limited"], "export": false, "admin": false}'::jsonb)
ON CONFLICT (role_level) DO NOTHING;

-- ============================================================================
-- PASSWORD RESET
-- ============================================================================

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    token_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    reset_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- USER PREFERENCES
-- ============================================================================

-- Bookmarks: Saved dashboard configurations
CREATE TABLE IF NOT EXISTS bookmarks (
    bookmark_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    dashboard_name VARCHAR(100) NOT NULL,
    bookmark_name VARCHAR(200) NOT NULL,
    filter_config JSONB,  -- Saved filters, date ranges, etc.
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Favorites: User's favorite accounts, customers, products
CREATE TABLE IF NOT EXISTS favorites (
    favorite_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    favorite_type VARCHAR(50) NOT NULL,  -- 'account', 'customer', 'product', 'branch'
    favorite_ref VARCHAR(100) NOT NULL,  -- Reference to the favorited item
    favorite_name VARCHAR(200),  -- Display name
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, favorite_type, favorite_ref)
);

-- User Settings: General user preferences
CREATE TABLE IF NOT EXISTS user_settings (
    setting_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    setting_key VARCHAR(100) NOT NULL,
    setting_value JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, setting_key)
);

-- ============================================================================
-- NOTIFICATIONS
-- ============================================================================

CREATE TABLE IF NOT EXISTS notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'info',  -- 'info', 'warning', 'alert', 'success'
    priority INTEGER DEFAULT 3,  -- 1=high, 2=medium, 3=low
    is_read BOOLEAN DEFAULT FALSE,
    link_to_dashboard VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

-- ============================================================================
-- AUDIT AND LOGGING
-- ============================================================================

-- Audit log: Track all user actions
CREATE TABLE IF NOT EXISTS audit_log (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    username VARCHAR(100),  -- Denormalized for deleted users
    action VARCHAR(100) NOT NULL,  -- 'login', 'logout', 'view_dashboard', 'export', 'update_profile'
    dashboard_accessed VARCHAR(100),
    details JSONB,  -- Additional context (filters applied, exports generated, etc.)
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session tracking
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(50),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- User indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role_level ON users(role_level);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Bookmark indexes
CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id ON bookmarks(user_id);
CREATE INDEX IF NOT EXISTS idx_bookmarks_dashboard ON bookmarks(dashboard_name);

-- Favorites indexes
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_type ON favorites(favorite_type);

-- Notification indexes
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);

-- Audit log indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);

-- Session indexes
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active);

-- ============================================================================
-- FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookmarks_updated_at BEFORE UPDATE ON bookmarks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_settings_updated_at BEFORE UPDATE ON user_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SAMPLE DATA (for development/testing)
-- ============================================================================

-- Create a default admin user (password: Admin@123456)
-- Note: This should be removed in production
INSERT INTO users (username, email, password_hash, first_name, last_name, role_level, department, is_active)
VALUES (
    'admin',
    'admin@nmbz.co.zw',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LGYj9XQWq',  -- bcrypt hash of 'Admin@123456'
    'System',
    'Administrator',
    1,
    'IT',
    TRUE
)
ON CONFLICT (username) DO NOTHING;

-- Sample notification for admin
INSERT INTO notifications (user_id, title, message, notification_type, priority)
SELECT 
    user_id,
    'Welcome to NMB BI Portal',
    'Your account has been created successfully. Please update your profile and change your password.',
    'info',
    1
FROM users WHERE username = 'admin'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- VIEWS FOR REPORTING
-- ============================================================================

-- Active users view
CREATE OR REPLACE VIEW v_active_users AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    r.role_name,
    u.department,
    u.last_login,
    u.login_count
FROM users u
JOIN roles r ON u.role_level = r.role_level
WHERE u.is_active = TRUE;

-- User activity summary
CREATE OR REPLACE VIEW v_user_activity_summary AS
SELECT 
    u.user_id,
    u.username,
    r.role_name,
    COUNT(DISTINCT DATE(a.created_at)) as active_days,
    COUNT(a.log_id) as total_actions,
    MAX(a.created_at) as last_activity,
    array_agg(DISTINCT a.dashboard_accessed) FILTER (WHERE a.dashboard_accessed IS NOT NULL) as dashboards_accessed
FROM users u
JOIN roles r ON u.role_level = r.role_level
LEFT JOIN audit_log a ON u.user_id = a.user_id
GROUP BY u.user_id, u.username, r.role_name;

-- Unread notifications view
CREATE OR REPLACE VIEW v_unread_notifications AS
SELECT 
    u.username,
    u.email,
    n.title,
    n.message,
    n.notification_type,
    n.priority,
    n.created_at
FROM notifications n
JOIN users u ON n.user_id = u.user_id
WHERE n.is_read = FALSE
ORDER BY n.priority ASC, n.created_at DESC;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE users IS 'Core user authentication and profile information';
COMMENT ON TABLE roles IS 'Role definitions with 5-level RBAC structure';
COMMENT ON TABLE bookmarks IS 'User-saved dashboard configurations and filters';
COMMENT ON TABLE favorites IS 'User-favorited accounts, customers, products, branches';
COMMENT ON TABLE notifications IS 'In-app notifications for users';
COMMENT ON TABLE audit_log IS 'Complete audit trail of user actions';
COMMENT ON TABLE user_sessions IS 'Active user sessions for authentication';

-- ============================================================================
-- GRANTS (Adjust based on your user setup)
-- ============================================================================

-- Grant appropriate permissions
-- Note: Adjust username based on your database configuration
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO nmb_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO nmb_app_user;

-- ============================================================================
-- SCHEMA VERSION
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_version (
    version_id SERIAL PRIMARY KEY,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial schema with 5-level RBAC, user management, bookmarks, favorites, and notifications');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
