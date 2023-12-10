INSERT INTO Location (Location_ID, State, City, StreetAddress, ZipCode, Precinct_ID) VALUES
(1, 'New York', 'New York City', '123 Broadway', '10001', 1),
(2, 'California', 'Los Angeles', '456 Hollywood Blvd', '90028', 2);

INSERT INTO Precinct (Precinct_ID, On_duty, Precinct_email, Precinct_phonenum) VALUES
(1, TRUE, 'precinct1@police.nyc', '555-0101'),
(2, FALSE, 'precinct2@police.la', '555-0202');

INSERT INTO Crime_details (Crime_ID, Crime_description, Violent, Time, Date, Location_ID, addition_info) VALUES
(101, 'Robbery', TRUE, '15:30:00', '2023-12-01', 1, 'Additional details here'),
(102, 'Vandalism', FALSE, '09:00:00', '2023-12-02', 2, 'Additional details here');

INSERT INTO Suspect_details (Crime_ID, At_large, PhysicalDescription) VALUES
(101, TRUE, 'Height 6ft, wearing a black hoodie'),
(102, FALSE, 'Height 5ft 5in, wearing a red cap');

INSERT INTO MissingPersons (Visual_description, Location_ID, Age, Date, Guardian_phonenum, addition_info) VALUES
('Height 5ft 2in, long brown hair', 1, 31, '2023-12-03', '555-0303', 'Last seen near Central Park'),
('Height 5ft 9in, short blonde hair', 2, 22, '2023-12-04', '555-0404', 'Last seen in Hollywood');

