# Hotel tool function
def hotel_tool():

    # Return fake hotel data
    return {
        "message": "Hotels found",
        "ui_type": "hotel_page",
        "data": {
            "hotels": [
                {
                    "name": "Grand Palace",
                    "price": "$220",
                    "rating": 4.8
                },
                {
                    "name": "Budget Inn",
                    "price": "$90",
                    "rating": 4.1
                }
            ]
        }
    }

def get_cheaper_hotels():

    # Get all hotels from hotel tool
    hotels = hotel_tool()["data"]["hotels"]

    # Keep only hotels under $100
    cheaper_hotels = []

    for hotel in hotels:

        #converting price to number
        price = int(hotel["price"].replace("$", ""))

 
        if price < 100:

            # Add to cheaper hotel list
            cheaper_hotels.append(hotel)

    return {
        "message": "Cheaper hotels found",
        "ui_type": "hotel_page",
        "data": {
            "hotels": cheaper_hotels
        }
    }