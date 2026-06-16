import json, os, boto3

TABLE  = os.environ["TABLE_NAME"]
dynamo = boto3.resource("dynamodb").Table(TABLE)

def lambda_handler(event, context):
    code = (event.get("pathParameters") or {}).get("code", "")

    if not code:
        return _response(400, {"error": "Missing code"})

    item = dynamo.get_item(Key={"shortCode": code}).get("Item")
    if not item:
        return _response(404, {"error": "Not found"})

    return {
        "statusCode": 301,
        "headers": {
            "Location": item["originalUrl"],
            "Cache-Control": "no-cache",
        },
        "body": "",
    }

def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
