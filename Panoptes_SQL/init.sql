-- Create Events table
CREATE TABLE IF NOT EXISTS Events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Create Locations table
CREATE TABLE IF NOT EXISTS Locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL
);

-- Create EventDetails table
CREATE TABLE IF NOT EXISTS EventDetails (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    location_id INT NOT NULL,
    event_date DATE,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);

-- Create Images table
CREATE TABLE IF NOT EXISTS Images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    processed_date DATETIME
);

-- Create EventImage Link table
CREATE TABLE IF NOT EXISTS EventImage (
    event_id INT NOT NULL,
    image_id INT NOT NULL,
    PRIMARY KEY (event_id, image_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (image_id) REFERENCES Images(image_id)
);
