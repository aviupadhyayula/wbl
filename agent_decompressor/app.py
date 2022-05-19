from google.cloud import dialogflowcx_v3
import asyncio
from openpyxl import Workbook

# export GOOGLE_APPLICATION_CREDENTIALS="heartschat-prod-a505-de929d994427.json"

PROJECT_ID = "heartschat-prod-a505"
AGENT_ID = "37dd682b-aa44-48eb-bffc-86e80b93e38c"
LOCATION_ID = "us-central1"
ENDPOINT_ID = "us-central1-dialogflow.googleapis.com"
FLOW_ID = "00000000-0000-0000-0000-000000000000"
AGENT = "projects/{}/locations/{}/agents/{}".format(PROJECT_ID, LOCATION_ID, AGENT_ID)
FLOW = "{}/flows/{}".format(AGENT, FLOW_ID)

async def get_intents():
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT_ID})
    request = dialogflow.ListIntentsRequest(parent=AGENT)
    intents = await client.list_intents(request=request)
    return intents

async def write_intents(intents):
    workbook = Workbook()
    sheet = workbook.active
    row = 1
    async for intent in intents:
        display_name = display_name.replace("?", "")
        sheet["A{}".format(row)] = intent.display_name
        intent_sheet = workbook.create_sheet(intent.display_name)
        sub_row = 1
        for phrase in intent.training_phrases:
            phrase_text += [part.text for part in phrase.parts]
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

def main():
    # intents = asyncio.run(get_intents())
    # asyncio.run(write_intents(intents))
    asyncio.run(get_flows())

main()