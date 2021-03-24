
SELECT Flight_number, amount
from leg_instance NATURAL JOIN fare
WHERE amount in (
SELECT min(amount)
FROM leg_instance NATURAL JOIN fare
WHERE leg_instance.Leg_date = '2018-08-05' AND leg_instance.Departure_airport_code = 'LAX');

SELECT Flight_number, Seat_number
FROM seat_reservation;

SELECT *
FROM (
SELECT Flight_number, max(Leg_number) as max_leg
FROM flight_leg NATURAL JOIN flight
WHERE airline = 'American'
GROUP BY Flight_number) as max_leg
WHERE max_leg = 1;

SELECT max(airplane_id) FROM airplane;

INSERT INTO airplane(Airplane_id, Total_number_of_seats, Airplane_type)
VALUES({max_id}+1, {seats}, '{type}');

SELECT *
FROM airplane;

UPDATE fare
SET amount = amount * 1.01
WHERE amount < 200;

SELECT Flight_number, amount
from fare;

SELECT *
FROM seat_reservation;

DELETE
FROM seat_reservation
WHERE Flight_number=%s AND Customer_name=%s;

SELECT *
from leg_instance NATURAL JOIN fare;

SELECT Flight_number, amount
FROM leg_instance NATURAL JOIN fare 
WHERE amount in ( 
SELECT min(amount) 
FROM leg_instance NATURAL JOIN fare 
WHERE leg_instance.Leg_date = '2018-08-05' AND leg_instance.Departure_airport_code = 'ONT' AND leg_instance.Arrival_airport_code = 'SMF')
GROUP BY Flight_number;

SELECT min(amount) 
FROM leg_instance NATURAL JOIN fare 
WHERE leg_instance.Leg_date = '2018-08-05' AND leg_instance.Departure_airport_code = 'ONT' AND leg_instance.Arrival_airport_code = 'SMF';

