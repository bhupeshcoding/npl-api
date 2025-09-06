import json
from mangum import Mangum
from main import app

# Create a handler for Netlify
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    # Convert API Gateway event to ASGI scope
    asgi_scope = {
        "type": "http",
        "http_version": "1.1",
        "method": event["httpMethod"],
        "path": event["path"],
        "query_string": event.get("queryStringParameters", {}),
        "headers": [[k.lower().encode(), v.encode()] for k, v in event.get("headers", {}).items()],
        "server": (event.get("requestContext", {}).get("domainName", ""), 80),
        "client": (event.get("requestContext", {}).get("identity", {}).get("sourceIp", ""), 0),
        "asgi": {"version": "3.0"},
        "raw_path": event["path"].encode(),
        "root_path": ""
    }
    
    # Call the ASGI app
    response = handler(event, context)
    
    # Convert the response to the format expected by API Gateway
    return {
        "statusCode": response["statusCode"],
        "headers": response.get("headers", {}),
        "body": response["body"]
    }
