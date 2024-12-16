DROP DATABASE IF EXISTS wireless;

CREATE DATABASE IF NOT EXISTS wireless;

USE wireless;

CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Teams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE SimulationScenarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visibility VARCHAR(50) NOT NULL,
    frequency VARCHAR(50),
    type VARCHAR(50),
    map_center_lat DECIMAL(8,6),
    map_center_long DECIMAL(9,6),
    map_size INT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE GeoReferencedPoints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    latitude DECIMAL(8,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    simulation_scenario_id INT NOT NULL,
    FOREIGN KEY (simulation_scenario_id) REFERENCES SimulationScenarios(id) ON DELETE CASCADE
);

CREATE TABLE UserTeams (
    user_id INT NOT NULL,
    team_id INT NOT NULL,
    PRIMARY KEY (user_id, team_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES Teams(id) ON DELETE CASCADE
);
