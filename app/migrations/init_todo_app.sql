BEGIN;

-- =========================
-- USERS
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) UNIQUE,
    password TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

-- =========================
-- GROUPS
-- =========================
CREATE TABLE IF NOT EXISTS groups (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================
-- GROUP MEMBERS
-- =========================
CREATE TABLE IF NOT EXISTS group_members (
    group_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_group_members
        PRIMARY KEY (group_id, user_id),

    CONSTRAINT fk_group_members_group
        FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_group_members_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =========================
-- TASKS
-- =========================
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    due_date TIMESTAMPTZ,
    status VARCHAR(50) NOT NULL DEFAULT 'todo',
    attachment JSON[] NULL DEFAULT '{}'::JSON[],

    assigned_to_id UUID,
    group_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_tasks_assigned_user
        FOREIGN KEY (assigned_to_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_tasks_group
        FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE SET NULL
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to
    ON tasks(assigned_to_id);

CREATE INDEX IF NOT EXISTS idx_tasks_group
    ON tasks(group_id);

CREATE INDEX IF NOT EXISTS idx_group_members_user
    ON group_members(user_id);

COMMIT;
