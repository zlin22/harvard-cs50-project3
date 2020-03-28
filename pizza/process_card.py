from square.client import Client
import uuid
 
# Create an instance of the API Client 
# and initialize it with the credentials 
# for the Square account whose assets you want to manage
 
client = Client(
    access_token='EAAAEDjhGlYSsPaPl8t01AzkGgY9nKZoI-z8vuqX8oSHXsQJ4O7qK6jGC2LudLpg',
    environment='sandbox',
)
 
# Get an instance of the Square API you want call
payments_api = client.payments
 
# Call list_locations method to get all locations in this Square account
# result = api_locations.list_locations()

nonce = "cnon:card-nonce-ok"
cents_charged = 1001

body = {
    "source_id": nonce,
    "idempotency_key": str(uuid.uuid1()),
    "amount_money": {"amount": cents_charged, "currency": "USD"}
}

payment_results = payments_api.create_payment(body)

# Call the success method to see if the call succeeded
if payment_results.is_success():
	# The body property is a list of locations
    res = payment_results.body['payment']
	# Iterate over the list
    print(res)
# Call the error method to see if the call failed
elif payment_results.is_error():
    print('Error calling payment API')
    errors = payment_results.errors
    # An error is returned as a list of errors
    for error in errors:
    	# Each error is represented as a dictionary
        for key, value in error.items():
            print(f"{key} : {value}")
        print("\n")