import pytest
from pact import Consumer, Provider, Like, Term
from clients import UserServiceClient # Import our new client

# Define the Pact consumer and provider
pact = Consumer('OrderService').has_pact_with(
    Provider('UserService'),
    # You can change the host and port for the mock server if needed
    pact_dir='../../pacts', # This is where the generated pact file will be stored
    host_name='localhost',
    port=1234
)

# Start the Pact mock server
#pact.start_service()

def test_get_user_details_with_valid_token():
    # Define the expected request and response for the interaction
    expected_response_body = {
        'id': Like(1), # The user ID should be a number
        'name': Like('Test User'), # The name should be a string
        'email': Term(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'user@example.com'), # Email format
    }

    # Set up the expected interaction on the mock server
    (pact
     .given('An authenticated user with a valid token exists for user_id 1')
     .upon_receiving('a request to get user details')
     .with_request(
         method='POST',
         path='/users/me',
         headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
         body={'access_token': 'a-valid-token', 'token_type': 'bearer'}
     )
     .will_respond_with(200, body=Like(expected_response_body)))

    # The `with pact:` block ensures that all interactions are verified
    # and the pact file is written.
    with pact:
        # Create an instance of our client pointed at the Pact mock server
        client = UserServiceClient(pact.uri)
        
        # Make the actual request from our client code
        user = client.verify_user_token('a-valid-token')

        # Assert that our client code correctly handles the response
        assert user['id'] == 1
        assert user['name'] == 'Test User'



# This will stop the mock server once all tests in this file are complete.
# It is important to do this to clean up the resources.
#pact.stop_service()