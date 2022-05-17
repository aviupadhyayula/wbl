from google.cloud import dialogflowcx_v3 as dialogflow
import asyncio
import csv

AGENT = "projects/{}/locations/us-central1/agents/{}".format("heartschat-prod-a505", "37dd682b-aa44-48eb-bffc-86e80b93e38c")
ENDPOINT = "us-central1-dialogflow.googleapis.com"

async def get_intents():
    client = dialogflow.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflow.ListIntentsRequest(parent=AGENT)
    page_result = await client.list_intents(request=request)
    # with open('intents.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     async for response in page_result:
    #         writer.writerow(response['display_name'])
    #         writer.writerow(response['training_phrases'])
    with open('intents.txt', 'w') as f:
        async for response in page_result:
            f.write(str(response))

async def get_flows():
    client = dialogflow.FlowsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflow.GetFlowRequest(name=AGENT + "/flows/00000000-0000-0000-0000-000000000000")
    response = await client.get_flow(request=request)
    with open('flows.txt', 'a') as f:
        f.write(str(response))

def main():
    asyncio.run(get_intents())
    # asyncio.run(get_flows())

main()