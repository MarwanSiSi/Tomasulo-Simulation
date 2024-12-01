import React from "react";

const InstructionsTable = ({ instructions }) => {
  return (
    <div>
      <h2 className="text-xl font-bold mb-2">Instructions</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border p-2">Instruction</th>
              <th className="border p-2">j</th>
              <th className="border p-2">k</th>
              <th className="border p-2">Issue</th>
              <th className="border p-2">Execute</th>
              <th className="border p-2">Write</th>
            </tr>
          </thead>
          <tbody>
            {instructions.map((inst, idx) => (
              <tr key={idx}>
                <td className="border p-2">{inst.instruction}</td>
                <td className="border p-2">{inst.args}</td>
                <td className="border p-2">-</td>
                <td className="border p-2">{inst.issue}</td>
                <td className="border p-2">{inst.execute}</td>
                <td className="border p-2">{inst.writeResult}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default InstructionsTable;
