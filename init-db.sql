-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS task_db;
USE task_db;

-- Create the 'tasks' table if it doesn't already exist
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL
);

