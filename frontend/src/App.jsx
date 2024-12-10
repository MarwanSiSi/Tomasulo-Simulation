import { useState } from "react";
import { Upload } from "lucide-react";
import ConfigPanel from "./components/ConfigPanel";
import InstructionsTable from "./components/InstructionsTable";
import ReservationStationTable from "./components/ReservationStationTable";
import RegisterStatusTable from "./components/RegisterStatusTable";
import { useStations } from "./hooks/useStations";
import { useConfig } from "./hooks/useConfig";

function App() {
  const [cycle, setCycle] = useState(1);
  const [instructions, setInstructions] = useState([]);
  const [registerFile, setRegisterFile] = useState(
    Array(10).fill({ value: 0, busy: false, station: null })
  );
  const {
    addSubStations,
    mulDivStations,
    loadStations,
    storeStations,
    updateStation,
    resetAllStations,
  } = useStations();

  const { config, setConfig } = useConfig();

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const parsedInstructions = text.split("\n").map((line) => {
        const [instruction, ...args] = line.trim().split(" ");
        return {
          instruction,
          args: args.join(" "),
          issue: null,
          execute: null,
          writeResult: null,
        };
      });
      setInstructions(parsedInstructions);
    };
    reader.readAsText(file);
  };

  const nextCycle = () => {
    setCycle((prev) => prev + 1);
  };

  const handleReset = () => {
    setCycle(1);
    setInstructions([]);
    resetAllStations();
    setRegisterFile(Array(10).fill({ value: 0, busy: false, station: null }));
  };

  return (
    <div className="p-6 max-w-full mx-auto">
      <div className="mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-bold">Tomasulo Simulator</h1>
        <div className="flex gap-4">
          <label className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded cursor-pointer hover:bg-blue-600">
            <Upload size={20} />
            Upload Instructions
            <input
              type="file"
              className="hidden"
              onChange={handleFileUpload}
              accept=".txt"
            />
          </label>
          <button
            onClick={nextCycle}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Next Cycle
          </button>
        </div>
      </div>

      <div className="mb-6 text-xl">
        Cycle: <span className="font-bold">{cycle}</span>
      </div>

      <div className="flex w-full gap-6">
        <div className="flex-grow">
          <ConfigPanel config={config} setConfig={setConfig} />

          <InstructionsTable instructions={instructions} className="mb-6" />

          <div className="grid grid-cols-2 gap-6 mt-10">
            <ReservationStationTable
              title="Load Stations"
              stations={Object.entries(loadStations)}
              type="load"
            />

            <ReservationStationTable
              title="Store Stations"
              stations={Object.entries(storeStations)}
              type="store"
            />

            <ReservationStationTable
              title="Add/Subtract Reservation Stations"
              stations={Object.entries(addSubStations)}
            />

            <ReservationStationTable
              title="Multiply/Divide Reservation Stations"
              stations={Object.entries(mulDivStations)}
            />
          </div>
        </div>

        <div className="w-1/4 mt-[254px]">
          <RegisterStatusTable registers={registerFile} />
        </div>
      </div>
    </div>
  );
}

export default App;
