import { useState } from "react";
import {
  createEmptyArithmeticStation,
  createEmptyLoadStation,
  createEmptyStoreStation,
  createStations,
} from "../utils/helpers.js";

export const useStations = (config) => {
  // Initialize all stations based on config
  const [floatAddSubStations, setFloatAddSubStations] = useState(() =>
    createStations(
      "AF",
      config.floatAddSubStationSize,
      createEmptyArithmeticStation
    )
  );

  const [floatMulDivStations, setFloatMulDivStations] = useState(() =>
    createStations(
      "MF",
      config.floatMulDivStationSize,
      createEmptyArithmeticStation
    )
  );

  const [intAddSubStations, setIntAddSubStations] = useState(() =>
    createStations(
      "AI",
      config.intAddSubStationSize,
      createEmptyArithmeticStation
    )
  );

  const [intMulDivStations, setIntMulDivStations] = useState(() =>
    createStations(
      "MI",
      config.intMulDivStationSize,
      createEmptyArithmeticStation
    )
  );

  const [loadStations, setLoadStations] = useState(() =>
    createStations("L", config.loadBufferSize, createEmptyLoadStation)
  );

  const [storeStations, setStoreStations] = useState(() =>
    createStations("S", config.storeBufferSize, createEmptyStoreStation)
  );

  // Helper function to reset all stations
  const resetAllStations = () => {
    setFloatAddSubStations(
      createStations(
        "AF",
        config.floatAddSubStationSize,
        createEmptyArithmeticStation
      )
    );
    setFloatMulDivStations(
      createStations(
        "MF",
        config.floatMulDivStationSize,
        createEmptyArithmeticStation
      )
    );

    setIntAddSubStations(
      createStations(
        "AI",
        config.intAddSubStationSize,
        createEmptyArithmeticStation
      )
    );
    setIntMulDivStations(
      createStations(
        "MI",
        config.intMulDivStationSize,
        createEmptyArithmeticStation
      )
    );

    setLoadStations(
      createStations("L", config.loadBufferSize, createEmptyLoadStation)
    );

    setStoreStations(
      createStations("S", config.storeBufferSize, createEmptyStoreStation)
    );
  };

  return {
    // Station states
    floatAddSubStations,
    floatMulDivStations,

    intAddSubStations,
    intMulDivStations,

    loadStations,
    storeStations,

    // Station setters
    setFloatAddSubStations,
    setFloatMulDivStations,
    setIntAddSubStations,
    setIntMulDivStations,

    setLoadStations,
    setStoreStations,

    // Helper functions
    resetAllStations,
  };
};
