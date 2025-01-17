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
('i0002', 'Phone',    'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg',  10,   800, 'Latest smartphone'),
('i0003', 'Monitor',  'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg',  3,   300, '4K monitor'),
('i0004', 'Headset',  'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg', 20,    50, 'Noise-cancelling headset'),
('i0005', 'Keyboard', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664.jpg', 15,    90, 'Mechanical keyboard');

------------------------------------------------------------------------------
-- TASKS
------------------------------------------------------------------------------
INSERT INTO tasks (id, name, created_by, reward, start_time, deadline, is_recurring, recurrence_interval, description)
VALUES
('t0001', 'Write Blog Post',   'u0002', 10.00, '2025-01-01 10:00:00+00', '2025-01-10 10:00:00+00', FALSE, NULL, 'Write a blog post about features'),
('t0002', 'Design Logo',       'u0002', 25.00, '2025-02-01 09:00:00+00', '2025-02-15 09:00:00+00', FALSE, NULL, 'Design a new logo'),
('t0003', 'Translate Document','u0003', 15.00, '2025-03-01 12:00:00+00', '2025-03-05 12:00:00+00', TRUE, 7, 'Translate documents weekly'),
('t0004', 'Weekly Cleanup',    'u0004',  5.00, '2025-01-07 14:00:00+00', '2025-01-07 15:00:00+00', TRUE, 7, 'Cleanup shared workspace'),
('t0005', 'Survey Feedback',   'u0005',  2.50, '2025-01-15 08:00:00+00', '2025-01-15 18:00:00+00', FALSE, NULL, 'Provide feedback on survey');

------------------------------------------------------------------------------
-- USERTASKS
------------------------------------------------------------------------------
INSERT INTO usertasks (id, uid, task, start_time, end_time, status, admin_comment)
VALUES
('ut0001', 'u0001', 't0001', '2025-01-01 11:00:00+00', '2025-01-10 11:00:00+00', 'ONGOING', 'Pending progress review'),
('ut0002', 'u0002', 't0002', '2025-02-01 10:00:00+00', '2025-02-15 10:00:00+00', 'UNDER_REVIEW', 'Final adjustments required'),
('ut0003', 'u0003', 't0003', '2025-03-01 13:00:00+00', '2025-03-05 13:00:00+00', 'COMPLETED', 'Task completed successfully'),
('ut0004', 'u0004', 't0004', '2025-01-07 15:00:00+00', '2025-01-07 16:00:00+00', 'APPLIED', 'Initial application under review'),
('ut0005', 'u0005', 't0005', '2025-01-15 09:00:00+00', '2025-01-15 19:00:00+00', 'COMPLETED', 'Feedback received');

------------------------------------------------------------------------------
-- TRANSACTIONS
------------------------------------------------------------------------------
INSERT INTO transactions (id, item, uid, quantity, status)
VALUES
('tr0001', 'i0001', 'u0001', 1, 'CONFIRMED'),
('tr0002', 'i0003', 'u0003', 2, 'PREORDER'),
('tr0003', 'i0005', 'u0002', 1, 'AWAITING_CONF'),
('tr0004', 'i0002', 'u0004', 1, 'CLAIMED'),
('tr0005', 'i0004', 'u0005', 1, 'CANCELED');

------------------------------------------------------------------------------
-- ITEMREQUESTS
------------------------------------------------------------------------------
INSERT INTO itemrequests (id, requested_by, description)
VALUES
('ir0001', 'u0001', 'Requesting a stand for the laptop'),
('ir0002', 'u0002', 'Request for ergonomic chairs'),
('ir0003', 'u0003', 'Requesting spare monitor cables'),
('ir0004', 'u0004', 'Need additional phone cases'),
('ir0005', 'u0005', 'Request for wireless keyboards');

------------------------------------------------------------------------------
-- LOGS
------------------------------------------------------------------------------
INSERT INTO logs (id, cat, uid, timestamp, description)
VALUES
('lg0001', 'USER', 'u0001', '2025-01-01 10:00:00+00', 'User logged in'),
('lg0002', 'TRANSACTION', 'u0001', '2025-01-02 10:30:00+00', 'User purchased an item'),
('lg0003', 'USER', 'u0003', '2025-01-03 11:00:00+00', 'Password change request'),
('lg0004', 'USERTASK', 'u0002', '2025-01-04 14:00:00+00', 'Updated user task status'),
('lg0005', 'TRANSACTION', 'u0005', '2025-01-05 16:00:00+00', 'Refund request processed');
