import ConfigPanel from "./components/ConfigPanel";
import Cache from "./components/Cache";
import InstructionsTable from "./components/InstructionsTable";
import ReservationStationTable from "./components/ReservationStationTable";
import RegisterStatusTable from "./components/RegisterStatusTable";
import { useStations } from "./hooks/useStations";
import { useConfig } from "./hooks/useConfig";
import { useFunctions } from "./hooks/useFunctions";
import InstructionQueue from "./components/InstQueue";

function App() {
  const { config, setConfig } = useConfig();

  const {
    floatAddSubStations,
    floatMulDivStations,

    loadStations,
    storeStations,

    intAddSubStations,
    intMulDivStations,

    resetAllStations,
  } = useStations(config);

  const {
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
  } = useFunctions();

  return (
    <div className="p-6 max-w-full mx-auto">
      <div className="mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-bold">Tomasulo Simulator</h1>
      </div>

      <div className="flex w-full gap-6">
        <div className="flex-grow">
          <ConfigPanel config={config} setConfig={setConfig} />

          <InstructionsTable
            hasLoop={hasLoop}
            instructions={instructions}
            handleFileUpload={handleFileUpload}
            handleReset={() => handleReset(resetAllStations)}
            className="mb-6"
          />

          <div className="flex items-center justify-end gap-5 mt-10 mb-0 ">
            <p className="text-2xl  font-bold text-end space-x-1">
              <span className="underline">Cycle:</span>
              <span>{cycle}</span>
            </p>
            <button
              onClick={nextCycle}
              className="px-4 py-2 bg-emerald-400 text-black rounded hover:bg-opacity-75"
            >
              Next Cycle
            </button>
          </div>

          <div className="flex gap-5">
            <div className="grid grid-cols-2 gap-6 w-3/4">
              <ReservationStationTable
                title="Load Buffer"
                stations={Object.entries(loadStations)}
                type="load"
                tableSize={config.loadBufferSize}
              />

              <ReservationStationTable
                title="Store Buffer"
                stations={Object.entries(storeStations)}
                type="store"
                tableSize={config.storeBufferSize}
              />

              <ReservationStationTable
                title="Float Add/Subtract Reservation Stations"
                stations={Object.entries(floatAddSubStations)}
                type="arithmetic"
                tableSize={config.floatAddSubStationSize}
              />

              <ReservationStationTable
                title="Float Multiply/Divide Reservation Stations"
                stations={Object.entries(floatMulDivStations)}
                type="arithmetic"
                tableSize={config.floatMulDivStationSize}
              />

              <ReservationStationTable
                title="Int Add/Subtract Reservation Stations"
                stations={Object.entries(intAddSubStations)}
                type="arithmetic"
                tableSize={config.intAddSubStationSize}
              />

              <ReservationStationTable
                title="Int Multiply/Divide Reservation Stations"
                stations={Object.entries(intMulDivStations)}
                type="arithmetic"
                tableSize={config.intMulDivStationSize}
              />
            </div>
            <div className="w-1/4">
              <div className="mt-10">
                <RegisterStatusTable
                  pinnedRegisters={pinnedRegisters}
                  setPinnedRegisters={setPinnedRegisters}
                  registers={registerFile}
                  onRegFileUpload={handleRegFileUpload}
                />
              </div>
              <div className="mt-10">
                <Cache />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-8 w-full">
        <div className="justify-end flex">
          <InstructionQueue
            instructions={[
              "Initialize system",
              "Load configuration",
              "Start processing",
              "Validate data",
            ]}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
