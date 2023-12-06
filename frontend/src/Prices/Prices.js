import {
  Card,
  CardHeader,
  Typography,
  CardBody,
  CardFooter,
  Avatar,
} from "@material-tailwind/react";
import React, { useState, useEffect } from "react";

const TABLE_HEAD = ["Store", "Price", "Link"];

const logos = {
  amazon: "./logos/amazon.svg",
  bestbuy: "./logos/bestbuy.svg",
  walmart: "./logos/walmart.svg",
  newegg: "./logos/newegg.svg",
  ebay: "./logos/ebay.svg",
};
export function Prices({ brand }) {
  const [prices, setPrices] = useState(null);
  const fetchData = (search_term) => {
    console.log("fetchData called with search_term:", search_term);
    fetch(`http://localhost:8000/prices`, {
      method: "POST", // or 'PUT', depending on your requirement
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        search_term: search_term,
      }), // make sure bodyData is an object
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => setPrices(data))
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      });
  };
  useEffect(() => {
    fetchData(brand);
  }, [brand]);
  return (
    <div>
      {prices && (
        <Card className="h-full w-full">
          <CardHeader floated={false} shadow={false} className="rounded-none">
            <div className="mb-4 flex flex-col justify-between gap-8 md:flex-row md:items-center">
              <div>
                <Typography variant="h5" color="blue-gray">
                  ONLINE PRICES
                </Typography>
              </div>
            </div>
          </CardHeader>
          <CardBody className="overflow-scroll px-0">
            <table className="w-full min-w-max table-auto text-left">
              <thead>
                <tr>
                  {TABLE_HEAD.map((head) => (
                    <th
                      key={head}
                      className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4"
                    >
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-normal leading-none opacity-70"
                      >
                        {head}
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {prices.map(({ store, product_price, link }, index) => {
                  return (
                    <tr key={store}>
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <Avatar
                            src={logos[store]}
                            alt={store}
                            size="md"
                            className="border border-blue-gray-50 bg-blue-gray-50/50 object-contain p-1"
                          />
                          <Typography
                            variant="small"
                            color="blue-gray"
                            className="font-bold"
                          >
                            {store}
                          </Typography>
                        </div>
                      </td>
                      <td className="p-4">
                        <Typography
                          variant="small"
                          color="blue-gray"
                          className="font-normal"
                        >
                          {product_price}
                        </Typography>
                      </td>
                      <td className="p-4">
                        <a
                          href={link}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Visit
                        </a>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </CardBody>
          <CardFooter className="flex items-center justify-between border-t border-blue-gray-50 p-4"></CardFooter>
        </Card>
      )}
      {!prices && <p>Loading Live Prices</p>}
    </div>
  );
}

export default Prices;
