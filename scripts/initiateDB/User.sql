
INSERT INTO users(
	id, username, email, password, disabled)
	VALUES (1, 'superadmin', 'superadmin@admin.com', 'fakehashed123', False),
	(2, 'admin', 'admin@admin.com', 'fakehashed123', False),
	(3, 'test_user', 'test@test.com', 'fakehashed123', False);

INSERT INTO roles(
	id, name)
	VALUES (1, 'superadmin'), (2, 'admin'), (3, 'user');


INSERT INTO permissions(
	id, name, details, "parentPermissionID")
	VALUES 
	(1, 'user', '{"permission_details": "CRUD collection of User"}', NULL),
	(2, 'user:create', '{"permission_details": "create operation of User"}', 1),
	(3, 'user:read', '{"permission_details": "read operation of User"}', 1),
	(4, 'user:update', '{"permission_details": "update operation of User"}', 1),
	(5, 'user:delete', '{"permission_details": "delete operation of User"}', 1),

	(6, 'movie', '{"permission_details": "CRUD collection of Movie"}', NULL),
	(7, 'movie:create', '{"permission_details": "create operation of Movie"}', 6),
	(8, 'movie:read', '{"permission_details": "read operation of Movie"}', 6),
	(9, 'movie:update', '{"permission_details": "update operation of Movie"}', 6),
	(10, 'movie:delete', '{"permission_details": "delete operation of Movie"}', 6),

	(11, 'series', '{"permission_details": "CRUD collection of Series"}', NULL),
	(12, 'series:create', '{"permission_details": "create operation of Series"}', 11),
	(13, 'series:read', '{"permission_details": "read operation of Series"}', 11),
	(14, 'series:update', '{"permission_details": "update operation of Series"}', 11),
	(15, 'series:delete', '{"permission_details": "delete operation of Series"}', 11),

	(16, 'anime', '{"permission_details": "CRUD collection of Anime"}', NULL),
	(17, 'anime:create', '{"permission_details": "create operation of Anime"}', 16),
	(18, 'anime:read', '{"permission_details": "read operation of Anime"}', 16),
	(19, 'anime:update', '{"permission_details": "update operation of Anime"}', 16),
	(20, 'anime:delete', '{"permission_details": "delete operation of Anime"}', 16);

INSERT INTO role_permissions(
	role_id, permission_id)
	VALUES 
	(1, 1), (1, 2),	(1, 3),	(1, 4),	(1, 5),	(1, 6),	(1, 7),	(1, 8),	(1, 9),	(1, 10), 
	(1, 11), (1, 12), (1, 13), (1, 14),	(1, 15), (1, 16), (1, 17), (1, 18),	(1, 19), (1, 20),

	(2, 6),	(2, 7),	(2, 8),	(2, 9),	(2, 10), 
	(2, 11), (2, 12), (2, 13), (2, 14),	(2, 15), (2, 16), (2, 17), (2, 18),	(2, 19), (2, 20),

	(3, 6),	(3, 8), 
	(3, 11), (3, 13), (3, 16), (3, 18);

INSERT INTO user_roles(
	user_id, role_id)
	VALUES (1, 1), (2, 2), (3, 3);

INSERT INTO user_permissions(
	user_id, permission_id)
	VALUES (2, 1), (2, 3);