CREATE DATABASE hotel_management;
USE hotel_management;

-- Room Types
CREATE TABLE room_type (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(20),
    price INT
);

INSERT INTO room_type(type_name,price) VALUES
('Single',1000),
('Double',2000),
('Deluxe',3500),
('Suite',7000);

-- Rooms
CREATE TABLE room (
    room_no INT PRIMARY KEY,
    type_id INT,
    FOREIGN KEY (type_id) REFERENCES room_type(type_id)
);

-- Customers
CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(15),
    aadhar VARCHAR(20)
);

-- Bookings
CREATE TABLE booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    room_no INT,
    customer_id INT,
    checkin DATE,
    checkout DATE,
    mode VARCHAR(10),
    FOREIGN KEY (room_no) REFERENCES room(room_no),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);