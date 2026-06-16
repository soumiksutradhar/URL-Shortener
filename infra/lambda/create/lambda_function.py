import json, os, boto3, hashlib, base64, time

TABLE  = os.environ["TABLE_NAME"]
DOMAIN = os.environ["DOMAIN"]
dynamo = boto3.resource("dynamodb").Table(TABLE)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        original_url = body.get("url", "").strip()

        if not original_url.startswith("http"):
            return _response(400, {"error": "Invalid URL"})

        code = _short_code(original_url)
        dynamo.put_item(
            Item={
                "shortCode":   code,
                "originalUrl": original_url,
                "createdAt":   int(time.time()),
                "ttl":         int(time.time()) + 60 * 60 * 24 * 90,
            },
            ConditionExpression="attribute_not_exists(shortCode)",
        )
        return _response(201, {"shortUrl": f"{DOMAIN}/{code}", "code": code})

    except dynamo.meta.client.exceptions.ConditionalCheckFailedException:
        return _response(200, {"shortUrl": f"{DOMAIN}/{code}", "code": code})
    except Exception as exc:
        print(f"ERROR: {exc}")
        return _response(500, {"error": "Internal server error"})

def _short_code(url):
    digest = hashlib.sha256(url.encode()).digest()
    return base64.urlsafe_b64encode(digest)[:7].decode()

def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
