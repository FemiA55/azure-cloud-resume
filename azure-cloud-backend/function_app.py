import azure.functions as func
import logging
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="GetResumeCount")
def GetResumeCount(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 1. Connect to Cosmos DB using keyless Managed Identity
    url = "https://azure.com"
    client = CosmosClient(url, credential=None) # Uses DefaultAzureCredential under the hood

    # 2. Target the exact database and container
    database = client.get_database_client('AzureResume')
    container = database.get_container_client('Counter')

    # 3. Read the baseline item we created in the portal (id="1", partition key="1")
    counter_item = container.read_item(item="1", partition_key="1")

    # 4. Increment the counter value by 1
    counter_item['count'] += 1

    # 5. Save the updated item back to Cosmos DB
    container.upsert_item(counter_item)

    # 6. Return the fresh count number back to your website browser response
    # We add CORS headers so your frontend website is legally allowed to talk to this API
    return func.HttpResponse(
        body=f"{counter_item['count']}", 
        status_code=200,
        headers={"Access-Control-Allow-Origin": "*"}
    )
