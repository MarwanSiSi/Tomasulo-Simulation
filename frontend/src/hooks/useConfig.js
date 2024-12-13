import { useState } from "react";
export function useConfig() {
  const [config, setConfig] = useState({
    //file path
    filePath:
      "/home/ahmedgado/SharedDisk/GUC/Tomasulo-Simulation/instructions.txt",

    // Latencies
    floatAddSubLatency: 1,
    floatMulDivLatency: 1,
    intAddSubLatency: 1,

    // Load/store latencies
    cacheHitLatency: 1,
    cacheMissLatency: 1,

    // Station sizes
    floatAddSubStationSize: 1,
    floatMulDivStationSize: 1,

    loadBufferSize: 1,
    storeBufferSize: 1,

    intAddSubStationSize: 1,

    // Cache
    cacheSize: 1024,
    blockSize: 16,
  });

  return { config, setConfig };
}
