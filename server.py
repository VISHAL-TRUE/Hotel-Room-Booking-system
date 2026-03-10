from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- DATABASE CONNECTION ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="hotel_management"
)

cursor = db.cursor()

# ---------- ADD ROOM ----------
@app.route('/add_room', methods=['POST'])
def add_room():
    data = request.json
    room_no = data['room_no']
    room_type = data['room_type']

    cursor.execute(
        "SELECT type_id FROM room_type WHERE type_name=%s",
        (room_type,)
    )
    result = cursor.fetchone()

    if result is None:
        return jsonify({"error": "Room type not found"})

    type_id = result[0]

    # check if room exists
    cursor.execute(
        "SELECT * FROM room WHERE room_no=%s",
        (room_no,)
    )

    if cursor.fetchone():
        return jsonify({"error": "Room already exists"})

    cursor.execute(
        "INSERT INTO room(room_no,type_id) VALUES(%s,%s)",
        (room_no, type_id)
    )
    db.commit()

    return jsonify({"status": "Room Added Successfully"})


# ---------- CHECK AVAILABLE ROOMS ----------
@app.route('/available/<checkin>/<checkout>', methods=['GET'])
def available(checkin, checkout):

    query = """
    SELECT room_no FROM room
    WHERE room_no NOT IN(
        SELECT room_no FROM booking
        WHERE (checkin <= %s AND checkout >= %s)
    )
    """

    cursor.execute(query, (checkout, checkin))
    rooms = cursor.fetchall()

    return jsonify(rooms)


# ---------- BOOK ROOM ----------
@app.route('/book_room', methods=['POST'])
def book_room():

    data = request.json

    name = data['name']
    phone = data['phone']
    aadhar = data['aadhar']
    room_no = data['room_no']
    checkin = data['checkin']
    checkout = data['checkout']
    mode = data['mode']

    # insert customer
    cursor.execute(
        "INSERT INTO customer(name,phone,aadhar) VALUES(%s,%s,%s)",
        (name, phone, aadhar)
    )
    db.commit()

    customer_id = cursor.lastrowid

    # insert booking
    cursor.execute(
        "INSERT INTO booking(room_no,customer_id,checkin,checkout,mode) VALUES(%s,%s,%s,%s,%s)",
        (room_no, customer_id, checkin, checkout, mode)
    )
    db.commit()

    return jsonify({"status": "Booking Confirmed"})


# ---------- GET ROOMS ----------
@app.route('/get_rooms', methods=['GET'])
def get_rooms():

    cursor.execute("""
        SELECT r.room_no, rt.type_name, rt.price
        FROM room r
        JOIN room_type rt ON r.type_id = rt.type_id
    """)

    rooms = cursor.fetchall()

    return jsonify(rooms)


# ---------- GET BOOKINGS ----------
@app.route('/get_bookings', methods=['GET'])
def get_bookings():

    cursor.execute("""
        SELECT b.booking_id, c.name, b.room_no, b.checkin, b.checkout, b.mode
        FROM booking b
        JOIN customer c ON b.customer_id = c.customer_id
    """)

    bookings = cursor.fetchall()

    return jsonify(bookings)


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)