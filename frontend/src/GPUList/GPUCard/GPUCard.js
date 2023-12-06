/* eslint-disable jsx-a11y/img-redundant-alt */
import React from "react";
import "./GPUCard.css";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Button,
} from "@material-tailwind/react";

function GPUCard({ gpu, setGPU, setIsDetailsPage }) {
  return (
    <Card className="w-96 gpu-item" style={{ backgroundColor: "#2e3c43" }}>
      <CardHeader shadow={false} floated={false} className="h-96">
        <img
          src={gpu.image_url}
          alt="GPU Image"
          className="h-full w-50 object-cover"
        />
      </CardHeader>
      <CardBody>
        <div className="mb-2 flex items-center justify-between">
          <Typography color="white" className="font-medium">
            {gpu.model}
          </Typography>
          <Typography color="white" className="font-medium">
            {gpu.brand}
          </Typography>
        </div>
        <Typography
          variant="small"
          color="white"
          className="font-normal opacity-75"
        >
          {gpu.description && gpu.description.substring(0, 100) + "..."}
        </Typography>
      </CardBody>
      <CardFooter className="pt-0">
        <Button
          ripple={false}
          fullWidth={true}
          className="bg-green text-white shadow-none hover:scale-105 hover:shadow-none focus:scale-105 focus:shadow-none active:scale-100"
          onClick={() => {
            setGPU(gpu);
            setIsDetailsPage(true);
          }}
        >
          View More Details
        </Button>
      </CardFooter>
    </Card>
  );
}

export default GPUCard;
