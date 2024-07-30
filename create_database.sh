#!/bin/bash

# Config
DB_USER="myuser"
DB_PASSWORD="mypassword"
DB_HOST="localhost"
DB_NAME="mydatabase"

# Commands for creating the tables
SQL_COMMANDS="
CREATE TABLE IF NOT EXISTS authentifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    realname VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    x FLOAT NOT NULL DEFAULT 0.5,
    y FLOAT NOT NULL DEFAULT 65.0,
    z FLOAT NOT NULL DEFAULT 0.5,
    regdate BIGINT NOT NULL DEFAULT 0,
    regip VARCHAR(40) NOT NULL DEFAULT '0.0.0.0',
    email VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS webapi_session (
    username VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) NOT NULL,
    valid_until DATETIME NOT NULL,
    perm_level INT NOT NULL,
    PRIMARY KEY (username, api_key)
);

CREATE TABLE IF NOT EXISTS website_permissions (
    username VARCHAR(255) NOT NULL,
    perm_level INT NOT NULL,
    PRIMARY KEY (username)
);
"

# Run commands
echo "Creating tables for database ${DB_NAME}..."

mysql -u ${DB_USER} -p${DB_PASSWORD} -h ${DB_HOST} ${DB_NAME} -e "${SQL_COMMANDS}"

echo "Tables created."
