import PropTypes from "prop-types";
import { createEmptyStation } from "../utils/helpers";

const ReservationStationTable = ({
  title,
  stations,
  type = "arithmetic",
  tableSize,
}) => {
  const generateEmptyRows = () => {
    const currentSize = stations.length;
    const targetSize = tableSize || stations.length; // Fallback to current size if not specified by user
    const emptyRows = [];

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
        const emptyStation = createEmptyStation();
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
              <th className="border p-2">Op</th>
              <th className="border p-2">Vj</th>
              <th className="border p-2">Vk</th>
              <th className="border p-2">Qj</th>
              <th className="border p-2">Qk</th>
              <th className="border p-2">Address</th>
            </tr>
          </thead>
          <tbody>
            {allRows.map(([name, station]) => (
              <tr key={name}>
                <td className="border p-2 text-center">{name}</td>
                <td className="border p-2 text-center">
                  {station.busy ? "1" : "0"}
                </td>
                <td className="border p-2 text-center">{station.op || "-"}</td>
                <td className="border p-2 text-center">{station.vj || "-"}</td>
                <td className="border p-2 text-center">{station.vk || "-"}</td>
                <td className="border p-2 text-center">{station.qj || "-"}</td>
                <td className="border p-2 text-center">{station.qk || "-"}</td>
                <td className="border p-2 text-center">{station.a || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
ReservationStationTable.propTypes = {
  title: PropTypes.string.isRequired,
  stations: PropTypes.array,
  type: PropTypes.string,
  tableSize: PropTypes.number,
};

export default ReservationStationTable;
