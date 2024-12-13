import { useState } from "react";
import { createStations } from "../utils/helpers.js";

export const useStations = (config) => {
  // Initialize all stations based on config
  const [floatAddSubStations, setFloatAddSubStations] = useState(() =>
    createStations("AF", config.floatAddSubStationSize)
  );

  const [floatMulDivStations, setFloatMulDivStations] = useState(() =>
    createStations("MF", config.floatMulDivStationSize)
  );

  const [intAddSubStations, setIntAddSubStations] = useState(() =>
    createStations("AI", config.intAddSubStationSize)
  );

  const [loadStations, setLoadStations] = useState(() =>
    createStations("L", config.loadBufferSize)
  );

  const [storeStations, setStoreStations] = useState(() =>
    createStations("S", config.storeBufferSize)
  );

  // Helper function to reset all stations
  const resetAllStations = () => {
    setFloatAddSubStations(createStations("AF", config.floatAddSubStationSize));
    setFloatMulDivStations(createStations("MF", config.floatMulDivStationSize));

    setIntAddSubStations(createStations("AI", config.intAddSubStationSize));

    setLoadStations(createStations("L", config.loadBufferSize));

    setStoreStations(createStations("S", config.storeBufferSize));
  };

  return {
    // Station states
    floatAddSubStations,
    floatMulDivStations,

    intAddSubStations,

    loadStations,
    storeStations,

    // Station setters
    setFloatAddSubStations,
    setFloatMulDivStations,
    setIntAddSubStations,

    setLoadStations,
    setStoreStations,

    // Helper functions
    resetAllStations,
  };
};
