import PropTypes from "prop-types";

export default function ExecTable({ data }) {
  return (
    <div className="w-3/4 ">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th colSpan={2} className="border border-gray-400 bg-gray-200 p-2">
              Instruction
            </th>
            <th className="border border-gray-400 bg-gray-200 p-2">J</th>
            <th className="border border-gray-400 bg-gray-200 p-2">K</th>
            <th className="border border-gray-400 bg-gray-200 p-2">Issue</th>
            <th className="border border-gray-400 bg-gray-200 p-2">
              Execution Complete
            </th>
            <th className="border border-gray-400 bg-gray-200 p-2">
              Write Result
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              <td className="border border-gray-400 p-2 text-center">
                {row.OP}
              </td>
              <td className="border border-gray-400 p-2 text-center">
                {row.Dest || "-"}{" "}
                {/* IN CASE OF STORE NO DEST, R[J] -> Mem[K]*/}
              </td>
              <td className="border border-gray-400 p-2 text-center">
                {row.j || "-"} {/* IN CASE OF LD NO DEST, Mem[K] -> R[J]*/}
              </td>
              <td className="border border-gray-400 p-2 text-center">
                {row.k}
              </td>
              <td className="border border-gray-400 p-2 text-center">
                {row.issue}
              </td>
              <td className="border border-gray-400 p-2 text-center">
                {row.execComp}
              </td>
              <td className="border border-gray-400 p-2 text-center">
                {row.writeResult}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

ExecTable.propTypes = {
  data: PropTypes.array.isRequired,
};
