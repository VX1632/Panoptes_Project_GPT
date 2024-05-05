-- Create Events table
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    all_day_event BOOLEAN DEFAULT TRUE,
    description VARCHAR(255),
    location VARCHAR(255)
);


-- Create Locations table (if separate location details are needed)
CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL
);

-- If Locations are directly linked to events and not reused, consider embedding location in the Events table
