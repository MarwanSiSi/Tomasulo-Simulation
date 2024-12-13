import { useState } from "react";
import axios from "axios";

export const useFunctions = () => {
  const [instructions, setInstructions] = useState([]);
  const [hasLoop, setHasLoop] = useState(false);
  const [cycle, setCycle] = useState(0);
  const [registerFile, setRegisterFile] = useState({
    ...Array(32)
      .fill()
      .reduce(
        (acc, _, idx) => ({
          ...acc,
          [`R${idx}`]: { value: 0, busy: false, station: null },
        }),
        {}
      ),
    ...Array(32)
      .fill()
      .reduce(
        (acc, _, idx) => ({
          ...acc,
          [`F${idx}`]: { value: 0, busy: false, station: null },
        }),
        {}
      ),
  });
  console.log("registerFile", registerFile);
  const [pinnedRegisters, setPinnedRegisters] = useState(new Set());

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split("\n");

      // Filter out empty lines and create array of instructions
      const parsedInstructions = lines
        .filter((line) => line.trim())
        .map((line) => {
          // Handle lines with labels
          const [label, ...rest] = line.split(":");
          return rest.length > 0 ? rest[0].trim() : label.trim();
        });

      setInstructions(parsedInstructions);
    };
    reader.readAsText(file);
  };

  const handleRegFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    console.log("event", event);
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target.result;
        const regValues = text.split(",").reduce((acc, pair) => {
          const [reg, value] = pair.trim().split("=");
          if (reg && value) {
            acc[reg.trim()] = {
              value: Number(value),
              busy: false,
              station: null,
            };
          }
          return acc;
        }, {});

        setRegisterFile((prev) => ({
          ...prev,
          ...regValues,
        }));
      } catch (error) {
        console.error("Error parsing register file:", error);
        alert(
          "Invalid register file format. Expected format: R0=1,R1=2,F0=3.14,F1=2.5"
        );
      }
    };
    reader.readAsText(file);
  };

  const nextCycle = () => {
    setCycle((prev) => prev + 1);
  };

  const handleReset = (resetAllStations) => {
    setCycle(1);
    setHasLoop(false);
    setInstructions([]);
    resetAllStations();
    setPinnedRegisters(new Set());
    setRegisterFile({
      ...Array(32)
        .fill()
        .reduce(
          (acc, _, idx) => ({
            ...acc,
            [`R${idx}`]: { value: 0, busy: false, station: null },
          }),
          {}
        ),
      ...Array(32)
        .fill()
        .reduce(
          (acc, _, idx) => ({
            ...acc,
            [`F${idx}`]: { value: 0, busy: false, station: null },
          }),
          {}
        ),
    });
  };

  return {
    instructions,
    hasLoop,
    cycle,
    registerFile,
    pinnedRegisters,
    handleFileUpload,
    handleRegFileUpload,
    nextCycle,
    handleReset,
    setPinnedRegisters,
  };
};
