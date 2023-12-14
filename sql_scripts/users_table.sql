CREATE DATABASE GAME_SERVER;

USE GAME_SERVER;
CREATE TABLE users (
  login VARCHAR(50) unique not null,
  password VARCHAR(50) not null,
  name varchar(50),
  date_of_creation timestamp,
  score int
);

CREATE USER 'game_user'@'localhost' IDENTIFIED BY '';
GRANT SELECT, INSERT, UPDATE, DELETE ON GAME_SERVER.* TO 'game_user'@'localhost';
FLUSH PRIVILEGES;