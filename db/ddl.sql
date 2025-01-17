-- 1) USERS
CREATE TABLE users (
    uid         VARCHAR(36) PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    cat         VARCHAR(50) NOT NULL,  -- e.g. 'USER' or 'ADMIN'
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    credit      DECIMAL(10,2) DEFAULT 0.00,
    is_active   BOOLEAN DEFAULT TRUE
);

-- 2) ITEMS
CREATE TABLE items (
    id          VARCHAR(36) PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    image       TEXT,               -- Storing image as a blob/bytea
    stock       INT NOT NULL CHECK (stock >= 0),
    price       INT NOT NULL CHECK (price >= 0),
    description TEXT
);

-- 3) TASKS
CREATE TABLE tasks (
    id                  VARCHAR(36) PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    created_by          VARCHAR(36) NOT NULL REFERENCES users(uid),
    reward              DECIMAL(10,2) DEFAULT 0.00 CHECK (reward >= 0),
    start_time          TIMESTAMP WITH TIME ZONE,
    deadline            TIMESTAMP WITH TIME ZONE,
    is_recurring        BOOLEAN,
    recurrence_interval INT,  -- e.g. 1 for daily, 7 for weekly, etc. Not recurring if NULL
    description         TEXT
);

-- 4) USERTASK (Association between User and Task)
CREATE TABLE usertasks (
    id                  VARCHAR(36) PRIMARY KEY,
    uid                 VARCHAR(36) NOT NULL REFERENCES users(uid),
    task                VARCHAR(36) NOT NULL REFERENCES tasks(id),
    start_time          TIMESTAMP WITH TIME ZONE,
    end_time            TIMESTAMP WITH TIME ZONE,
    status              VARCHAR(50) NOT NULL,  -- e.g. APPLIED, REJECTED, ONGOING, UNDER_REVIEW, COMPLETED
    admin_comment       TEXT
);

-- 5) TRANSACTIONS
CREATE TABLE transactions (
    id       VARCHAR(36) PRIMARY KEY,
    item     VARCHAR(36) NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    uid     VARCHAR(36) NOT NULL REFERENCES users(uid) ON DELETE CASCADE,
    quantity INT NOT NULL,
    status   VARCHAR(50) NOT NULL  -- e.g. 'PREORDER', 'AWAITING_CONF', 'CONFIRMED', 'CLAIMED', 'CANCELED'
);

-- 6) ITEMREQUEST
CREATE TABLE itemrequests (
    id            VARCHAR(36) PRIMARY KEY,
    requested_by  VARCHAR(36) NOT NULL REFERENCES users(uid) ON DELETE CASCADE,
    description   TEXT NOT NULL
);

-- 7) LOGS
CREATE TABLE logs (
    id          VARCHAR(36) PRIMARY KEY,
    cat         VARCHAR(50) NOT NULL,   -- e.g. 'USER', 'TRANSACTION', ...
    uid         VARCHAR(36),  -- quoting "user" if we keep that as column name
    timestamp   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);
