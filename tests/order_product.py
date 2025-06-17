import pytest
from pact import Consumer, Provider
from pact.matchers import Like  # Import matchers
import requests

PACT_DIR = "./pacts"
MOCK_SERVER_URL = "http://localhost:1234"

# Define Pact contract
pact = Consumer("OrderService").has_pact_with(
    Provider("ProductService"),
    pact_dir=PACT_DIR
)

@pytest.fixture(scope="module")
def pact_setup():
    yield

def test_get_product_by_id(pact_setup):
    # Define flexible body using matchers
    expected_body = {
        "id": Like(1),
        "name": Like("SamsungGalaxy"),
        "price": Like(30000.0),
        "stock": Like(49)
    }

    pact.given("Product with ID 1 exists and has sufficient stock").upon_receiving(
        "a request for product with ID 1"
    ).with_request(
        method='GET',
        path='/products/1',
        headers={"Authorization": "Bearer dummy-token"}
    ).will_respond_with(
        status=200,
        headers={"Content-Type": "application/json"},
        body=expected_body
    )

    with pact:
        result = requests.get(
            MOCK_SERVER_URL + "/products/1",
            headers={"Authorization": "Bearer dummy-token"}
        )
        assert result.status_code == 200

        # Actual result should still match a fixed example
        assert result.json() == {
            "id": 1,
            "name": "SamsungGalaxy",
            "price": 30000.0,
            "stock": 49
        }
