from google.cloud import dialogflowcx_v3
import asyncio

# export GOOGLE_APPLICATION_CREDENTIALS=""

ENDPOINT = "us-central1-dialogflow.googleapis.com"
INTENT = ""
NEW_PRIORITY = 500000

async def get_intent(intent_name):
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.GetIntentRequest(name=intent_name)
    intent = await client.get_intent(request=request)
    return intent

async def update_intent(intent, priority):
    intent.priority = priority
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.UpdateIntentRequest(intent=intent)
    await client.update_intent(request=request)

async def main():
    intent = await get_intent(INTENT)
    await update_intent(intent, NEW_PRIORITY)

if __name__ == '__main__':
    asyncio.run(main())
