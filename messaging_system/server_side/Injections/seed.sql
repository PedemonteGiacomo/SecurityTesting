DROP DATABASE IF EXISTS fstt23;
CREATE DATABASE fstt23;
CREATE TABLE fstt23.users (first_name text, last_name text, username text, password text);
INSERT INTO fstt23.users VALUES ('Arthur', 'Dent', 'arthur', 'Bathrobe'),
                                ('Ford', 'Prefect', 'ford', 'dontpanic'),
                                ('Trisha', 'McMillan', 'trillian', 'random');
