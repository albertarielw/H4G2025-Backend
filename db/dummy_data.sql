------------------------------------------------------------------------------
-- USERS
------------------------------------------------------------------------------
INSERT INTO users (uid, name, cat, email, password, credit)
VALUES 
('u0001', 'Alice', 'USER', 'alice@example.com', 'alicepass',  10.00),
('u0002', 'Bob',   'ADMIN', 'bob@example.com',   'bobpass',   100.00),
('u0003', 'Charlie', 'USER', 'charlie@example.com', 'charliepass',  25.50),
('u0004', 'Diana', 'USER', 'diana@example.com', 'dianapass',  5.00),
('u0005', 'Eve',   'USER', 'eve@example.com',   'evepass',    0.00);

------------------------------------------------------------------------------
-- ITEMS
------------------------------------------------------------------------------
INSERT INTO items (id, name, image, stock, price, description)
VALUES
('i0001', 'Laptop', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg',  5,   1200, 'This is an item.'),
('i0002', 'Phone', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg',  10,  800, 'This is an item.'),
('i0003', 'Monitor', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg',  3,   300, 'This is an item.'),
('i0004', 'Headset', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg',  20,  50, 'This is an item.'),
('i0005', 'Keyboard', 'https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg', 15,  90, 'This is an item.');

------------------------------------------------------------------------------
-- TASKS
------------------------------------------------------------------------------
INSERT INTO tasks (id, name, created_by, reward, deadline, user_limit, description, 
                   require_review, require_proof, is_recurring)
VALUES
('t0001', 'Write Blog Post', 'u0002', 10.00, '2025-12-31 23:59:59+00', 3, 'Write a post about new features', TRUE, TRUE, FALSE),
('t0002', 'Design Logo', 'u0002', 25.00, '2025-06-30 23:59:59+00', 2, 'Create a brand logo', TRUE, FALSE, FALSE),
('t0003', 'Translate Document', 'u0002', 15.00, '2025-05-15 23:59:59+00', 5, 'Translate the user manual', FALSE, FALSE, FALSE),
('t0004', 'Weekly Cleanup', 'u0002', 5.00, '2025-12-31 23:59:59+00', 10, 'Clean up shared folder', FALSE, FALSE, TRUE),
('t0005', 'Survey Feedback', 'u0002', 2.50, '2026-01-01 23:59:59+00', 100, 'Fill out a short survey', FALSE, FALSE, FALSE);

------------------------------------------------------------------------------
-- USERTASKS
------------------------------------------------------------------------------
INSERT INTO usertasks (uid, task, status, proof_of_completion)
VALUES
('u0001', 't0001', 'APPLIED', NULL),
('u0001', 't0002', 'REJECTED', NULL),
('u0003', 't0003', 'ONGOING', NULL),
('u0004', 't0004', 'COMPLETED', NULL),
('u0005', 't0005', 'APPLIED', NULL);

------------------------------------------------------------------------------
-- TRANSACTIONS
------------------------------------------------------------------------------
INSERT INTO transactions (id, item, uid, quantity, status)
VALUES
('tr0001', 'i0001', 'u0001', 1, 'CONFIRMED'),
('tr0002', 'i0003', 'u0001', 1, 'PREORDER'),
('tr0003', 'i0005', 'u0002', 2, 'AWAITING_CONF'),
('tr0004', 'i0002', 'u0003', 1, 'CLAIMED'),
('tr0005', 'i0002', 'u0004', 2, 'CANCELED');

------------------------------------------------------------------------------
-- ITEMREQUESTS
------------------------------------------------------------------------------
INSERT INTO itemrequests (id, requested_by, description)
VALUES
('ir0001', 'u0001', 'Requesting a stand for the monitor'),
('ir0002', 'u0003', 'Need extra phone chargers'),
('ir0003', 'u0004', 'Requesting gaming mouse in stock'),
('ir0004', 'u0005', 'More color variants of keyboards'),
('ir0005', 'u0005', 'Request for ergonomic chairs');

------------------------------------------------------------------------------
-- LOGS
------------------------------------------------------------------------------
INSERT INTO logs (id, cat, uid, timestamp, description)
VALUES
('lg0001', 'USER', 'u0001', '2025-01-01 10:00:00+00', 'User logged in'),
('lg0002', 'TRANSACTION', 'u0001', '2025-01-02 12:30:00+00', 'User purchased an item'),
('lg0003', 'USER', 'u0003', '2025-01-02 13:00:00+00', 'User changed password'),
('lg0004', 'USER', 'u0002', '2025-01-03 09:00:00+00', 'Admin updated user task'),
('lg0005', 'TRANSACTION', 'u0002', '2025-01-04 14:00:00+00', 'User refunded purchase');
