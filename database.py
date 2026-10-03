import psycopg2


def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="ev_charging",
        user="postgres",
        password="vandhana",
        port="5432"
    )


def save_vehicle(vehicle, status):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO vehicles
        (vehicle_id, urgency, departure, duration, status)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            vehicle["id"],
            vehicle["urgency"],
            vehicle["departure"],
            vehicle["duration"],
            status
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_vehicles():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            vehicle_id,
            urgency,
            departure,
            duration,
            status
        FROM vehicles
        ORDER BY id DESC
    """)

    vehicles = cursor.fetchall()

    cursor.close()
    connection.close()

    return vehicles