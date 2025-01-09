CREATE DATABASE IF NOT EXISTS wireless;

USE wireless;

CREATE TABLE IF NOT EXISTS Teams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    team_id INT,
    CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES Teams(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Scenarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visibility VARCHAR(50) NOT NULL,
    frequency VARCHAR(50),
    type VARCHAR(50),
    map_center_lat DECIMAL(8,6),
    map_center_long DECIMAL(9,6),
    map_size INT,
    user_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS GeoPoints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    latitude DECIMAL(8,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    scenario_id INT NOT NULL,
    CONSTRAINT fk_scenario FOREIGN KEY (scenario_id) REFERENCES Scenarios(id) ON DELETE CASCADE
);
