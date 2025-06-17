// pact/consumer-tests/shippingConsumer.test.js

const path = require("path");
const { Pact, Matchers } = require("@pact-foundation/pact");
const chai = require("chai");
const axios = require("axios");

const { like, integer, uuid } = Matchers;
const expect = chai.expect;

const provider = new Pact({
  consumer: "UIService",
  provider: "ShippingService",
  port: 1234,
  log: path.resolve(process.cwd(), "logs", "pact-shipping.log"),
  dir: path.resolve(process.cwd(), "pacts"),
  logLevel: "INFO",
});

describe("ShippingService Pact", () => {
  before(() => provider.setup());
  after(() => provider.finalize());
  afterEach(() => provider.verify());

  describe("POST /shipping", () => {
    before(() =>
      provider.addInteraction({
        state: "an order exists and shipping can be created",
        uponReceiving: "a request to create a shipping entry",
        withRequest: {
          method: "POST",
          path: "/shipping",
          headers: {
            Authorization: like("Bearer dummy-token"),
            "Content-Type": "application/json",
          },
          body: {
            orderId: integer(1),
            userId: integer(1),
            address: like("123 Main St, City, 123456"),
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            "Content-Type": "application/json",
          },
          body: {
            trackingId: uuid("550e8400-e29b-41d4-a716-446655440000"),
            orderId: integer(1),                                      
            status: like("Pending")
          },
        },
      })
    );

    it("creates a shipping entry and returns tracking ID", async () => {
      const res = await axios.post(
        "http://localhost:1234/shipping",
        {
          orderId: 1,
          userId: 1,
          address: "123 Main St, City, 123456",
        },
        {
          headers: {
            Authorization: "Bearer dummy-token",
            "Content-Type": "application/json",
          },
        }
      );

      expect(res.status).to.equal(200);
      expect(res.data).to.have.property("trackingId");
    });
  });
});
