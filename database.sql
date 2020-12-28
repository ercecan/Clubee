/*
*   CREATE TABLE
*       USERS
*       CLUBS
*       CLUB ADMINS
*       CLUB MANAGERS
*       MEMBERS
*       ANNOUNCEMENTS
*       EVENTS
*       COMMENTS
*/


CREATE TABLE users (
user_id SERIAL PRIMARY KEY,
email VARCHAR UNIQUE,
name VARCHAR(30) NOT NULL, 
surname VARCHAR(30) NOT NULL, 
student_id CHAR(9) UNIQUE NOT NULL, 
department VARCHAR (150) NOT NULL, 
password_hash CHAR(64) NOT NULL
);


CREATE TABLE clubs (
club_id SERIAL PRIMARY KEY,
name VARCHAR(100) UNIQUE NOT NULL, 
description TEXT,
history TEXT,
student_count INTEGER DEFAULT 0,
source VARCHAR, 
mission TEXT,
vision TEXT,
image_url TEXT
);


CREATE TABLE club_admins (
admin_id SERIAL PRIMARY KEY,
nickname VARCHAR(50) UNIQUE NOT NULL, 
password_hash CHAR(64) NOT NULL
);


CREATE TABLE club_managers(
admin_id INTEGER NOT NULL,
club_id INTEGER NOT NULL,
PRIMARY KEY (admin_id, club_id),
FOREIGN KEY (admin_id) REFERENCES club_admins (admin_id)
ON DELETE CASCADE
ON UPDATE CASCADE,
FOREIGN KEY (club_id) REFERENCES clubs (club_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);


CREATE TABLE members (
user_id INTEGER NOT NULL,
club_id INTEGER NOT NULL,
PRIMARY KEY (user_id, club_id),
FOREIGN KEY (user_id) REFERENCES users (user_id) 
ON DELETE CASCADE
ON UPDATE CASCADE,
FOREIGN KEY (club_id) REFERENCES clubs (club_id) 
ON DELETE CASCADE
ON UPDATE CASCADE
);


CREATE TABLE announcements (
announcement_id SERIAL PRIMARY KEY,
club_id INTEGER NOT NULL REFERENCES clubs (club_id) 
ON DELETE CASCADE
ON UPDATE CASCADE,
header TEXT NOT NULL,
content TEXT NOT NULL,
image_url TEXT
);


CREATE TABLE events (
event_id SERIAL PRIMARY KEY,
club_id INTEGER NOT NULL REFERENCES clubs (club_id) 
ON DELETE CASCADE
ON UPDATE CASCADE,
header TEXT NOT NULL,
content TEXT NOT NULL,
date_ DATE,
iamge_url TEXT
);


CREATE TABLE comments (
comment_id SERIAL PRIMARY KEY,
event_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
content TEXT NOT NULL,
created_at TIMESTAMP NOT NULL,
FOREIGN KEY (event_id) REFERENCES events (event_id) 
ON DELETE CASCADE
ON UPDATE CASCADE,
FOREIGN KEY (user_id) REFERENCES users (user_id) 
ON DELETE CASCADE
ON UPDATE CASCADE
);