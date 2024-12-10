import { useState } from "react";

export function useConfig() {
  const [config, setConfig] = useState({
    addLatency: 2,
    subLatency: 2,
    mulLatency: 10,
    divLatency: 40,
    loadLatency: 2,
    storeLatency: 2,
    cacheSize: 1024,
    blockSize: 16,
  });

  return { config, setConfig };
}
