from google.cloud import dialogflowcx_v3
from openpyxl import Workbook
import asyncio
import time
import string
from datetime import datetime

# export GOOGLE_APPLICATION_CREDENTIALS="heartschat-prod-a505-9599eda00cef.json"

ALPHABET = list(string.ascii_uppercase)
ENDPOINT = "us-central1-dialogflow.googleapis.com"
AGENT = "projects/heartschat-prod-a505/locations/us-central1/agents/3eaf696f-5b7d-4e1e-b47c-5c9066d1dce9"
FLOW = "projects/heartschat-prod-a505/locations/us-central1/agents/3eaf696f-5b7d-4e1e-b47c-5c9066d1dce9/flows/00000000-0000-0000-0000-000000000000"

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
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.GetIntentRequest(name=intent_name)
    intent = await client.get_intent(request=request)
    return intent

async def write_routes(route_groups, intents):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Routes"
    fulfillments_sheet = workbook.create_sheet("Fulfillments")
    route_group_num = 0
    route_num = 1
    fulfillment_num = 1
    async for route_group in route_groups:
        sheet["{}1".format(ALPHABET[route_group_num])] = route_group.display_name
        intent_num = 2
        for route in route_group.transition_routes:
            route_sheet = workbook.create_sheet(str(route_num))
            route_sheet["A1"] = route.name
            time.sleep(1)
            intent = await get_intent(intents, route.intent)
            sheet["{}{}".format(ALPHABET[route_group_num], intent_num)] = intent.display_name
            sheet["{}{}".format(ALPHABET[route_group_num], intent_num)].hyperlink = "#{}!A1".format(route_num)
            message_num = 2
            for phrase in intent.training_phrases:
                phrase_text = "".join([part.text for part in phrase.parts])
                route_sheet["A{}".format(message_num)] = phrase_text
                message_num += 1
            message_num = 2
            for message in route.trigger_fulfillment.messages:
                route_sheet["B{}".format(message_num)] = message.text.text[message_num - 2]
                fulfillments_sheet["A{}".format(fulfillment_num)] = message.text.text[message_num - 2]
                message_num += 1
                fulfillment_num += 1
            intent_num += 1
            route_num += 1
        route_group_num += 1
    now = datetime.now()
    datetime_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    workbook.save(filename="route_map_{}.xlsx".format(datetime_string))

async def main():
    route_groups = await get_route_groups()
    intents = await get_intents()
    await write_routes(route_groups, intents)

if __name__ == '__main__':
    asyncio.run(main())
