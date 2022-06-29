from google.cloud import dialogflowcx_v3
from openpyxl import Workbook, load_workbook
import asyncio
import time

# export GOOGLE_APPLICATION_CREDENTIALS="heartschat-prod-a505-9599eda00cef.json"

ROUTE_MAP = "route_map_06-29-2022_13-03-42.xlsx"
ENDPOINT = "us-central1-dialogflow.googleapis.com"
VARIANT_NAME = "create_variant_test_1"

async def create_variant():
    agent = dialogflowcx_v3.Agent()
    agent.display_name = VARIANT_NAME
    agent.default_language_code = "en"
    agent.time_zone = "GMT-8:00"
    client = dialogflowcx_v3.AgentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.CreateAgentRequest(parent="projects/heartschat-prod-a505/locations/us-central1", agent=agent)
    agent = await client.create_agent(request=request)
    return agent.name

async def export_reference():
    workbook = load_workbook(ROUTE_MAP)
    ref_sheet = workbook["Reference"]
    client = dialogflowcx_v3.AgentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ExportAgentRequest(name=ref_sheet["A1"].value)
    operation = await client.export_agent(request=request)
    response = await operation.result()
    return response.agent_content

async def restore_reference(agent_name, agent_content):
    client = dialogflowcx_v3.AgentsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.RestoreAgentRequest(name=agent_name, agent_content=agent_content)
    operation = await client.restore_agent(request=request)
    response = await operation.result()

async def get_route_groups(agent_name):
    client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT})
    request = dialogflowcx_v3.ListTransitionRouteGroupsRequest(parent="{}/flows/00000000-0000-0000-0000-000000000000".format(agent_name))
    route_groups = await client.list_transition_route_groups(request=request)
    return route_groups

async def update_variant(route_groups):
    workbook = load_workbook(ROUTE_MAP)
    ref_sheet = workbook["Reference"]
    async for route_group in route_groups:
        for route in route_group.transition_routes:
            for i in range(1, len(workbook.sheetnames) - 3):
                if route.name != ref_sheet["B{}".format(i)].value:
                    continue
                route_sheet = workbook[str(i)]
                for message in route.trigger_fulfillment.messages:
                    fulfillment_num = 1
                    for j in range(len(message.text.text)):
                        if route_sheet["B{}".format(fulfillment_num)].value:
                            message.text.text[j] = route_sheet["B{}".format(fulfillment_num)].value
                            fulfillment_num += 1
                        else:
                            message.text.text = message.text.text[:j]
                            break
                    for j in range(fulfillment_num, 999):
                        if route_sheet["B{}".format(j)].value:
                            message.text.text.append(route_sheet["B{}".format(j)].value)
                        else:
                            break
                break
        client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient(client_options={"api_endpoint": ENDPOINT})
        request = dialogflowcx_v3.UpdateTransitionRouteGroupRequest(transition_route_group=route_group)
        response = await client.update_transition_route_group(request=request)

async def main():
    variant_name = await create_variant()
    ref_content = await export_reference()
    await restore_reference(variant_name, ref_content)
    route_groups = await get_route_groups(variant_name)
    await update_variant(route_groups)

if __name__ == '__main__':
    asyncio.run(main())
