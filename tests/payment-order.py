import pytest
from pact import Consumer, Provider
from pact.matchers import Like
import requests

PACT_DIR = "./pacts"
MOCK_SERVER_URL = "http://localhost:1234"

# Define Pact contract
pact = Consumer("PaymentService").has_pact_with(
    Provider("OrderService"),
    pact_dir=PACT_DIR
)

@pytest.fixture(scope="module")
def pact_setup():
    yield

def test_update_order_status(pact_setup):
    order_id = 4

    # Flexible expected response
    expected_body = {
        "orderId": Like(order_id),
        "status": Like("Confirmed"),
        "message": Like("Order status updated successfully.")
    }

    pact.given("Order with ID 4 exists").upon_receiving(
        "a request to update order status to Confirmed"
    ).with_request(
        method="PATCH",
        path=f"/orders/{order_id}",
        headers={"Content-Type": "application/json"},
        body={"status": "Confirmed"}
    ).will_respond_with(
        status=200,
        headers={"Content-Type": "application/json"},
        body=expected_body
    )

    with pact:
        result = requests.patch(
            MOCK_SERVER_URL + f"/orders/{order_id}",
            json={"status": "Confirmed"}
        )
        assert result.status_code == 200

        # Hardcoded for consumer validation, flexible only in contract
        assert result.json() == {
            "orderId": 4,
            "status": "Confirmed",
            "message": "Order status updated successfully."
        }
