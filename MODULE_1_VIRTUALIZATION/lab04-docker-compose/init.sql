CREATE TABLE asdn_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

INSERT INTO asdn_users (username) VALUES ('admin'), ('student');
