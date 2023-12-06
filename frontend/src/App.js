import "./App.css";
import Header from "./Header/Header";
import GPUList from "./GPUList/GPUList";
import Description from "./Description/Description";
import { useState } from "react";
// import Prices from "./Prices/Prices";
// import ChartComponent from "./Chart/Chart";

function App() {
  const [isDetailsPage, setIsDetailsPage] = useState(false);
  const [currentGPU, setCurrentGPU] = useState(null);

  const setGPU = (gpu) => {
    setCurrentGPU(gpu);
  };

  const setDetails = (val) => {
    setIsDetailsPage(val);
  };
  return (
    <div className="App">
      <Header />
      {!isDetailsPage && (
        <GPUList setIsDetailsPage={setDetails} setGPU={setGPU} />
      )}
      {isDetailsPage && <Description gpu={currentGPU} />}
    </div>
  );
}

export default App;
