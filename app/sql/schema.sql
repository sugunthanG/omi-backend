-- Enable UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- ROLES
-- =========================
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL, -- Maker, Executor, User
    description TEXT
);

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    
    role_id UUID REFERENCES roles(id) ON DELETE SET NULL,

    is_active BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- PERMISSIONS
-- =========================
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- =========================
-- USER PERMISSIONS (M:N)
-- =========================
CREATE TABLE user_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,

    UNIQUE(user_id, permission_id)
);

-- =========================
-- APPROVAL SYSTEM
-- =========================
CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    entity_type VARCHAR(50) NOT NULL, -- e.g. "user"
    entity_id UUID NOT NULL,

    requested_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),

    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected

    step INT DEFAULT 1, -- 1 = Executor1, 2 = Executor2

    comments TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- AUDIT LOGS
-- =========================
CREATE TABLE logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID REFERENCES users(id),

    action VARCHAR(100), -- CREATE_USER, APPROVE_USER, LOGIN, TRADE_EXECUTE
    entity_type VARCHAR(50),
    entity_id UUID,

    metadata JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- INDEXES (IMPORTANT)
-- =========================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role_id);

CREATE INDEX idx_approvals_entity ON approvals(entity_id);
CREATE INDEX idx_approvals_status ON approvals(status);

CREATE INDEX idx_logs_user ON logs(user_id);
CREATE INDEX idx_logs_action ON logs(action);