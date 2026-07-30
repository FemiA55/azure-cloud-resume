import azure.functions as func
import logging
import os
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="GetResumeCount")
def GetResumeCount(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # 1. Dynamically load your unique Cosmos URI endpoint from environment variables
        # Hardcoding the URI is bad practice; pull it cleanly from settings/app configurations
        cosmos_uri = os.environ.get("CosmosDBEndpointUri") 
        
        if not cosmos_uri:
            raise ValueError("CosmosDBEndpointUri environment variable is missing.")

        # 2. Authenticate securely via Managed Identity (Cloud) or AZ CLI/VS Code (Local)
        credential = DefaultAzureCredential()
        client = CosmosClient(cosmos_uri, credential=credential)

        # 3. Target database and container resources
        database = client.get_database_client('AzureResume')
        container = database.get_container_client('Counter')

        # 4. Transactionally retrieve, increment, and upsert counter object
        counter_item = container.read_item(item="1", partition_key="1")
        counter_item['count'] += 1
        container.upsert_item(counter_item)

        # 5. Return count value to client browser interface
        return func.HttpResponse(
            body=str(counter_item['count']), 
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "text/plain"
            }
        )

    except Exception as e:
        logging.error(f"Error processing counter operation: {str(e)}")
        return func.HttpResponse(
            body="Internal server error processing counter data.",
            status_code=500
        )
