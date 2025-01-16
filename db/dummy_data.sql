------------------------------------------------------------------------------
-- USERS
------------------------------------------------------------------------------
INSERT INTO users (uid, name, cat, email, password, credit, is_active)
VALUES 
('u0001', 'Alice',   'USER',  'alice@example.com',   'alicepass',   10.00, TRUE),
('u0002', 'Bob',     'ADMIN', 'bob@example.com',     'bobpass',    100.00, TRUE),
('u0003', 'Charlie', 'USER',  'charlie@example.com', 'charliepass', 25.50, TRUE),
('u0004', 'Diana',   'USER',  'diana@example.com',   'dianapass',    5.00, TRUE),
('u0005', 'Eve',     'USER',  'eve@example.com',     'evepass',      0.00, TRUE);

------------------------------------------------------------------------------
-- ITEMS
------------------------------------------------------------------------------
INSERT INTO items (id, name, image, stock, price, description)
VALUES
('i0001', 'Laptop',   'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg',  5,  1200, 'High-end laptop'),
('i0002', 'Phone',    'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg', 10,   800, 'Latest smartphone'),
('i0003', 'Monitor',  'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg',  3,   300, '4K monitor'),
('i0004', 'Headset',  'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg', 20,    50, 'Noise-cancelling headset'),
('i0005', 'Keyboard', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg', 15,    90, 'Mechanical keyboard');

------------------------------------------------------------------------------
-- TASKS
------------------------------------------------------------------------------
INSERT INTO tasks (
    id, 
    name, 
    created_by, 
    reward, 
    start_time, 
    end_time, 
    recurrence_interval, 
    description, 
    require_review, 
    require_proof
)
VALUES
('t0001', 'Write Blog Post',   'u0002', 10.00, '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00',  3, 'Write a post about new features', TRUE,  TRUE),
('t0002', 'Design Logo',       'u0002', 25.00, '2025-06-30 23:59:59+00', '2025-07-01 23:59:59+00',  2, 'Create a brand logo',             TRUE,  FALSE),
('t0003', 'Translate Document','u0002', 15.00, '2025-05-15 23:59:59+00', '2025-05-16 23:59:59+00',  5, 'Translate the user manual',       FALSE, FALSE),
('t0004', 'Weekly Cleanup',    'u0002',  5.00, '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00', 10, 'Clean up shared folder',          FALSE, FALSE),
('t0005', 'Survey Feedback',   'u0002',  2.50, '2026-01-01 23:59:59+00', '2026-01-02 23:59:59+00',100, 'Fill out a short survey',         FALSE, FALSE);

------------------------------------------------------------------------------
-- TASK_POSTINGS
-- These represent "open calls" or "slots" for a task, where multiple users can apply.
------------------------------------------------------------------------------
INSERT INTO task_postings (
    id, 
    task, 
    user_limit, 
    is_open
)
VALUES
('tp0001', 't0001',  5, TRUE),
('tp0002', 't0002',  3, TRUE),
('tp0003', 't0003',  0, TRUE),   -- 0 might mean "unlimited" or "no limit" depending on your logic
('tp0004', 't0004', 10, TRUE),
('tp0005', 't0005',  2, FALSE);  -- This posting is currently closed

------------------------------------------------------------------------------
-- TASK_APPLICATIONS
-- Users apply to a posting; admin can APPROVE or REJECT, or it can remain PENDING.
------------------------------------------------------------------------------
INSERT INTO task_applications (
    id, 
    posting, 
    applicant, 
    status, 
    comment
)
VALUES
('ta0001', 'tp0001', 'u0001', 'PENDING',  'Eager to write the blog post'),
('ta0002', 'tp0001', 'u0003', 'APPROVED', 'Good writer, can start right away'),
('ta0003', 'tp0002', 'u0001', 'REJECTED', 'Needs more design experience'),
('ta0004', 'tp0004', 'u0004', 'PENDING',  'Can help with weekly cleanup'),
('ta0005', 'tp0005', 'u0005', 'APPROVED', 'Survey form fill completed');

------------------------------------------------------------------------------
-- TASK_REQUESTS
-- Users create new task requests that can be reviewed/approved/rejected by an admin.
------------------------------------------------------------------------------
INSERT INTO task_requests (
    id, 
    created_by, 
    name, 
    description, 
    reward, 
    status, 
    start_time, 
    end_time, 
    recurrence_interval
)
VALUES
('trq0001', 'u0001', 'New Blog Post',       'Write a new article about AI',             5.00, 'PENDING',   '2025-02-01 08:00:00+00', '2025-02-05 17:00:00+00', NULL),
('trq0002', 'u0003', 'Design Infographic',  'Create a marketing infographic',           10.00, 'APPROVED',  '2025-03-01 09:00:00+00', '2025-03-02 09:00:00+00', 7),
('trq0003', 'u0005', 'Code Review',         'Review the new codebase',                  15.00, 'REJECTED',  '2025-04-05 10:00:00+00', '2025-04-06 10:00:00+00', 1),
('trq0004', 'u0004', 'Photography Session', 'Take photos for marketing campaign',        8.00,  'PENDING',   '2025-05-10 09:00:00+00', '2025-05-11 18:00:00+00', NULL),
('trq0005', 'u0002', 'Security Audit',      'Review system security configurations',     20.00, 'APPROVED',  '2025-06-01 10:00:00+00', '2025-06-02 17:00:00+00', 7);

------------------------------------------------------------------------------
-- USERTASKS
-- Association between an individual user and a specific task instance
------------------------------------------------------------------------------
INSERT INTO usertasks (
    id, 
    uid, 
    task, 
    start_time, 
    end_time, 
    status, 
    proof_of_completion, 
    admin_comment
)
VALUES
('ut0001', 'u0001', 't0001', '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00', 'ONGOING', NULL, ''),
('ut0002', 'u0001', 't0002', '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00', 'ONGOING', NULL, ''),
('ut0003', 'u0003', 't0003', '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00', 'ONGOING', NULL, ''),
('ut0004', 'u0004', 't0004', '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00', 'ONGOING', NULL, ''),
('ut0005', 'u0005', 't0005', '2025-12-31 23:59:59+00', '2026-01-01 23:59:59+00', 'ONGOING', NULL, '');

------------------------------------------------------------------------------
-- TRANSACTIONS
------------------------------------------------------------------------------
INSERT INTO transactions (
    id, 
    item, 
    uid, 
    quantity, 
    status
)
VALUES
('tr0001', 'i0001', 'u0001', 1, 'CONFIRMED'),
('tr0002', 'i0003', 'u0001', 1, 'PREORDER'),
('tr0003', 'i0005', 'u0002', 2, 'AWAITING_CONF'),
('tr0004', 'i0002', 'u0003', 1, 'CLAIMED'),
('tr0005', 'i0002', 'u0004', 2, 'CANCELED');

------------------------------------------------------------------------------
-- ITEMREQUESTS
------------------------------------------------------------------------------
INSERT INTO itemrequests (
    id, 
    requested_by, 
    description
)
VALUES
('ir0001', 'u0001', 'Requesting a stand for the monitor'),
('ir0002', 'u0003', 'Need extra phone chargers'),
('ir0003', 'u0004', 'Requesting a gaming mouse in stock'),
('ir0004', 'u0005', 'More color variants of keyboards'),
('ir0005', 'u0005', 'Request for ergonomic chairs');

------------------------------------------------------------------------------
-- LOGS
------------------------------------------------------------------------------
INSERT INTO logs (
    id, 
    cat, 
    uid, 
    timestamp, 
    description
)
VALUES
('lg0001', 'USER',        'u0001', '2025-01-01 10:00:00+00', 'User logged in'),
('lg0002', 'TRANSACTION', 'u0001', '2025-01-02 12:30:00+00', 'User purchased an item'),
('lg0003', 'USER',        'u0003', '2025-01-02 13:00:00+00', 'User changed password'),
('lg0004', 'USER',        'u0002', '2025-01-03 09:00:00+00', 'Admin updated user task'),
('lg0005', 'TRANSACTION', 'u0002', '2025-01-04 14:00:00+00', 'User refunded purchase');
