import React, { useState, useEffect } from "react";
import "./GPUList.css";
import GPUCard from "./GPUCard/GPUCard";
import { IconButton, Typography } from "@material-tailwind/react";
import { ArrowRightIcon, ArrowLeftIcon } from "@heroicons/react/24/outline";
function GPUList({ setIsDetailsPage, setGPU }) {
  // Dummy data array. Replace with actual data fetching logic.
  const [data, setData] = useState(null);
  const [pages, setPages] = useState(1);
  const [active, setActive] = React.useState(1);

  const fetchData = (page) => {
    fetch(`http://localhost:8000/gpus?page=${page}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => setData(data))
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      });
  };

  const next = () => {
    if (active === pages) return;

    setActive(active + 1);
  };

  const prev = () => {
    if (active === 1) return;

    setActive(active - 1);
  };

  useEffect(() => {
    fetch("http://localhost:8000/gpu_count")
      .then((response) => response.json())
      .then((data) => setPages(Math.ceil(data / 9)));

    fetchData(1); // Fetch initial data for page 1
  }, []);

  useEffect(() => {
    fetchData(active);
  }, [active]);

  return (
    <div>
      <div className="grid-container">
        {data ? (
          data.map((gpu) => (
            <GPUCard
              className="gpu-item"
              key={gpu._id}
              gpu={gpu}
              setIsDetailsPage={setIsDetailsPage}
              setGPU={setGPU}
            />
          ))
        ) : (
          <p>Loading GPUs...</p>
        )}
      </div>
      {data && (
        <div className="flex items-center justify-center ">
          <div className="flex items-center gap-8">
            <IconButton
              size="sm"
              variant="outlined"
              onClick={prev}
              disabled={active === 1}
              className="text-white border-white" // Add Tailwind classes for white text and border
            >
              <ArrowLeftIcon strokeWidth={2} className="h-4 w-4 text-white" />{" "}
              {/* White icon */}
            </IconButton>
            <Typography color="white" className="font-normal text-white">
              {" "}
              {/* White text */}
              Page <strong className="text-white">{active}</strong> of{" "}
              {/* White text */}
              <strong className="text-white">{pages}</strong> {/* White text */}
            </Typography>
            <IconButton
              size="sm"
              variant="outlined"
              onClick={next}
              disabled={active === pages}
              className="text-white border-white" // Add Tailwind classes for white text and border
            >
              <ArrowRightIcon strokeWidth={2} className="h-4 w-4 text-white" />{" "}
              {/* White icon */}
            </IconButton>
          </div>
        </div>
      )}
    </div>
  );
}

export default GPUList;
