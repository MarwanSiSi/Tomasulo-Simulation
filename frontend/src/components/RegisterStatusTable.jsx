import { useState } from "react";
import PropTypes from "prop-types";
import { Search, Pin, PinOff, Upload } from "lucide-react";

const RegisterStatusTable = ({
  registers,
  onRegFileUpload,
  pinnedRegisters,
  setPinnedRegisters,
}) => {
  const [searchQuery, setSearchQuery] = useState("");

  const fullRegisterMap = {
    ...Array(32)
      .fill()
      .reduce(
        (acc, _, idx) => ({
          ...acc,
          [`R${idx}`]: registers[`R${idx}`] || {
            value: 0,
            busy: false,
            station: null,
          },
        }),
        {}
      ),
    ...Array(32)
      .fill()
      .reduce(
        (acc, _, idx) => ({
          ...acc,
          [`F${idx}`]: registers[`F${idx}`] || {
            value: 0,
            busy: false,
            station: null,
          },
        }),
        {}
      ),
  };

  const filteredRegisters = Object.entries(fullRegisterMap).filter(
    ([regName]) => {
      return (
        pinnedRegisters.has(regName) ||
        (searchQuery !== "" &&
          regName.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }
  );

  const handlePinToggle = (regName) => {
    setPinnedRegisters((prev) => {
      const newPinned = new Set(prev);
      if (newPinned.has(regName)) {
        newPinned.delete(regName);
      } else {
        newPinned.add(regName);
      }
      return newPinned;
    });
  };

  // Separate pinned and searched registers
  const pinnedOnly = Object.entries(fullRegisterMap).filter(([regName]) =>
    pinnedRegisters.has(regName)
  );

  const searchedOnly = Object.entries(fullRegisterMap).filter(
    ([regName]) =>
      !pinnedRegisters.has(regName) &&
      searchQuery !== "" &&
      regName.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Register File</h2>
        <label className="flex items-center gap-2 px-4 py-2 bg-indigo-400 text-black rounded cursor-pointer hover:bg-opacity-75">
          <Upload size={16} />
          Upload Registers
          <input
            type="file"
            className="hidden"
            onChange={onRegFileUpload}
            accept=".txt"
          />
        </label>
      </div>

      <div className="relative">
        <input
          type="text"
          placeholder="Search registers (e.g., R0, F16)"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-10 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
      </div>

      {/* Pinned Registers - Always in normal flow */}
      {pinnedOnly.length > 0 && (
        <div className="space-y-6 min-w-[400px]">
          <div className="space-y-2">
            <h3 className="font-semibold text-lg">Pinned Registers</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full border">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="border p-2">Register</th>
                    <th className="border p-2">Value</th>
                    <th className="border p-2">Busy</th>
                    <th className="border p-2">Station</th>
                    <th className="border p-2">Pin</th>
                  </tr>
                </thead>
                <tbody>
                  {pinnedOnly.map(([regName, reg]) => (
                    <tr key={regName} className="bg-blue-50">
                      <td className="border p-2 font-medium text-center">
                        {regName}
                      </td>
                      <td className="border p-2 text-center">{reg.value}</td>
                      <td className="border p-2 text-center">
                        {reg.busy ? "Yes" : "No"}
                      </td>
                      <td className="border p-2 text-center">
                        {reg.station || "-"}
                      </td>
                      <td className="border p-2 text-center">
                        <button
                          onClick={() => handlePinToggle(regName)}
                          className="hover:bg-gray-100 p-1 rounded-full"
                        >
                          <PinOff className="h-4 w-4 text-blue-500" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Search Results - Absolute positioned with scroll */}
      {searchQuery && searchedOnly.length > 0 && (
        <div className="absolute z-10 bg-white shadow-lg rounded-lg border min-w-[400px] max-h-[300px] overflow-y-auto">
          <div className="space-y-2 p-4">
            <h3 className="font-semibold text-lg">Search Results</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full border">
                <thead className="bg-gray-100 sticky top-0">
                  <tr>
                    <th className="border p-2">Register</th>
                    <th className="border p-2">Value</th>
                    <th className="border p-2">Busy</th>
                    <th className="border p-2">Station</th>
                    <th className="border p-2">Pin</th>
                  </tr>
                </thead>
                <tbody>
                  {searchedOnly.map(([regName, reg]) => (
                    <tr key={regName} className="bg-yellow-50">
                      <td className="border p-2 font-medium text-center">
                        {regName}
                      </td>
                      <td className="border p-2 text-center">{reg.value}</td>
                      <td className="border p-2 text-center">
                        {reg.busy ? "Yes" : "No"}
                      </td>
                      <td className="border p-2 text-center">
                        {reg.station || "-"}
                      </td>
                      <td className="border p-2 text-center">
                        <button
                          onClick={() => handlePinToggle(regName)}
                          className="hover:bg-gray-100 p-1 rounded-full"
                        >
                          <Pin className="h-4 w-4 text-gray-400" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {searchQuery && filteredRegisters.length === 0 && (
        <div className="text-center py-4 text-gray-500">
          No registers found matching &quot;{searchQuery}&quot;
        </div>
      )}

      {!searchQuery && pinnedRegisters.size === 0 && (
        <div className="text-center py-4 text-gray-500">
          Type a register name to see its details
        </div>
      )}
    </div>
  );
};

RegisterStatusTable.propTypes = {
  pinnedRegisters: PropTypes.instanceOf(Set).isRequired,
  setPinnedRegisters: PropTypes.func.isRequired,
  registers: PropTypes.objectOf(
    PropTypes.shape({
      value: PropTypes.number.isRequired,
      busy: PropTypes.bool.isRequired,
      station: PropTypes.string,
    })
  ).isRequired,
  onRegFileUpload: PropTypes.func.isRequired,
};

export default RegisterStatusTable;
