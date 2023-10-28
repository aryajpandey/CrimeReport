-- Location Table
CREATE TABLE Location (
    Location_ID INT PRIMARY KEY,
    State VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    StreetAddress VARCHAR(255),
    ZipCode VARCHAR(10),
    Precinct_ID INT
);

-- Precinct Table
CREATE TABLE Precinct (
    Precinct_ID INT PRIMARY KEY,
    On_duty BOOLEAN NOT NULL,
    Precinct_email VARCHAR(255) NOT NULL,
    Precinct_phonenum VARCHAR(15) NOT NULL
);

-- Crime_details Table
CREATE TABLE Crime_details (
    Crime_ID INT PRIMARY KEY,
    Crime_description VARCHAR(255) NOT NULL,
    Violent BOOLEAN NOT NULL,
    Time TIME NOT NULL,
    Date DATE NOT NULL,
    Location_ID INT,
    addition_info TEXT,
    FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID)
);

-- Suspect_details Table
CREATE TABLE Suspect_details (
    Crime_ID INT,
    At_large BOOLEAN NOT NULL,
    PhysicalDescription TEXT,
    PRIMARY KEY (Crime_ID),
    FOREIGN KEY (Crime_ID) REFERENCES Crime_details(Crime_ID)
);

-- MissingPersons Table
CREATE TABLE MissingPersons (
    Visual_description TEXT NOT NULL,
    Location_ID INT,
    Age INT NOT NULL,
    Date DATE NOT NULL,
    Guardian_phonenum VARCHAR(15) NOT NULL,
    addition_info TEXT,
    FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID)
);
