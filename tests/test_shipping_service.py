from pact import Consumer, Provider, Like, Term
from clients import ShippingServiceClient # Import our new client
import uuid
import pytest

# Define the Pact consumer and provider
pact = Consumer('OrderService').has_pact_with(
    Provider('ShippingService'),
    # You can change the host and port for the mock server if needed
    pact_dir='../../pacts', # This is where the generated pact file will be stored
    host_name='localhost',
    port=1234
)

def test_create_shipping_request():
    order_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4()) 
    expected_response_body = {
        'trackingId': Term(
            generate=str(uuid.uuid4()),
            matcher='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        ),
        'orderId': Term(
            generate=order_id,
            matcher='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        ),
        'status': Term(
            generate='Pending',
            matcher='^(Pending|Shipped|In Transit|Delivered)$'
        )
    }

    (pact
     .given('An order is ready to be shipped')
     .upon_receiving(f'a request to create a shipment for order {order_id}')
     .with_request(
         method='POST',
         path='/shipping',
         headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
         body={
             'orderId': Like(order_id),
             'userId': Term(
                generate=str(uuid.uuid4()),
                matcher='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            ),
             'address': Like('123 Pact Lane, Contract City')
         }
     )
     .will_respond_with(200, body=Like(expected_response_body)))
    
    with pact:
        client = ShippingServiceClient(pact.uri)
        shipping_response = client.createShipping(
            orderId=order_id,
            userId=user_id,
            address='123 Pact Lane, Contract City'
        )
        
        # Assert that the client processed the response correctly
        assert uuid.UUID(shipping_response['trackingId'])
        assert shipping_response['orderId'] == order_id