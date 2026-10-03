from flask import Flask, render_template, request
from scheduler import schedule_vehicles, job_sequencing
from database import save_vehicle, get_vehicles
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/schedule", methods=["POST"])
def schedule():

    vehicles = []

    vehicle_ids = request.form.getlist("vehicle_id")
    urgency = request.form.getlist("urgency")
    departure = request.form.getlist("departure")
    duration = request.form.getlist("duration")
    
    for i in range(len(vehicle_ids)):

        vehicles.append({
            "id": vehicle_ids[i],
            "urgency": int(urgency[i]),
            "departure": int(departure[i]),
            "duration": int(duration[i])
        })

    # Priority Queue + Greedy
    greedy_result = schedule_vehicles(vehicles)

    # Job Sequencing
    job_result = job_sequencing(vehicles)
    timeline = []

    for item in greedy_result:

        if item["status"] == "Scheduled":

            timeline.append({
                "vehicle": item["vehicle"],
                "start": item["slot"],
                "end": item["end_slot"],
                "urgency": item["urgency"]
            })
    for i, vehicle in enumerate(vehicles):

     status = greedy_result[i]["status"]

    save_vehicle(vehicle, status)
    # Dashboard statistics
    total_vehicles = len(vehicles)

    scheduled = sum(
        1 for item in greedy_result
        if item["status"] == "Scheduled"
    )

    not_scheduled = total_vehicles - scheduled

    total_duration = sum(
        vehicle["duration"]
        for vehicle in vehicles
    )

    return render_template(
        "index.html",
        result=greedy_result,
        job_result=job_result,
        total_vehicles=total_vehicles,
        scheduled=scheduled,
        not_scheduled=not_scheduled,
        total_duration=total_duration,
        timeline=timeline
    )
@app.route("/vehicles")
def vehicles():

    saved_vehicles = get_vehicles()

    return render_template(
        "vehicles.html",
        vehicles=saved_vehicles
    )
if __name__ == "__main__":
    app.run(debug=True)