# Scripts for the Wharton Behavioral Lab's Negotiation Bot 

## map_routes.py

Converts a Dialogflow agent's dialog taxonomy to an easily-viewable Excel spreadsheet. Works by using Google's [Dialogflow CX Python client](https://googleapis.dev/python/dialogflow-cx/latest/index.html) to scrape an agent's pages in a particular flow.

### To use: 
- Download a credentials file from the Google Cloud Platform console.
- Run `export GOOGLE_APPLICATION_CREDENTIALS="<insert credentials here>"` in your terminal
- Set the `AGENT` environment variable to the agent whose routes you'd like to map. The content should be in the format `projects/.../locations/.../agents/...`
- Set the `FLOW` environment variable to the specific flow whose pages you'd like to scrape the routes from. The content should be in the format `{}/flows/...`

## create_variant.py

Enables mass editing of a Dialogflow agent's dialog via an Excel spreadsheet. Works by using a route map (see `map_routes.py`) to parse changes to an agent's fulfillments; then uploads the generated "variant" as a new Dialogflow agent.

### To use:
- Run `map_routes.py` on an existing agent.
- Edit route fulfillments as you'd like. Keep in mind that only fulfillments in the edited route map will be uploaded to the generated variant agent.
- Set the `ROUTE_MAP` environment variable to the file path of the edited route map.
- Set the `VARIANT_NAME` environment variable to the name of the new bot.

## prioritize_intent.py

Prioritizes a given intent by setting its internal priority value to an inputted integer. See [intent priorities](https://cloud.google.com/dialogflow/es/docs/intents-settings#priority).

### To use:
- Set the `INTENT` environment variable to the intent whose priority you'd like to change. The intent should be in the format `projects/.../locations/.../agents.../intents/...`
- Set the `NEW_PRIORITY` environment variable to the integer value you'd like.

## sync_training.py

Syncs training phrases for matching intents between two agents. Works by examining all common intents between a reference agent and a target agent, and then updating the target agent's training phrases with the reference agent's.

### To use:
- Set the `REFERENCE` environment variable to the agent whose training phrases you'd like to copy over. The content should be in the format `projects/.../locations/.../agents/...`
- Set the `AGENT` environment variable to the agent whose training phrases you'd like to update. The content should be in the format `projects/.../locations/.../agents/...`

## paraphrase_text.py

Paraphrases input text using [Google Research's PEGASUS model](https://huggingface.co/docs/transformers/model_doc/pegasus). 

### To use: 
- Set `sentence` variable to an input sentence you'd like.
