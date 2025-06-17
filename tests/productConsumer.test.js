// pact/consumer-tests/productConsumer.test.js

const path = require("path");
const { Pact, Matchers } = require("@pact-foundation/pact");
const chai = require("chai");
const axios = require("axios");

const { eachLike, like, decimal, integer } = Matchers;
const expect = chai.expect;

const provider = new Pact({
  consumer: "UIService",
  provider: "ProductService",
  port: 1234,
  log: path.resolve(process.cwd(), "logs", "pact.log"),
  dir: path.resolve(process.cwd(), "pacts"),
  logLevel: "INFO",
});

describe("ProductService Pact", () => {
  before(() => provider.setup());
  after(() => provider.finalize());
  afterEach(() => provider.verify());

  describe("GET /products/:id", () => {
    before(() =>
      provider.addInteraction({
        state: "product with ID '1' exists",
        uponReceiving: "a request to GET a product by ID",
        withRequest: {
          method: "GET",
          path: "/products/1",
          headers: {
            Authorization: like("Bearer dummy-token"),
            "Content-Type": "application/json",
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            "Content-Type": "application/json",
          },
          body: {
            id: integer(1),
            name: like("SamsungGalaxy"),
            price: decimal(30000.0),
            stock : integer(43)
          },
        },
      })
    );

    it("returns product details by ID", async () => {
      const res = await axios.get("http://localhost:1234/products/1", {
        headers: {
          Authorization: "Bearer dummy-token",
          "Content-Type": "application/json",
        },
      });

      expect(res.status).to.equal(200);
      expect(res.data).to.have.property("name");
      expect(res.data).to.have.property("price");
    });
  });

  describe("GET /products/", () => {
    before(() =>
      provider.addInteraction({
        state: "products exist",
        uponReceiving: "a request to GET all products",
        withRequest: {
          method: "GET",
          path: "/products/",
          headers: {
            Authorization: like("Bearer dummy-token"),
            "Content-Type": "application/json",
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            "Content-Type": "application/json",
          },
          body: eachLike({
            id: integer(1),
            name: like("SamsungGalaxy"),
            price: decimal(30000.0),
            stock : integer(43),
          }),
        },
      })
    );

    it("returns all products", async () => {
      const res = await axios.get("http://localhost:1234/products/", {
        headers: {
          Authorization: "Bearer dummy-token",
          "Content-Type": "application/json",
        },
      });

      expect(res.status).to.equal(200);
      expect(res.data).to.be.an("array");
      expect(res.data[0]).to.have.property("name");
      expect(res.data[0]).to.have.property("price");
    });
  });
});
