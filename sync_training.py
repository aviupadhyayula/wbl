from google.cloud import dialogflowcx_v3
from utils import *
import asyncio

# export GOOGLE_APPLICATION_CREDENTIALS=""

ENDPOINT = "us-central1-dialogflow.googleapis.com"
REFERENCE = ""
AGENT = ""

async def sync_training_phrases():
    ref_intents = await get_intents(REFERENCE)
    agent_intents = await get_intents(AGENT)
    async for agent_intent in agent_intents:
        async for ref_intent in ref_intents:
            if agent_intent.display_name == ref_intent.display_name:
                agent_intent.training_phrases = ref_intent.training_phrases
                await update_intent(agent_intent)

if __name__ == '__main__':
    asyncio.run(sync_training_phrases())