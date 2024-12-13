import React from "react";
import { Upload } from "lucide-react";

const InstructionsTable = ({ instructions, handleFileUpload, handleReset }) => {
  return (
    <div>
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold mb-2">Instructions</h2>

        <div className="flex flex-col gap-5 mb-5">
          <div className="flex gap-4">
            <button
              onClick={handleReset}
              className="px-4 py-2 bg-red-500 text-black rounded hover:bg-opacity-75"
            >
              Reset Simulation
            </button>
            <label className="flex items-center gap-2 px-4 py-2 bg-indigo-400 text-black rounded cursor-pointer hover:bg-opacity-75">
              <Upload size={20} />
              Upload Instructions
              <input
                type="file"
                className="hidden"
                onChange={(e) => handleFileUpload(e)}
                accept=".txt"
              />
            </label>
          </div>
        </div>
      </div>

      <div className="overflow-y-auto max-h-72">
        <table className="min-w-full border">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              <th className="border p-2">Instruction</th>
            </tr>
          </thead>
          <tbody>
            {instructions.map((instruction, idx) => (
              <tr key={idx}>
                <td className="border p-2 text-center">{instruction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default InstructionsTable;
