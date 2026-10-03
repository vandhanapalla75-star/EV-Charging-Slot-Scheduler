import heapq


# -----------------------------------
# PRIORITY QUEUE + GREEDY
# -----------------------------------

def schedule_vehicles(vehicles):

    priority_queue = []

    for vehicle in vehicles:

        # Higher urgency gets higher priority
        priority = -vehicle["urgency"]

        heapq.heappush(
            priority_queue,
            (priority, vehicle["departure"], vehicle)
        )

    schedule = []
    current_time = 1

    while priority_queue:

        _, _, vehicle = heapq.heappop(priority_queue)

        start_time = current_time
        end_time = start_time + vehicle["duration"]

        if end_time <= vehicle["departure"]:

            schedule.append({
                "vehicle": vehicle["id"],
                "slot": start_time,
                "end_slot": end_time,
                "urgency": vehicle["urgency"],
                "departure": vehicle["departure"],
                "duration": vehicle["duration"],
                "status": "Scheduled",
                "reason": "High urgency and feasible before departure"
            })

            current_time = end_time

        else:

            schedule.append({
                "vehicle": vehicle["id"],
                "slot": "-",
                "end_slot": "-",
                "urgency": vehicle["urgency"],
                "departure": vehicle["departure"],
                "duration": vehicle["duration"],
                "status": "Not Scheduled",
                "reason": "Not enough time before departure"
            })

    return schedule


# -----------------------------------
# JOB SEQUENCING
# -----------------------------------

def job_sequencing(vehicles):

    # Sort vehicles by urgency
    jobs = sorted(
        vehicles,
        key=lambda x: x["urgency"],
        reverse=True
    )

    max_slot = max(
        vehicle["departure"]
        for vehicle in vehicles
    )

    occupied = [False] * (max_slot + 1)

    result = []

    for vehicle in jobs:

        duration = vehicle["duration"]
        deadline = vehicle["departure"]

        assigned_start = None

        # Try to find the latest possible slot
        for start in range(
            deadline - duration,
            0,
            -1
        ):

            possible = True

            for slot in range(
                start,
                start + duration
            ):

                if occupied[slot]:
                    possible = False
                    break

            if possible:

                assigned_start = start
                break

        if assigned_start is not None:

            for slot in range(
                assigned_start,
                assigned_start + duration
            ):
                occupied[slot] = True

            result.append({
                "vehicle": vehicle["id"],
                "start": assigned_start,
                "end": assigned_start + duration,
                "urgency": vehicle["urgency"],
                "departure": vehicle["departure"],
                "status": "Scheduled",
                "reason": "Latest feasible slot before deadline"
            })

        else:

            result.append({
                "vehicle": vehicle["id"],
                "start": "-",
                "end": "-",
                "urgency": vehicle["urgency"],
                "departure": vehicle["departure"],
                "status": "Not Scheduled",
                "reason": "No available slot before deadline"
            })

    return result