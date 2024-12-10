import React from "react";

const ReservationStationTable = ({ title, stations, type = "arithmetic" }) => {
  return (
    <div>
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead className="bg-gray-100">
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
                  <th className="border p-2">A</th>
                </>
              )}
              {type === "load" && (
                <>
                  <th className="border p-2">Address</th>
                  <th className="border p-2">Dest</th>
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
            {stations.map(([name, station]) => (
              <tr key={name}>
                <td className="border p-2">{name}</td>
                <td className="border p-2">{station.busy ? "1" : "0"}</td>
                {type === "arithmetic" && (
                  <>
                    <td className="border p-2">{station.op}</td>
                    <td className="border p-2">{station.vj}</td>
                    <td className="border p-2">{station.vk}</td>
                    <td className="border p-2">{station.qj}</td>
                    <td className="border p-2">{station.qk}</td>
                    <td className="border p-2">{station.a}</td>
                  </>
                )}
                {type === "load" && (
                  <>
                    <td className="border p-2">{station.address}</td>
                    <td className="border p-2">{station.dest}</td>
                  </>
                )}
                {type === "store" && (
                  <>
                    <td className="border p-2">{station.address}</td>
                    <td className="border p-2">{station.v}</td>
                    <td className="border p-2">{station.q}</td>
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
