import azure.functions as func
import logging
import requests  # Non-native third-party package

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="michi_entry")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Test third-party library execution
    try:
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_address = ip_response.json().get("ip", "Unknown")
        requests_status = f"Successfully used 'requests' package! Outbound IP: {ip_address}"
    except Exception as e:
        requests_status = f"Error calling external API with requests: {str(e)}"

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully. BIG GUY!!!\n\n[{requests_status}]"
        )
    else:
        return func.HttpResponse(
            f"This HTTP triggered function executed successfully. Yeah MICHI.\n\n[{requests_status}]",
            status_code=200
        )