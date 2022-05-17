from google.cloud import dialogflowcx_v3 as dialogflow
import asyncio

AGENT = "projects/{}/locations/us-central1/agents/{}"

client = dialogflow.IntentsAsyncClient(client_options={"api_endpoint": "us-central1-dialogflow.googleapis.com"})

async def get_intents():
    request = dialogflow.ListIntentsRequest(parent=AGENT.format("heartschat-prod-a505", "37dd682b-aa44-48eb-bffc-86e80b93e38c"))
    page_result = await client.list_intents(request=request)
    with open('intents.txt', 'w') as f:
        async for response in page_result:
            f.write(str(response))



def main():
    asyncio.run(list_intents())
