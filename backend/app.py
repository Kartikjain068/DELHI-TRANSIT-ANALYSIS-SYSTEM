from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection
import os

app = Flask(__name__)
CORS(app)

# 1️⃣ Get stations based on mode (metro / bus)
@app.get("/stations")
def get_stations():
    mode = request.args.get("mode")

    try:
        conn = get_connection()
        cur = conn.cursor()

        if mode == "metro":
            query = "SELECT station_name FROM delhi_metro_stations ORDER BY station_name;"
        elif mode == "bus":
            query = "SELECT station_name FROM bus_stations ORDER BY station_name;"
        else:
            return jsonify({"error": "Invalid mode"}), 400
        
        cur.execute(query)
        stations = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return jsonify({"stations": stations})

    except Exception as e:
        return jsonify({"error": str(e)})


# 2️⃣ Calculate stops + travel time
@app.get("/route")
def get_route():
    mode = request.args.get("mode")
    start = request.args.get("start")
    end = request.args.get("end")

    if not (mode and start and end):
        return jsonify({"error": "mode, start, end required"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Pick correct table
        if mode == "metro":
            table = "delhi_metro_stations"
        elif mode == "bus":
            table = "bus_stations"
        else:
            return jsonify({"error": "Invalid mode"}), 400

        query = f"SELECT stop_number FROM {table} WHERE station_name = %s;"

        cur.execute(query, (start,))
        start_stop = cur.fetchone()

        cur.execute(query, (end,))
        end_stop = cur.fetchone()

        if not start_stop or not end_stop:
            return jsonify({"error": "Station not found"}), 404

        start_num = start_stop[0]
        end_num = end_stop[0]

        stops = abs(end_num - start_num)

        if mode == "metro":
            approx_time = stops * 2
        else:
            approx_time = stops * 3

        cur.close()
        conn.close()

        return jsonify({
            "mode": mode,
            "start": start,
            "end": end,
            "stops": stops,
            "approx_time_minutes": approx_time
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ✅ Allow Render to set PORT automatically
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
