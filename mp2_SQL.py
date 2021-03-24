import pymysql


# 1. Query: Find the cheapest flight given airports and a date.
# Please enter the airport code for the departure airport:
# Please enter the airport code for the destination airport:
# What is the date of the flight in yyyy-mm-dd?
# Result: The cheapest flight is $FlightNumber, and the cost is $FareAmount.
def findCheapest():
    dep_code = input("Please enter the airport code for the departure airport:")
    dest_code = input("Please enter the airport code for the destination airport:")
    date = input("What is the date of the flight in yyyy-mm-dd?")

    cur.execute(f"SELECT Flight_number, amount FROM leg_instance NATURAL JOIN fare WHERE amount in ( SELECT min(amount) FROM leg_instance NATURAL JOIN fare WHERE leg_instance.Leg_date = '{date}' AND leg_instance.Departure_airport_code = '{dep_code}' AND leg_instance.Arrival_airport_code = '{dest_code}') GROUP BY Flight_number")

    for row in cur.fetchall():
        print(f"The cheapest flight is {row[0]}, and the cost is ${row[1]}.")



# 2. Query: Find the flight and seat information for a customer.
# Please enter the customer’s name:
# Result: The flight number is $FlightNumber, and the seat number is $SeatNumber.
def seatInfo():
    customer = input("Please enter the customer’s name:")
    cur.execute(f"SELECT Flight_number, Seat_number FROM seat_reservation WHERE Customer_name = '{customer}'")

    for row in cur.fetchall():
        print(f"The flight number is {row[0]}, and the seat number is {row[1]}.")

# 3. Query: Find all non-stop flights for an airline.
# What is the name of the airline?
# Result: The non-stop flights are: $FlightNumber1, $FlightNumber2,
# $FlightNumber3...
def nonStop():
    airline = input("What is the name of the airline?")
    cur.execute(f"SELECT * FROM (SELECT Flight_number, max(Leg_number) as max_leg FROM flight_leg NATURAL JOIN flight WHERE airline = '{airline}' GROUP BY Flight_number) as max_leg WHERE max_leg = 1")
    
    print("The non-stop flights are:")
    for row in cur.fetchall():
        print(row[0])



# 4. Task: Add a new airplane.
# Please enter the total number of seats:
# Please enter the airplane type:
# Result: The new airplane has been added with id: $AirplaneID
def addPlane():
    cur.execute("SELECT max(airplane_id) FROM airplane")
    max_id = int(cur.fetchone()[0])
    seats = int(input("Please enter the total number of seats:"))
    air_type = input("Please enter the airplane type:")

    cur.execute(f"INSERT INTO airplane(Airplane_id, Total_number_of_seats, Airplane_type) VALUES({max_id+1}, {seats}, '{air_type}')")
    db.commit() #use commit to save the changes you made to the database

    print(f"The new airplane has been added with id: {max_id+1}")

# 5. Increase low-cost fares(≤ 200) by a factor.
# Please enter a factor (e.g. 0.2 will increase all fares by 20%):
# Result: $NumAffected fares are affected. (e.g. “3 fares are affected”)
def incFares():
    cur.execute("SELECT Flight_number, amount FROM fare")
    before = cur.fetchall()

    factor = input("Please enter a factor (e.g. 0.2 will increase all fares by 20%):")
    if float(factor) < 1:
        cur.execute(f"UPDATE fare SET amount = amount * {float(factor)+1} WHERE amount <= 200")
    else:
        cur.execute(f"UPDATE fare SET amount = amount * {float(factor)} WHERE amount <= 200")
    cur.execute("SELECT Flight_number, amount FROM fare")
    after = cur.fetchall()

    affected = 0
    for row in before:
        if row not in after:
            affected += 1
    
    print(f"{affected} fare(s) is/are affected.")
    db.commit() #use commit to save the changes you made to the database


# 6. Remove a seat reservation.
# Please enter the flight number:
# Please enter the customer name:
# Result: Seat $SeatNumber is released.
def removeReserve():
    flight_num = input("Please enter the flight number:")
    customer_name = input("Please enter the customer name:")

    cur.execute(f"SELECT Seat_number FROM seat_reservation WHERE Flight_number='{flight_num}' AND Customer_name='{customer_name}'")
    seat = cur.fetchone()[0]

    cur.execute(f"DELETE FROM seat_reservation WHERE Flight_number='{flight_num}' AND Customer_name='{customer_name}'")

    print(f"Seat {seat} is released")
    db.commit() #use commit to save the changes you made to the database


if __name__ == '__main__':
    db = pymysql.connect(host='127.0.0.1',
    user='mp2',
    passwd='eecs116',
    db= 'flights')
    cur = db.cursor()

    print("A. Find the cheapest flight given airports and a date.")
    print("B. Find the flight and seat information for a customer.")
    print("C. Find all non-stop flights for an airline.")
    print("D. Add a new airplane.")
    print("E. Increase low-cost fares(≤ 200) by a factor.")
    print("F. Remove a seat reservation.")
    print("Q. Quit program.")
    choice = input("Enter the letter for a query/task to execute or 'q' to quit:")
    while choice.lower() != 'q':
        if choice.lower() == 'a':
            findCheapest()
        elif choice.lower() == 'b':
            seatInfo()
        elif choice.lower() == 'c':
            nonStop()
        elif choice.lower() == 'd':
            addPlane()
        elif choice.lower() == 'e':
            incFares()
        elif choice.lower() == 'f':
            removeReserve()
        else:
            print("Unknown command")
        choice = input("Enter the letter for another query/task to execute or 'q' to quit:")
        
    print("Closing program...")
    db.close()
