from google.cloud import dialogflowcx_v3
from openpyxl import Workbook
import asyncio
import string
import re

# export GOOGLE_APPLICATION_CREDENTIALS="heartschat-prod-a505-de929d994427.json"

ALPHABET = list(string.ascii_uppercase)
PROJECT_ID = "heartschat-prod-a505"
AGENT_ID = "37dd682b-aa44-48eb-bffc-86e80b93e38c"
LOCATION_ID = "us-central1"
ENDPOINT_ID = "us-central1-dialogflow.googleapis.com"
FLOW_ID = "00000000-0000-0000-0000-000000000000"
AGENT = "projects/{}/locations/{}/agents/{}".format(PROJECT_ID, LOCATION_ID, AGENT_ID)
FLOW = "{}/flows/{}".format(AGENT, FLOW_ID)

async def get_intents():
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT_ID})
    request = dialogflowcx_v3.ListIntentsRequest(parent=AGENT)
    intents = await client.list_intents(request=request)
    await write_intents(intents)

async def write_intents(intents):
    workbook = Workbook()
    sheet = workbook.active
    row = 1
    async for intent in intents:
        intent.display_name = intent.display_name.replace("?", "")
        sheet["A{}".format(row)] = intent.display_name
        intent_sheet = workbook.create_sheet(intent.display_name)
        sub_row = 1
        for phrase in intent.training_phrases:
            phrase_text = "".join([part.text for part in phrase.parts])
            intent_sheet["A{}".format(sub_row)] = phrase_text
            sub_row += 1
        row += 1
    workbook.save(filename="dialog_map.xlsx")

async def get_flows():
    client = dialogflowcx_v3.FlowsAsyncClient(client_options={"api_endpoint": ENDPOINT_ID})
    request = dialogflowcx_v3.GetFlowRequest(name=FLOW)
    flow = await client.get_flow(request=request)
    with open('flows.txt', 'w') as f:
        f.write(str(flow))

async def get_route_groups():
    client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT_ID})
    request = dialogflowcx_v3.ListTransitionRouteGroupsRequest(parent=FLOW)
    route_groups = await client.list_transition_route_groups(request=request)
    await write_route_groups(route_groups)

async def get_intent(intent_id):
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT_ID})
    request = dialogflowcx_v3.GetIntentRequest(name=intent_id)
    intent = await client.get_intent(request=request)
    return intent

async def write_route_groups(route_groups):
    workbook = Workbook()
    sheet = workbook.active
    col = 0
    async for route_group in route_groups:
        sheet["{}1".format(ALPHABET[col])] = route_group.display_name
        intent_row = 2
        for route in route_group.transition_routes:
            intent = await get_intent(route.intent)
            sheet["{}{}".format(ALPHABET[col], intent_row)] = clean_string(intent.display_name)
            intent_sheet = workbook.create_sheet(clean_string(intent.display_name).replace("?", ""))
            sheet["{}{}".format(ALPHABET[col], intent_row)].hyperlink = "#{}!A1".format(clean_string(intent.display_name).replace("?", ""))
            phrase_row = 1
            for phrase in intent.training_phrases:
                phrase_text = "".join([part.text for part in phrase.parts])
                intent_sheet["A{}".format(phrase_row)] = phrase_text
                phrase_row += 1
            phrase_row = 1
            for message in route.trigger_fulfillment.messages:
                intent_sheet["B{}".format(phrase_row)] = clean_string(message.text)
                phrase_row += 1
            intent_row += 1
        col += 1
    workbook.save(filename="dialog_map.xlsx")

def clean_string(s):
    rx = re.compile('\W+')
    s = rx.sub("", str(s)).strip()
    return s


def main():
    # asyncio.run(get_intents())
    # asyncio.run(get_flows())
    asyncio.run(get_route_groups())

main()