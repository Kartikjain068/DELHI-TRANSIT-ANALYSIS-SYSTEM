#unit testing
import psycopg2

DB_NAME = "your_database_name"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"


def get_connection():
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def fetch_data(table_name):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = f"SELECT * FROM {table_name};"
        cur.execute(query)

        rows = cur.fetchall()

        print(f"\n---- DATA FROM TABLE: {table_name} ----")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def main():
    table_options = {
        "1": "metro_station",
        "2": "bus_station",
        "3": "routes",
        "4": "bus_routes",
        "5": "coordinates",
        "6": "station_details"
    }

    while True:
        print("\n===== DELHI TRANSIT DATABASE MENU =====")
        print("1. View metro_station")
        print("2. View bus_station")
        print("3. View routes")
        print("4. View bus_routes")
        print("5. View coordinates")
        print("6. View station_details")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "7":
            print("Exiting... Goodbye!")
            break

        table_name = table_options.get(choice)

        if table_name:
            fetch_data(table_name)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
