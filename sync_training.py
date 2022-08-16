from google.cloud import dialogflowcx_v3
from utils import *
import asyncio

ENDPOINT = "us-central1-dialogflow.googleapis.com"
REFERENCE = "projects/heartschat-prod-a505/locations/us-central1/agents/e7128213-f538-44fa-847c-d9da090624a9"
AGENT = "projects/heartschat-prod-a505/locations/us-central1/agents/f41cee4e-0ec0-47bf-9fc5-80493e023fdf"

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