# Flight tool function
def flight_tool():

    #Return flight data
    return {
    "message": "Flights found",
    "ui_type": "flight_page",
    "data": {
        "flights": [
            {
                "airline": "Emirates",
                "price": "$450",
                "destination": "London"
            },
            {
                "airline": "Qatar Airways",
                "price": "$850",
                "destination": "London"
            }
        ]
    }
}

def get_cheaper_flights():

    # Get all flights from flight tool
    flights = flight_tool()["data"]["flights"]

    # Keep only flights under $500
    cheaper_flights = []

    for flight in flights:

        # Remove dollar sign and convert price to number
        price = int(flight["price"].replace("$", ""))

        # If flight is cheap
        if price < 500:

            # Add to cheaper flight list
            cheaper_flights.append(flight)

    return {
        "message": "Cheaper flights found",
        "ui_type": "flight_page",
        "data": {
            "flights": cheaper_flights
        }
    }