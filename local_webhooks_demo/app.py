from flask import Flask, request, json, jsonify, abort

app = Flask(__name__)

offer_list, counter_list = [], []
price_floor = 750
price_ceiling = 1000
price_median = (price_floor + price_ceiling) / 2

@app.route('/', methods=['POST'])
def manage_offers():
    if not request.json['queryResult']['allRequiredParamsPresent']:
        return(create_response(request.json['fulfillmentMessages']))
    action = request.json['queryResult']['action']
    print(request.json)
    if action in ['process.offer', 'final.offer']:
        offer = request.json['queryResult']['parameters']['offer']['amount']
        offer_list.append(int(offer))
    if action == 'process.offer':
        return(process_offer())
    if action == 'final.offer':
        return(final_offer())
    if action == 'accept':
        return(accept_offer())
    if action == 'decline':
        return(decline_offer())
    return(create_response(request.json['fulfillmentMessages']))

def process_offer():
    offer = offer_list[-1]
    if len(offer_list) == 1:
        return(first_offer(offer))
    if offer >= price_median:
        return(create_response("Sold for $", offer))
    if offer >= price_floor:
        if is_increasing():
            counter = get_average()
            counter_list.append(counter)
            return(create_response("How about $", counter))
        if is_decreasing():
            counter = max(max(offer_list), price_floor)
            counter_list.append(counter)
            return(create_response("How about $", counter))
        if is_duplicate():
            return(final_offer())
    if offer < price_floor:
        return(create_response("That's a bit too low. How about something in the range of $", price_floor))
    

def first_offer(offer):
    message = ""
    if offer >= price_median:
        return(create_response("Sold for $", offer))
    counter = get_average()
    counter_list.append(counter)
    return(create_response("How about $", counter))

def final_offer():
    offer = offer_list[-1]
    if offer >= price_floor:
        return(create_response("Sold for $", offer))
    return(create_response("I'm sorry. I can't take that offer. Have a good day."))

def accept_offer():
    if len(offer_list) > len(counter_list):
        winning_offer = offer_list[-1]
    else:
        winning_offer = counter_list[-1]
    return(create_response("Sold for $", winning_offer))

def decline_offer():
    return(create_response("I'm sorry about that. Have a good day."))

def get_average():
    weight = min(len(offer_list), 5) * 0.1
    return(weight * offer_list[-1] + (1 - weight) * price_median)

def is_decreasing():
    return offer_list[-1] < offer_list[-2]

def is_increasing():
    return offer_list[-1] > offer_list[-2]

def is_duplicate():
    return offer_list[-1] == offer_list[-2]

def create_response(message, number=0):
    response = {
        "fulfillmentMessages": [{
            "text": {
                "text": [
                    message + str(round(number))
                ]
            }
        }]
    }
    return(jsonify(response))

if __name__ == '__main__':
    app.run(debug=True)
