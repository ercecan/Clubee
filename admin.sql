/*
*
*   INSERT INTO ADMINS
*
*/

INSERT INTO club_admins (nickname,password_hash) 
VALUES ('ituacm','$pbkdf2-sha256$29000$xfgfY4wR4vzfO6e0dq51Tg$5NMULXhDk3ZALE1Stem6AZsdgkEqvPL91G3kBYWFhd4');

INSERT INTO club_admins (nickname,password_hash) 
VALUES ('itubc','$pbkdf2-sha256$29000$IeTc25uTMua89x5DqHWuNQ$TKduwlfmdcreV0SEQOoulXNyKi2bQsSo.Fqsf3eBAQ0');

INSERT INTO club_admins (nickname,password_hash) 
VALUES ('ituieee','$pbkdf2-sha256$29000$GmOs1frfm5OyFuK8dy5l7A$nriRyrsCZbWQ1AcFG0jijno15CR8cRl4LDHTbZ6egjw');

INSERT INTO club_admins (nickname,password_hash) 
VALUES ('ituds','$pbkdf2-sha256$29000$yJmTkrJ2Tkmp1ZqTEqJ0Lg$7Gx5ENNbOH6EZEWrdyGrMxUDq9H6VlU8TomrTMDYBto');

INSERT INTO club_admins (nickname,password_hash) 
VALUES ('iturob','$pbkdf2-sha256$29000$J8RY670X4lyLMcZ4T.k9Bw$iO0lm84v0JQNMTs4oGy/6OxGsrEfaA0O.5eyLUpvyt0');

INSERT INTO club_managers (admin_id, club_id)
VALUES (1,1);

INSERT INTO club_managers (admin_id, club_id)
VALUES (2,2);

INSERT INTO club_managers (admin_id, club_id)
VALUES (3,3);

INSERT INTO club_managers (admin_id, club_id)
VALUES (4,4);

INSERT INTO club_managers (admin_id, club_id)
VALUES (5,5);