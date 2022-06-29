from google.cloud import dialogflowcx_v3
from openpyxl import Workbook
from datetime import datetime
import asyncio
import string
import time

# export GOOGLE_APPLICATION_CREDENTIALS="heartschat-prod-a505-9599eda00cef.json"

ALPHABET = list(string.ascii_uppercase)
ENDPOINT = "us-central1-dialogflow.googleapis.com"
AGENT = "projects/heartschat-prod-a505/locations/us-central1/agents/3eaf696f-5b7d-4e1e-b47c-5c9066d1dce9"
FLOW = "{}/flows/00000000-0000-0000-0000-000000000000".format(AGENT)

async def get_route_groups():
    client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ListTransitionRouteGroupsRequest(parent=FLOW)
    route_groups = await client.list_transition_route_groups(request=request)
    return route_groups

async def get_intents():
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ListIntentsRequest(parent=AGENT)
    intents = await client.list_intents(request=request)
    return intents

async def get_intent(intents, intent_name):
    async for intent in intents:
        if intent.name == intent_name:
            return intent
    time.sleep(1)
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.GetIntentRequest(name=intent_name)
    intent = await client.get_intent(request=request)
    return intent

def create_workbook():
    workbook = Workbook()
    routes_sheet = workbook.active
    routes_sheet.title = "Routes"
    fulfillments_sheet = workbook.create_sheet("Fulfillments")
    ref_sheet = workbook.create_sheet("Reference")
    ref_sheet["A1"] = AGENT
    ref_sheet["A2"] = FLOW
    ref_sheet["A3"] = ENDPOINT
    now = datetime.now()
    datetime_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    return workbook, "route_map_{}.xlsx".format(datetime_string)

async def write_routes(route_groups, intents):
    workbook, workbook_name = create_workbook()
    routes_sheet = workbook["Routes"]
    fulfillments_sheet = workbook["Fulfillments"]
    ref_sheet = workbook["Reference"]
    route_group_num = 0
    route_num = 1
    fulfillment_num = 1
    async for route_group in route_groups:
        routes_sheet["{}1".format(ALPHABET[route_group_num])] = route_group.display_name
        intent_num = 2
        for route in route_group.transition_routes:
            route_sheet = workbook.create_sheet(str(route_num))
            ref_sheet["B{}".format(route_num)] = route.name
            message_num = 1
            for message in route.trigger_fulfillment.messages:
                for text in message.text.text:
                    route_sheet["B{}".format(message_num)] = text
                    fulfillments_sheet["A{}".format(fulfillment_num)] = text
                    message_num += 1
                    fulfillment_num += 1
            if route.intent == "":
                routes_sheet["{}{}".format(ALPHABET[route_group_num], intent_num)] = route.condition
                routes_sheet["{}{}".format(ALPHABET[route_group_num], intent_num)].hyperlink = "#{}!A1".format(route_num)
                intent_num += 1
                route_num += 1
                continue
            intent = await get_intent(intents, route.intent)
            routes_sheet["{}{}".format(ALPHABET[route_group_num], intent_num)] = intent.display_name
            routes_sheet["{}{}".format(ALPHABET[route_group_num], intent_num)].hyperlink = "#{}!A1".format(route_num)
            message_num = 1
            for phrase in intent.training_phrases:
                phrase_text = "".join([part.text for part in phrase.parts])
                route_sheet["A{}".format(message_num)] = phrase_text
                message_num += 1
            intent_num += 1
            route_num += 1
        route_group_num += 1
    workbook.save(filename=workbook_name)

async def main():
    route_groups = await get_route_groups()
    intents = await get_intents()
    await write_routes(route_groups, intents)

if __name__ == '__main__':
    asyncio.run(main())
