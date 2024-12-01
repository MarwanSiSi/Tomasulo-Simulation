import { useState } from "react";

export const useStations = () => {
  const [addSubStations, setAddSubStations] = useState({
    A1: {
      busy: false,
      op: "",
      vj: "",
      vk: "",
      qj: "",
      qk: "",
      a: "",
      cycles: 0,
    },
    A2: {
      busy: false,
      op: "",
      vj: "",
      vk: "",
      qj: "",
      qk: "",
      a: "",
      cycles: 0,
    },
    A3: {
      busy: false,
      op: "",
      vj: "",
      vk: "",
      qj: "",
      qk: "",
      a: "",
      cycles: 0,
    },
  });

  const [mulDivStations, setMulDivStations] = useState({
    M1: {
      busy: false,
      op: "",
      vj: "",
      vk: "",
      qj: "",
      qk: "",
      a: "",
      cycles: 0,
    },
    M2: {
      busy: false,
      op: "",
      vj: "",
      vk: "",
      qj: "",
      qk: "",
      a: "",
      cycles: 0,
    },
  });

  const [loadStations, setLoadStations] = useState({
    L1: { busy: false, address: null, dest: null },
    L2: { busy: false, address: null, dest: null },
  });

  const [storeStations, setStoreStations] = useState({
    S1: { busy: false, address: null, v: null, q: null },
    S2: { busy: false, address: null, v: null, q: null },
  });

  // Helper function to update a specific station
  const updateStation = (stationType, stationId, updates) => {
    switch (stationType) {
      case "addSub":
        setAddSubStations((prev) => ({
          ...prev,
          [stationId]: { ...prev[stationId], ...updates },
        }));
        break;
      case "mulDiv":
        setMulDivStations((prev) => ({
          ...prev,
          [stationId]: { ...prev[stationId], ...updates },
        }));
        break;
      case "load":
        setLoadStations((prev) => ({
          ...prev,
          [stationId]: { ...prev[stationId], ...updates },
        }));
        break;
      case "store":
        setStoreStations((prev) => ({
          ...prev,
          [stationId]: { ...prev[stationId], ...updates },
        }));
        break;
    }
  };

  // Helper function to reset all stations
  const resetAllStations = () => {
    setAddSubStations({
      A1: {
        busy: false,
        op: "",
        vj: "",
        vk: "",
        qj: "",
        qk: "",
        a: "",
        cycles: 0,
      },
      A2: {
        busy: false,
        op: "",
        vj: "",
        vk: "",
        qj: "",
        qk: "",
        a: "",
        cycles: 0,
      },
      A3: {
        busy: false,
        op: "",
        vj: "",
        vk: "",
        qj: "",
        qk: "",
        a: "",
        cycles: 0,
      },
    });
    setMulDivStations({
      M1: {
        busy: false,
        op: "",
        vj: "",
        vk: "",
        qj: "",
        qk: "",
        a: "",
        cycles: 0,
      },
      M2: {
        busy: false,
        op: "",
        vj: "",
        vk: "",
        qj: "",
        qk: "",
        a: "",
        cycles: 0,
      },
    });
    setLoadStations({
      L1: { busy: false, address: null, dest: null },
      L2: { busy: false, address: null, dest: null },
    });
    setStoreStations({
      S1: { busy: false, address: null, v: null, q: null },
      S2: { busy: false, address: null, v: null, q: null },
    });
  };

  return {
    // Station states
    addSubStations,
    mulDivStations,
    loadStations,
    storeStations,

    // Station setters
    setAddSubStations,
    setMulDivStations,
    setLoadStations,
    setStoreStations,

    // Helper functions
    updateStation,
    resetAllStations,
  };
};
