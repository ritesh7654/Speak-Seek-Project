CREATE DATABASE IF NOT EXISTS speak_seek_db;
USE speak_seek_db;

-- Table for Lost & Found
CREATE TABLE IF NOT EXISTS lost_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(100),
    contact_info VARCHAR(100),
    image_url VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Reported',
    date_reported DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for Student Voice (Complaints)
CREATE TABLE IF NOT EXISTS student_voice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    is_anonymous BOOLEAN DEFAULT FALSE,
    student_contact VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Pending',
    date_submitted DATETIME DEFAULT CURRENT_TIMESTAMP
);