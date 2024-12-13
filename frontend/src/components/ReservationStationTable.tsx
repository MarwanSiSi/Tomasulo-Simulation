import React from "react";

const ReservationStationTable = ({
  title,
  stations,
  type = "arithmetic",
  tableSize,
}) => {
  // Generate empty rows if needed to match the configured size
  const generateEmptyRows = () => {
    const currentSize = stations.length;
    const targetSize = tableSize || stations.length; // Fallback to current size if not specified
    const emptyRows: [string, any][] = [];

    if (targetSize > currentSize) {
      const baseId = title.includes("Float") ? "F" : "I";
      const prefix =
        type === "load"
          ? "L"
          : type === "store"
          ? "S"
          : type === "arithmetic" && title.includes("Mul")
          ? "M"
          : "A";

      for (let i = currentSize + 1; i <= targetSize; i++) {
        const name = `${prefix}${baseId}${i}`;
        const emptyStation =
          type === "arithmetic"
            ? {
                name,
                busy: false,
                op: null,
                vj: null,
                vk: null,
                qj: null,
                qk: null,
                a: null,
              }
            : type === "load"
            ? {
                name,
                busy: false,
                address: null,
                dest: null,
              }
            : {
                name,
                busy: false,
                address: null,
                v: null,
                q: null,
              };
        emptyRows.push([name, emptyStation]);
      }
    }

    return [...stations, ...emptyRows];
  };

  const allRows = generateEmptyRows();

  return (
    <div>
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead
            className={`${
              title.includes("Float")
                ? "bg-purple-300"
                : title.includes("Int")
                ? "bg-red-300"
                : "bg-green-300"
            }`}
          >
            <tr>
              <th className="border p-2">Name</th>
              <th className="border p-2">Busy</th>
              {type === "arithmetic" && (
                <>
                  <th className="border p-2">Op</th>
                  <th className="border p-2">Vj</th>
                  <th className="border p-2">Vk</th>
                  <th className="border p-2">Qj</th>
                  <th className="border p-2">Qk</th>
                  <th className="border p-2">Address</th>
                </>
              )}
              {type === "load" && (
                <>
                  <th className="border p-2">Address</th>
                </>
              )}
              {type === "store" && (
                <>
                  <th className="border p-2">Address</th>
                  <th className="border p-2">V</th>
                  <th className="border p-2">Q</th>
                </>
              )}
            </tr>
          </thead>
          <tbody>
            {allRows.map(([name, station]) => (
              <tr key={name}>
                <td className="border p-2 text-center">{name}</td>
                <td className="border p-2 text-center">
                  {station.busy ? "1" : "0"}
                </td>
                {type === "arithmetic" && (
                  <>
                    <td className="border p-2 text-center">
                      {station.op || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.vj || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.vk || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.qj || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.qk || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.address || "-"}
                    </td>
                  </>
                )}
                {type === "load" && (
                  <>
                    <td className="border p-2 text-center">
                      {station.address || "-"}
                    </td>
                  </>
                )}
                {type === "store" && (
                  <>
                    <td className="border p-2 text-center">
                      {station.address || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.v || "-"}
                    </td>
                    <td className="border p-2 text-center">
                      {station.q || "-"}
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ReservationStationTable;
