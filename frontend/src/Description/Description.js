/* eslint-disable react/jsx-no-target-blank */
/* eslint-disable jsx-a11y/anchor-is-valid */
import "./Description.css"; // Import the CSS file
import amazon from "./logos/amazon.svg";
import bestbuy from "./logos/bestbuy.svg";
import walmart from "./logos/walmart.svg";
import newegg from "./logos/newegg.svg";
import ebay from "./logos/ebay.svg";

import {
  Card,
  CardHeader,
  Typography,
  CardBody,
  CardFooter,
  Avatar,
} from "@material-tailwind/react";
import React, { useState } from "react";
import Chart from "../Chart/Chart";

const TABLE_HEAD = ["Store", "Price", "Link"];

const logos = {
  amazon: amazon,
  bestbuy: bestbuy,
  walmart: walmart,
  newegg: newegg,
  ebay: ebay,
};

function DetailsPage({ gpu }) {
  const { model, brand, description, features, image_url, release_date, url } =
    gpu;
  const [prices, setPrices] = useState(null);
  const [pastPrices, setPastPrices] = useState(null);
  const [showTrends, setShowTrends] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const showRealTimePrices = () => {
    setIsLoading(true);
    console.log("fetchData called with search_term:", model);
    fetch(`http://localhost:8000/prices`, {
      method: "POST", // or 'PUT', depending on your requirement
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        search_term: model,
      }), // make sure bodyData is an object
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setPrices(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      });
  };

  function extractDateAndTime(datetimeStr) {
    // Split the string at 'T' to separate date and time
    let [date, time] = datetimeStr.split("T");

    // Split the time part and take only the first two elements (hours and minutes)
    let timeWithoutSeconds = time.split(":").slice(0, 2).join(":");

    // Combine the date and time
    return `${date} ${timeWithoutSeconds}`;
  }
  function extractPastWeekPrices(dataArray) {
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    // Filter the data for the past week
    const lastWeekData = dataArray.filter(
      (item) => new Date(item.timestamp) >= oneWeekAgo
    );

    // Sort the filtered data in ascending order by timestamp
    lastWeekData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    // Extract and return the prices
    return lastWeekData.map((item) => item.price);
  }
  function extractPastMonthPricesTimeStamps(data) {
    data.sort((a, b) => {
      let dateA = new Date(a.timestamp);
      let dateB = new Date(b.timestamp);
      return dateA - dateB;
    });
    return data.map((item) => extractDateAndTime(item.timestamp));
  }

  function extractPastWeekPricesTimeStamps(dataArray) {
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    // Filter the data for the past week
    const lastWeekData = dataArray.filter(
      (item) => new Date(item.timestamp) >= oneWeekAgo
    );

    // Sort the filtered data in ascending order by timestamp
    lastWeekData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    // Extract and return the prices
    return lastWeekData.map((item) => extractDateAndTime(item.timestamp));
  }
  function extractPastMonthPrices(data) {
    data.sort((a, b) => {
      let dateA = new Date(a.timestamp);
      let dateB = new Date(b.timestamp);
      return dateA - dateB;
    });
    return data.map((item) => item.price);
  }

  function showTrendsFunc() {
    fetch(`http://localhost:8000/last_month_prices`, {
      method: "POST", // or 'PUT', depending on your requirement
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        search_term: model,
      }), // make sure bodyData is an object
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setPastPrices(data);
        setShowTrends(true);
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      });
  }
  return (
    <div>
      <div className="details-page">
        <h1>{model}</h1>
        <p>
          <strong>Release Date:</strong> {release_date}
        </p>
        <p>
          <strong>Brand:</strong> {brand}
        </p>
        <img src={image_url} alt={model} />
        <p>{description}</p>
        <h2>Features</h2>
        <ul>
          {Object.entries(features).map(([key, value]) => (
            <li key={key}>
              <strong>{key}:</strong> {value}
            </li>
          ))}
        </ul>
        <a
          className="buttons"
          href={url}
          target="_blank"
          rel="noopener noreferrer"
        >
          Benchmark
        </a>
        <a
          className="buttons"
          onClick={showTrendsFunc}
          rel="noopener noreferrer"
        >
          Show Price Trends
        </a>
        <a
          className="buttons"
          onClick={showRealTimePrices}
          rel="noopener noreferrer"
        >
          Show Real-Time Prices
        </a>
        {showTrends && (
          <Chart
            className="chart"
            week_month="Week"
            x_axis={extractPastWeekPricesTimeStamps(pastPrices)}
            y_axis={extractPastWeekPrices(pastPrices)}
          />
        )}
        {showTrends && (
          <Chart
            className="chart"
            week_month="Month"
            x_axis={extractPastMonthPricesTimeStamps(pastPrices)}
            y_axis={extractPastMonthPrices(pastPrices)}
          />
        )}
      </div>
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
                  {prices.map(
                    ({ store, product_price, product_link }, index) => {
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
                            <a href={product_link} target="_blank">
                              Visit
                            </a>
                          </td>
                        </tr>
                      );
                    }
                  )}
                </tbody>
              </table>
            </CardBody>
            <CardFooter className="flex items-center justify-between border-t border-blue-gray-50 p-4"></CardFooter>
          </Card>
        )}
        {isLoading && <p>Loading Live Prices</p>}
      </div>
    </div>
  );
}

export default DetailsPage;
