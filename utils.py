from google.cloud import dialogflowcx_v3

ENDPOINT = "us-central1-dialogflow.googleapis.com"

async def get_route_groups(flow):
    client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ListTransitionRouteGroupsRequest(parent=flow)
    route_groups = await client.list_transition_route_groups(request=request)
    return route_groups

async def get_intents(agent):
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ListIntentsRequest(parent=agent)
    intents = await client.list_intents(request=request)
    return intents

async def update_intent(intent):
    client = dialogflowcx_v3.IntentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.UpdateIntentRequest(intent=intent)
    reesponse = await client.update_intent(request=request)

async def get_route_group(route_group_name):
    client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.GetTransitionRouteGroupRequest(name=route_group_name)
    route_group = await client.get_transition_route_group(request=request)
    return route_group          

async def get_pages(flow):
    client = dialogflowcx_v3.PagesAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ListPagesRequest(parent=flow)
    pages = await client.list_pages(request=request)
    return pages

async def update_page(page):
    client = dialogflowcx_v3.PagesAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.UpdatePageRequest(page=page)
    response = await client.update_page(request=request)

async def update_route_group(route_group):
    client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.UpdateTransitionRouteGroupRequest(transition_route_group=route_group)
    response = await client.update_transition_route_group(request=request)
